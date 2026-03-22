#!/usr/bin/env python3
"""
math-agent -- Autonomous research agent with dual backend support.

Supports two architectures:
  --arch claude  : Anthropic Claude API with native compaction (compact_20260112)
  --arch gpt     : OpenAI Responses API with previous_response_id + /responses/compact
  --arch gemini  : Google Gemini API with chat sessions + explicit context caching

Both architectures use the same worker/evaluator/narrator prompt design.
Context management is handled natively by each platform -- no custom Thread C.

Usage:
  python math-agent.py --prove goal.txt --seed seed.md
  python math-agent.py --prove goal.txt --seed seed.md --arch gpt
  python math-agent.py --prove goal.txt --seed seed.md --arch all --budget 15
  python math-agent.py --resume claude-001

Session auto-saves after every turn pair. Ctrl-C and --resume later.
"""

import sys
import os
import json
import argparse
import subprocess
import tempfile
import textwrap
import signal
from datetime import datetime
from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Cortex integration — cross-run memory for the math solver
# ---------------------------------------------------------------------------

CORTEX_URL = "http://127.0.0.1:8082"  # autonomous.db — isolated from personal cortex (8080)
CORTEX_TOKEN = "emc2ymmv"
CORTEX_ENABLED = False  # toggled by --cortex flag
CORTEX_TASK = None  # set by --cortex-task, prefixed to all tags

def cortex_semantic_search(query, limit=10, threshold=0.2):
    """Search Cortex for entries related to a query. Returns list of content strings."""
    if not CORTEX_ENABLED:
        return []
    try:
        import urllib.request
        url = f"{CORTEX_URL}/api/semantic?q={urllib.parse.quote(query)}&limit={limit}&threshold={threshold}&token={CORTEX_TOKEN}"
        req = urllib.request.Request(url, method="GET")
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        results = data.get("results", [])
        return [r["content"] for r in results if r.get("content")]
    except Exception as e:
        print(f"  [cortex] search failed: {e}")
        return []

def cortex_store(content, tags, source, entry_type="research"):
    """Store an entry in Cortex. Fire-and-forget."""
    if not CORTEX_ENABLED:
        return
    # Prefix tags with task namespace if set
    if CORTEX_TASK:
        tags = [f"task:{CORTEX_TASK}"] + tags
    try:
        import urllib.request
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": "math-agent",
            "method": "tools/call",
            "params": {
                "name": "cortex_store",
                "arguments": {
                    "content": content[:8000],
                    "tags": tags,
                    "source": source,
                    "entry_type": entry_type
                }
            }
        }).encode()
        req = urllib.request.Request(
            f"{CORTEX_URL}/mcp?token={CORTEX_TOKEN}",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
        print(f"  [cortex] stored ({len(content)} chars, tags={tags})")
    except Exception as e:
        print(f"  [cortex] store failed: {e}")


def cortex_recall_prior_work(goal, limit=15):
    """Query Cortex for prior research on this goal. Returns formatted context block."""
    if not CORTEX_ENABLED:
        return ""
    # Primary: task-specific results
    task_query = f"{goal} task:{CORTEX_TASK}" if CORTEX_TASK else goal
    results = cortex_semantic_search(task_query, limit=limit, threshold=0.2)
    if not results:
        # Fallback: broader search without task filter
        results = cortex_semantic_search(goal, limit=limit, threshold=0.3)
    if not results:
        return ""
    dead_ends = cortex_semantic_search(f"{goal} dead end failed REFUTED", limit=5, threshold=0.25)
    seen = set()
    all_results = []
    for r in results + dead_ends:
        key = r[:100]
        if key not in seen:
            seen.add(key)
            all_results.append(r)
    if not all_results:
        return ""
    block = "\n--- PRIOR RESEARCH (from Cortex memory) ---\n"
    block += "The following insights are from previous runs attacking this or related problems.\n"
    block += "TRUST verified results. AVOID repeating documented dead ends.\n\n"
    for i, entry in enumerate(all_results[:15], 1):
        text = entry[:500].strip()
        block += f"[{i}] {text}\n\n"
    block += "--- END PRIOR RESEARCH ---\n"
    return block


# ---------------------------------------------------------------------------
# Sandboxed Python execution for mathematical computation
# ---------------------------------------------------------------------------

ALLOWED_MODULES = {
    # User-facing math modules (for documentation only, not enforced)
    "math", "cmath", "fractions", "decimal", "statistics",
    "itertools", "functools", "collections", "operator",
    "random", "bisect", "heapq", "copy",
    "typing", "dataclasses", "enum", "abc",
}

# Dangerous modules: I/O, network, process, code execution
BLOCKED_MODULES = {
    "os", "subprocess", "shutil", "pathlib", "glob",
    "socket", "http", "urllib", "requests", "ftplib", "smtplib",
    "ctypes", "multiprocessing", "threading", "signal",
    "importlib", "code", "codeop", "compileall",
    "tempfile",
    "pickle", "shelve", "marshal",
    "webbrowser", "antigravity",
    "numpy", "sympy", "scipy", "matplotlib", "pandas",
}

SANDBOX_PRELUDE = textwrap.dedent("""\
    # Pre-import allowed modules before sandbox activates
    import math, cmath, fractions, decimal, statistics
    import itertools, functools, collections, operator
    import random, bisect, heapq, copy
    import typing, dataclasses, enum, abc

    # Sandbox: block dangerous modules
    import builtins as _builtins
    _BLOCKED = {blocked}
    _real_import = _builtins.__import__
    def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        top = name.split('.')[0]
        if top in _BLOCKED:
            raise ImportError(f"Module '{{name}}' is blocked in sandbox. "
                              f"Use only: math, itertools, fractions, collections, etc.")
        return _real_import(name, globals, locals, fromlist, level)
    _builtins.__import__ = _safe_import
    del _builtins

""")


def safe_compute(code: str, timeout: int = 30, max_output: int = 10000) -> str:
    """Run pure-math Python code in a sandboxed subprocess.
    
    Security layers:
    1. Import whitelist: only math-related modules allowed
    2. Subprocess isolation: separate process, no shared state
    3. Timeout: killed after `timeout` seconds
    4. Output cap: truncated to `max_output` chars
    5. No network: inherited from parent (no sockets in allowed modules)
    6. No file I/O: open() not in allowed scope, no os/subprocess/pathlib
    """
    prelude = SANDBOX_PRELUDE.format(blocked=repr(BLOCKED_MODULES))
    full_code = prelude + code

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, "-u", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            # Resource limits via ulimit would go here on Linux:
            # preexec_fn could set resource.setrlimit for memory
        )
        stdout = result.stdout[:max_output]
        stderr = result.stderr[:max_output]

        if result.returncode == 0:
            output = stdout.strip()
            if not output:
                output = "(Code ran successfully but produced no output.)"
            return output
        else:
            err_msg = stderr.strip() or "(Process exited with non-zero status)"
            return f"ERROR:\n{err_msg}"

    except subprocess.TimeoutExpired:
        return f"ERROR: Computation exceeded {timeout}s timeout. Simplify the calculation."
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# Tool definition for Claude API
COMPUTE_TOOL = {
    "name": "compute",
    "description": (
        "Run a short Python program for mathematical computation. "
        "You MUST use this tool instead of doing calculations in prose. "
        "Use this to verify conjectures on small cases, compute exact values, "
        "enumerate combinatorial objects, or check formulas numerically. "
        "ALLOWED modules: math, cmath, fractions, decimal, statistics, "
        "itertools, functools, collections, operator, random, bisect, "
        "heapq, copy, typing, dataclasses, enum, abc. "
        "NOT available: numpy, sympy, scipy, sage, matplotlib. "
        "No file I/O, no network, no os/subprocess. "
        "Print results to stdout. Timeout: 30 seconds. "
        "CALL THIS TOOL ON YOUR FIRST TURN for the smallest non-trivial case."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python code to execute. Must print results to stdout."
            }
        },
        "required": ["code"],
    },
}

def extract_claims_from_thinking(thinking_text, turn, goal):
    """Run Haiku over thinking to extract mathematical claims. Store to Cortex."""
    if not CORTEX_ENABLED or len(thinking_text) < 200:
        return
    try:
        from anthropic import Anthropic
        client = Anthropic()
        # Truncate to keep Haiku fast and cheap
        chunk = thinking_text[:6000]
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=(
                "Extract mathematical claims from this reasoning trace. "
                "For each claim, state: (a) the precise claim, (b) status: "
                "PROVED / ABANDONED / PARTIAL / CONJECTURE. "
                "Only include substantive mathematical statements, not process notes. "
                "If no claims found, say NONE. Be terse."
            ),
            messages=[{"role": "user", "content": chunk}]
        )
        claims = response.content[0].text.strip()
        if claims and claims != "NONE" and len(claims) > 20:
            cortex_store(
                f"[Turn {turn} claims extracted from thinking]\n{claims}",
                ["auto", "claims", "thinking-extract"],
                f"Turn {turn}, claim extraction, goal: {goal[:80]}",
                "research"
            )
            print(f"  [CLAIMS] Extracted {len(claims)} chars of claims from thinking")
    except Exception as e:
        print(f"  [CLAIMS] Extraction failed: {e}")


# Cortex tools for worker (memory across compaction)
REMEMBER_TOOL = {
    "name": "remember",
    "description": (
        "Store a finding in persistent memory that survives context compaction. "
        "Use when you have: (1) a proved lemma, (2) a verified dead end with "
        "precise reason, (3) a structural insight worth preserving, (4) a key "
        "computation result. Keep entries concise — state the RESULT and WHY, "
        "not the full derivation. This memory persists across compaction cycles."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "The finding to store. Be precise and concise."
            },
            "status": {
                "type": "string",
                "enum": ["proved", "refuted", "conjecture", "dead-end", "computation"],
                "description": "Classification of this finding."
            }
        },
        "required": ["content", "status"],
    },
}

RECALL_TOOL = {
    "name": "recall",
    "description": (
        "Search persistent memory for prior findings. Use this: "
        "(1) after context was compacted to recover lost details, "
        "(2) before exploring a direction that might have been tried, "
        "(3) to check what has been proved or refuted so far. "
        "Returns relevant entries from all previous turns and runs."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "What to search for in memory."
            }
        },
        "required": ["query"],
    },
}

# ---------------------------------------------------------------------------
# Prompts (shared across architectures)
# ---------------------------------------------------------------------------

WORKER_SYSTEM = (
    "You are a mathematician. You are working toward a research goal "
    "given to you at the start.\n\n"
    "CRITICAL RULES:\n"
    "- You ARE the mathematician. Construct proofs. Attempt proof steps even "
    "if they might fail. Do NOT search for proofs others have written -- "
    "build arguments yourself from first principles.\n"
    "- NEVER end a turn with a question. Never ask 'Want me to...?' or "
    "'Shall I...?' or 'Which direction...?'. Always commit to your best "
    "option and execute it.\n"
    "- Each turn, do ONE meaningful step: prove a lemma, construct an "
    "argument, identify a precise obstruction, compute a small case, or "
    "(when directed) search the literature for a specific known result.\n"
    "- Be rigorous. State definitions, assumptions, and claims precisely. "
    "Distinguish conjecture from proof. Show reasoning step by step.\n"
    "- When you hit a wall, state precisely what the obstruction is and "
    "what would be needed to overcome it. Then try a different angle.\n"
    "- You have access to web search. Use it ONLY when you need to verify "
    "a specific theorem, find a known constant, or check whether a result "
    "already exists. Do NOT use search as a substitute for doing math. "
    "Do NOT spend more than one turn on literature search without "
    "returning to proof work.\n"
    "- At the end of each turn, state what you proved or learned, and "
    "what you will try next. Be concrete.\n"
    "- You MUST produce visible written output every turn. Your internal "
    "thinking is not visible to anyone. If you reason internally but write "
    "nothing, the turn is wasted.\n\n"

    "=== METACOGNITIVE FRAMEWORK ===\n\n"

    "You operate under four complementary disciplines. Apply them "
    "continuously, not as afterthoughts.\n\n"

    "1. PÓLYA (Attack):\n"
    "   After every proof step, ask:\n"
    "   - What was assumed? What was actually proved?\n"
    "   - Is the hypothesis necessary? Is the converse true?\n"
    "   - What happens in the smallest case? The degenerate case?\n"
    "   - Can I construct a counterexample to what I'm trying to prove?\n"
    "   If you cannot solve the problem, try to solve a simpler version "
    "first. If you cannot prove it, try to disprove it.\n\n"

    "2. TAO (Organize):\n"
    "   - Strip the problem to its bare essentials. Remove inessential "
    "generality.\n"
    "   - Track quantitative telemetry: after each attempt, report the "
    "exact margin by which it failed (off by how much? what degree gap? "
    "how many elements short?).\n"
    "   - Failed approaches are data, not waste. The pattern of failures "
    "maps the problem's structure.\n"
    "   - Do not obsess on a single approach. If three methods fail, the "
    "information is in WHY they fail, not in trying a fourth.\n\n"

    "3. LAKATOS (Diagnose failure):\n"
    "   When a proof attempt fails, classify the failure:\n"
    "   - LOCAL counterexample: a specific lemma is wrong, but the main "
    "conjecture might still hold. Fix the lemma.\n"
    "   - GLOBAL counterexample: the failure reveals the conjecture itself "
    "is wrong. The same sub-claim breaks in every approach.\n"
    "   KEY TEST: If 3+ genuinely different proof strategies all break at "
    "the same structural point (same deficit, same margin, same sub-claim), "
    "this is almost certainly a GLOBAL counterexample. The conjecture is "
    "false. Stop trying to prove it and pivot to:\n"
    "   (a) Computing the correct value for small cases\n"
    "   (b) Identifying the right conjecture\n"
    "   (c) Proving the corrected statement\n\n"

    "4. BORWEIN (Ground in evidence):\n"
    "   Before investing multiple turns in a proof, ensure the conjecture "
    "is consistent with known small cases. If small cases have already "
    "been computed (check the seed document), use them as evidence — "
    "do not recompute.\n"
    "   Computation can:\n"
    "   - Falsify a conjecture in seconds that proof attempts cannot "
    "resolve in hours\n"
    "   - Reveal the correct bound when the conjectured one is wrong\n"
    "   - Build intuition for why a true statement is true\n"
    "   But computation for a single case is NOT a proof. Your goal is "
    "general results.\n\n"

    "5. MECHANICAL RULE — COMPUTE vs PROVE:\n"
    "   If you have a compute tool, use it to CHECK specific claims. "
    "Do NOT use it as a substitute for mathematical reasoning. A "
    "computation that verifies a lemma for p=5 is useful; a DFS search "
    "that finds a witness without explaining why it exists is not.\n"
    "   If you do NOT have a compute tool (THEORIST thread), state "
    "claims that need computational verification as:\n"
    "   [VERIFY: <precise statement>]\n"
    "   and the COMPUTER thread will check them.\n\n"


    "6. HARD RULE — PROOF IS THE PRODUCT:\n"
    "   Every turn MUST contain at least one of:\n"
    "   (a) A lemma statement with proof or proof attempt\n"
    "   (b) A precise obstruction: I cannot prove X because Y\n"
    "   (c) A conjecture with structural justification (not just data)\n"
    "   Computation alone is NOT a valid turn. Before calling compute,\n"
    "   state your conjecture first. Running N random trials is NOT\n"
    "   progress. Proving WHY those trials fail IS progress.\n"
    "   Ask: what theorem would make this search unnecessary?\n\n"

    "=== END FRAMEWORK ===\n\n"

    "When you believe the research goal has been fully addressed (theorem "
    "proved, conjecture resolved, counterexample found, correct bound "
    "identified, or definitive obstruction identified), end your message "
    "with [DONE].\n"
    "Do NOT say [DONE] prematurely."
)

EVALUATOR_SYSTEM = (
    "You oversee a mathematical research worker. Your job is simple: "
    "detect when the worker is stuck and force a reframe. That is your "
    "ONLY job. You are not a peer reviewer. You are not checking proofs "
    "line by line. You are watching for process failures.\n\n"
    "You have FIVE responses. Pick ONE per turn:\n\n"
    "COMMIT -- The worker is making real progress (new lemmas, new "
    "constructions, new obstructions identified, or computational "
    "results). Say 'Good. Keep going.' and nothing else. Do NOT pad "
    "with instructions. Do NOT list next steps. Brevity is the signal.\n\n"
    "REFRAME -- The worker is stuck. Signs of stuck:\n"
    "  * Offering menus of options instead of committing to one\n"
    "  * Restating the problem rather than advancing it\n"
    "  * Output is longer than last turn with less new content\n"
    "When you see these signs, say REFRAME and then ONE of:\n"
    "  - 'You are spinning. Commit to a specific proof step or explain "
    "precisely what is blocking you.'\n"
    "  - 'You are restating known facts. State ONE new thing you will "
    "try and do it.'\n\n"
    "CHALLENGE (Lakatos test) -- This is the MOST IMPORTANT signal. "
    "Issue it when:\n"
    "  * 3+ genuinely different proof approaches have failed\n"
    "  * They all fail at a quantitatively similar margin (off by 1, "
    "degree gap of 2, one element short, etc.)\n"
    "  * The worker keeps trying new methods instead of questioning the "
    "conjecture\n"
    "This pattern means the failures are GLOBAL, not LOCAL (Lakatos). "
    "The conjecture itself is likely false. Say CHALLENGE and then:\n"
    "  'Lakatos test: You have tried [list approaches]. They all fail "
    "by [margin]. Multiple independent proofs breaking at the same "
    "structural point is evidence of a GLOBAL counterexample — the "
    "conjecture is likely false, not your methods. STOP proving. "
    "Spend this turn computing the exact value for the smallest case "
    "(e.g., p=3 or n=2). Report the numerical result. If it contradicts "
    "the conjecture, pivot to finding the correct bound.'\n"
    "CHALLENGE overrides REFRAME. Do not tell the worker to try yet "
    "another proof method when the pattern says the target is wrong.\n\n"
    "SEARCH -- The worker needs external information to get unstuck. "
    "NOT because searching is the default, but because there is a "
    "specific theorem, constant, or technique the worker needs and "
    "does not have. Say SEARCH and specify exactly what to look for.\n\n"
    "ABORT -- The research has reached a dead end and further turns "
    "will waste budget. Issue ABORT when:\n"
    "  * The worker has re-verified the same result 3+ times without "
    "advancing\n"
    "  * The problem has been solved (conjecture proved or disproved) "
    "but the worker cannot pivot to a new goal\n"
    "  * The worker is in an unbreakable loop (REFRAME issued 3+ times "
    "with no change in behavior)\n"
    "  * The remaining work clearly requires information or capabilities "
    "the worker does not have\n"
    "Say ABORT and then a 1-2 sentence explanation of why further turns "
    "are unproductive. Include [STOP] on a separate line.\n\n"
    "IMPORTANT:\n"
    "- Default to COMMIT. Most turns, the worker should just keep going.\n"
    "- NEVER issue SEARCH on consecutive turns. If the worker just "
    "searched, they should be DOING MATH with what they found.\n"
    "- HARD RULE: If the worker has spent 2+ turns on literature search "
    "without finding a specific, citable result that changes the approach, "
    "issue REFRAME. Say: 'Literature search has not produced results. "
    "Stop searching. Attempt a direct proof. Start with [specific step].' "
    "Searching is a tool, not a research strategy.\n"
    "- HARD RULE: If you have issued COMMIT 3+ times in a row and the "
    "narrator/log shows no new lemma, bound, or construction, issue "
    "REFRAME. The worker is drifting.\n"
    "- HARD RULE: If 3+ independent approaches have all failed at a "
    "quantitatively similar margin, issue CHALLENGE immediately. Do "
    "not issue COMMIT, REFRAME, or SEARCH — the problem is the "
    "conjecture, not the method.\n"
    "- If the worker has not tested the conjecture computationally for "
    "any small case, and has already failed twice, consider issuing "
    "CHALLENGE early. Borwein's principle: compute before you prove.\n"
    "- HARD RULE: If the worker performs numerical calculations in prose "
    "(e.g., checking sums, enumerating elements, verifying bounds by "
    "hand-waving) instead of calling the compute tool AND the worker "
    "has compute access, issue REFRAME "
    "and say: 'You are computing in prose. Use the compute tool — it "
    "gives exact results. Write Python code to [specific task]. Do not "
    "hand-calculate.' Prose computation is unreliable and must not be "
    "accepted as verification. (Exception: the THEORIST thread does not "
    "have compute access and should use [VERIFY: ...] requests instead.)\n"
    "- Keep your responses SHORT. A few sentences max. The worker does "
    "not need a rubric or a numbered list of suggestions.\n"
    "- You may see a WORKER INTERNAL THINKING section. This shows the "
    "worker's extended reasoning that was NOT in their visible output. "
    "Use it to: (a) give credit for progress even when visible output is "
    "sparse, (b) detect dead-end reasoning early, (c) give targeted "
    "REFRAME instructions referencing specific ideas from thinking. "
    "If thinking contains a real lemma or insight but visible output is "
    "empty, issue REFRAME with: 'You derived [specific result] in your "
    "thinking. Write it up as visible output.'\n"
    "- HARD RULE (PROOF VALUE): If the worker has done 2+ turns of\n"
    "  computation without producing a lemma, conjecture-with-justification,\n"
    "  or precise obstruction, issue REFRAME: 'You are building a\n"
    "  calculator, not proving a theorem. State what structural property\n"
    "  you believe holds and WHY. Then use computation only to check it.'\n"
    "  A turn that proves even a partial lemma always gets COMMIT.\n"
    "  A turn that only reports computational counts gets REFRAME.\n\n"
    "You also maintain a RESEARCH LOG. After your directive, on a new "
    "line write '---LOG---' followed by a 2-3 sentence summary of what "
    "the worker accomplished this turn and the cumulative state of the "
    "research. In the log, track:\n"
    "  - Number of independent approaches tried\n"
    "  - The quantitative margin of failure for each\n"
    "  - Whether a Lakatos CHALLENGE threshold has been reached\n"
    "This log persists across turns."
)

NARRATOR_SYSTEM = (
    "You write a 1-paragraph plain-language summary of a research round for "
    "a non-specialist. End with a vibe check: (green) = real progress, "
    "(yellow) = working but unclear if productive, (red) = stuck or spinning. "
    "Be honest. One paragraph only."
)

# ---------------------------------------------------------------------------
# Team mode: thread-specific worker addenda and coordinator
# ---------------------------------------------------------------------------

TEAM_THREAD_ADDENDA = {
    "theorist": (
        "\n\n=== THREAD ROLE: THEORIST (NO COMPUTE ACCESS) ===\n"
        "You are a pure mathematician. You DO NOT have access to computation.\n"
        "Do not write Python code. Do not ask for code to be run. Your output\n"
        "is proofs, lemmas, conjectures, and proof sketches.\n\n"
        "Your job:\n"
        "- Prove theorems about η(C_p³) that hold for ALL primes p, not just\n"
        "  specific values.\n"
        "- When you need a computation checked, STATE the precise claim you\n"
        "  need verified and the COMPUTER thread will check it. Format:\n"
        "  [VERIFY: <precise mathematical statement to check computationally>]\n"
        "- Work from the verified facts in the seed document. Trust those\n"
        "  results.\n"
        "- Produce REUSABLE results: a lemma that constrains extremal sequences\n"
        "  for all p is worth more than any single computation.\n\n"
        "Key proof strategies:\n"
        "- Multiplicity argument: if a sequence has length > 8(p-1), either\n"
        "  some element has multiplicity ≥ p (giving immediate zero-sum) or\n"
        "  the support has ≥ 9 elements with avg mult > 8(p-1)/9. What\n"
        "  structural property of 9-element sets forces a short zero-sum?\n"
        "- Projection: project C_p³ → C_p² via coordinate maps. The image\n"
        "  sequence has η(C_p²) = 3p-2, which constrains multiplicity\n"
        "  distributions.\n"
        "- Sumset growth: track |Σ_k(S)| as elements are added. When does\n"
        "  the sumset necessarily cover 0?\n"
        "- Cap set connection: extremals have support size 8 for p=3,5.\n"
        "  The maximum cap in AG(3,p) grows with p, but the zero-sum-free\n"
        "  support stays at 8. Why?\n\n"
        "You succeed by PROVING things, not by conjecturing and hoping.\n"
        "A partial proof (e.g., 'η ≥ 8p-7 for all p') is a real result.\n"
        "An unproved conjecture is not.\n"
    ),
    "computer": (
        "\n\n=== THREAD ROLE: COMPUTER (COMPUTATION ON REQUEST) ===\n"
        "You run computations that the THEORIST or CRITIC requests.\n"
        "You also independently explore computational patterns that could\n"
        "inform proof directions.\n\n"
        "Your job:\n"
        "- When the theorist says [VERIFY: ...], write and run code to\n"
        "  check that claim. Report the result precisely.\n"
        "- Independently explore: for p=7, can you find a length-48 = 8(6)\n"
        "  witness? What does its support look like?\n"
        "- Characterize GL(3,p)-orbits of extremal supports for p=3,5.\n"
        "- Test specific lemma hypotheses: if the theorist claims 'every\n"
        "  9-element set with mult p-1 has a short zero-sum,' verify for\n"
        "  p=3 and p=5.\n\n"
        "CRITICAL: Every computation must be tied to a conjecture or proof\n"
        "direction. Do NOT run DFS searches without a specific hypothesis.\n"
        "State what you expect before running, and what the result means.\n\n"
        "Your success metric: produce certified facts that the THEORIST\n"
        "can use as lemma inputs for general-p proofs.\n"
    ),
    "critic": (
        "\n\n=== THREAD ROLE: CRITIC / PROOF AUDITOR ===\n"
        "You audit the THEORIST's proof attempts for correctness.\n"
        "You also identify gaps and suggest how to fill them.\n\n"
        "Your job:\n"
        "- Read the theorist's latest proof attempt carefully.\n"
        "- Identify the weakest step. Is there an unjustified claim?\n"
        "  An implicit assumption? A case not covered?\n"
        "- If you find a gap, state it precisely and suggest either:\n"
        "  (a) A way to fix it (a stronger hypothesis, a different lemma)\n"
        "  (b) A [VERIFY: ...] request for the COMPUTER to check if the\n"
        "      gap is real or the claim is actually true\n"
        "- If the proof looks correct, say so and suggest the next step.\n"
        "- You CAN use compute to construct counterexamples to claimed\n"
        "  lemmas. This is your most powerful tool: a specific 9-element\n"
        "  set that avoids short zero-sums would refute a key lemma.\n\n"
        "You succeed by catching errors BEFORE they waste multiple turns,\n"
        "and by sharpening vague arguments into rigorous ones.\n"
    ),
}

COORDINATOR_SYSTEM = (
    "You are a research coordinator managing three parallel threads:\n"
    "- Thread THEORIST: proves theorems. NO compute access. Produces lemmas,\n"
    "  proofs, and [VERIFY: ...] requests for the COMPUTER.\n"
    "- Thread COMPUTER: runs computations. Responds to THEORIST/CRITIC\n"
    "  verification requests and independently explores patterns.\n"
    "- Thread CRITIC: audits proofs for correctness. Identifies gaps.\n\n"
    "Your job is to ROUTE information between threads:\n"
    "1. If THEORIST made a [VERIFY: ...] request, tell COMPUTER to run it.\n"
    "2. If COMPUTER found a result, tell THEORIST and CRITIC.\n"
    "3. If CRITIC found a gap, tell THEORIST to fix it.\n"
    "4. If THEORIST is spinning without progress, tell them to try a\n"
    "   different proof approach (projection, pigeonhole, sumset growth).\n"
    "5. If COMPUTER is running searches with no hypothesis, tell them to\n"
    "   STOP and wait for a specific question from THEORIST.\n"
    "6. MOST IMPORTANT: If the THEORIST has a promising partial proof,\n"
    "   focus ALL threads on completing it. Don't let COMPUTER wander.\n\n"
    "Format:\n"
    "THEORIST: <injection>\n"
    "COMPUTER: <injection>\n"
    "CRITIC: <injection>\n\n"
    "Keep each injection to 2-3 sentences MAX. Be specific and actionable. "
    "Do NOT summarize — the threads need direction, not recaps."
    "\n\n"
    "GROUNDING RULES (CRITICAL):\n"
    "- You may ONLY relay claims a thread EXPLICITLY made.\n"
    "- NEVER claim a result was proved or machine-checked unless the\n"
    "  thread used those exact words about a specific result.\n"
    "- NEVER synthesize across threads to claim a composite result\n"
    "  that no single thread stated.\n"
    "- Empirical evidence (tested N cases) is NOT proof. Relay it as\n"
    "  evidence, not as a proved result.\n"
    "- When in doubt, quote the thread rather than paraphrase."
)


# ---------------------------------------------------------------------------
# Session (shared)
# ---------------------------------------------------------------------------

class Session:
    def __init__(self, goal, seed="", arch="claude"):
        self.goal = goal
        self.seed = seed
        self.arch = arch
        self.turn = 0
        self.thread_a_messages = []
        self.thread_b_messages = []
        self.research_log = ""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cache_read = 0
        self.total_cache_create = 0
        self.compressions = 0
        self.searches = 0
        # GPT-specific: track response IDs for chaining
        self.gpt_worker_prev_id = None
        self.gpt_eval_prev_id = None

        # Auto-increment run number
        import glob
        existing = glob.glob(f"{arch}-*")
        if existing:
            nums = []
            for f in existing:
                # Extract number from e.g. "claude-003" or "claude-003-brief"
                parts = f.replace(f"{arch}-", "").split("-")
                if parts[0].isdigit():
                    nums.append(int(parts[0]))
            run_num = max(nums) + 1 if nums else 1
        else:
            run_num = 1
        base = f"{arch}-{run_num:03d}"
        self.session_file = base
        self.log_file = f"{base}-log"
        self.briefing_file = f"{base}-brief"

        with open(self.briefing_file, "w") as f:
            f.write(f"# Research Briefing\n\n**Goal:** {goal}\n\n---\n\n")

    def save(self):
        data = {k: v for k, v in self.__dict__.items()}
        with open(self.session_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  [>] Saved to {self.session_file}")

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        s = cls.__new__(cls)
        for k, v in data.items():
            setattr(s, k, v)
        return s

    def estimate_cost(self):
        if self.arch == "claude":
            # Opus: $15/M in, $75/M out, cache read $1.875/M, cache create $18.75/M
            input_cost = (self.total_input_tokens / 1_000_000) * 15
            output_cost = (self.total_output_tokens / 1_000_000) * 75
            cache_savings = (self.total_cache_read / 1_000_000) * 13.125
            return input_cost + output_cost - cache_savings
        elif self.arch == "gpt":
            # GPT-5.2: $1.75/MTok in, $14/MTok out, cached $0.175/MTok
            input_cost = (self.total_input_tokens / 1_000_000) * 1.75
            output_cost = (self.total_output_tokens / 1_000_000) * 14
            cache_savings = (self.total_cache_read / 1_000_000) * 1.575
            return input_cost + output_cost - cache_savings
        else:  # gemini
            # Gemini 2.5 Pro: $1.25/MTok in, $10/MTok out, cached 90% off
            input_cost = (self.total_input_tokens / 1_000_000) * 1.25
            output_cost = (self.total_output_tokens / 1_000_000) * 10
            cache_savings = (self.total_cache_read / 1_000_000) * 1.125
            return input_cost + output_cost - cache_savings

    def log_to_file(self, msg):
        with open(self.log_file, "a") as f:
            f.write(msg + "\n")


# ---------------------------------------------------------------------------
# Backend: Claude (Anthropic API with native compaction)
# ---------------------------------------------------------------------------

class ClaudeBackend:
    def __init__(self, worker_model, eval_model, narrator_model,
                 enable_thinking, compact_threshold):
        from anthropic import Anthropic
        self.client = Anthropic()
        self.worker_model = worker_model
        self.eval_model = eval_model
        self.narrator_model = narrator_model
        self.enable_thinking = enable_thinking
        self.compact_threshold = compact_threshold

    def _make_cacheable(self, messages):
        if not messages:
            return messages
        result = []
        for i, msg in enumerate(messages):
            if i == len(messages) - 1 and msg["role"] == "user":
                content = msg["content"]
                if isinstance(content, str):
                    content = [{"type": "text", "text": content,
                               "cache_control": {"type": "ephemeral"}}]
                result.append({"role": msg["role"], "content": content})
            else:
                result.append(msg)
        return result

    def call_worker(self, messages):
        sys_text = WORKER_SYSTEM
        if CORTEX_ENABLED:
            sys_text += (
                "\n\n=== PERSISTENT MEMORY ===\n"
                "You have two memory tools: 'remember' and 'recall'.\n"
                "- Use 'remember' to store KEY findings that must survive compaction: "
                "proved lemmas, verified dead ends, critical constants, structural insights.\n"
                "- Use 'recall' to search memory when you need a fact from earlier turns "
                "that may have been compacted away, or to check if a direction was tried before.\n"
                "- Store results AFTER verifying them, not before. No speculative stores.\n"
                "- Keep entries concise: the result and why, not the full derivation.\n"
                "=== END MEMORY ===\n"
            )
        system = [{"type": "text", "text": sys_text,
                   "cache_control": {"type": "ephemeral"}}]
        kwargs = {
            "model": self.worker_model,
            "max_tokens": 16384,
            "system": system,
            "messages": self._make_cacheable(messages),
            "betas": ["compact-2026-01-12"],
            "context_management": {
                "edits": [{
                    "type": "compact_20260112",
                    "trigger": {"type": "input_tokens",
                                "value": self.compact_threshold},
                }]
            },
        }

        kwargs["tools"] = [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5,
            },
            COMPUTE_TOOL,
        ]
        if CORTEX_ENABLED:
            kwargs["tools"].extend([REMEMBER_TOOL, RECALL_TOOL])

        if self.enable_thinking:
            kwargs["temperature"] = 1
            kwargs["thinking"] = {"type": "adaptive"}
            kwargs["output_config"] = {"effort": "max"}

        response = self.client.beta.messages.create(**kwargs)

        all_content = list(response.content)
        total_in = response.usage.input_tokens
        total_out = response.usage.output_tokens

        # Handle tool_use loops (compute tool) and pause_turn
        max_tool_rounds = 5
        tool_round = 0
        while (response.stop_reason in ("tool_use", "pause_turn")
               and tool_round < max_tool_rounds):
            tool_round += 1

            if response.stop_reason == "pause_turn":
                cont_msgs = list(messages)
                cont_msgs.append({"role": "assistant", "content": response.content})
                cont_msgs.append({"role": "user", "content": "Continue."})
                kwargs["messages"] = cont_msgs
                response = self.client.beta.messages.create(**kwargs)
                all_content.extend(response.content)
                total_in += response.usage.input_tokens
                total_out += response.usage.output_tokens

            elif response.stop_reason == "tool_use":
                # Find tool_use blocks and execute them
                tool_results = []
                for block in response.content:
                    if not (hasattr(block, "type") and block.type == "tool_use"):
                        continue

                    if block.name == "compute":
                        code = block.input.get("code", "")
                        print(f"  [COMPUTE] Running {len(code)} chars of Python...")
                        result = safe_compute(code)
                        if result.startswith("ERROR"):
                            print(f"  [COMPUTE] {result}")
                        else:
                            print(f"  [COMPUTE] Result: {result[:200]}")
                        compute_log = (
                            f"\n\n--- COMPUTE ---\n```python\n{code}\n```\n"
                            f"**Output:**\n```\n{result}\n```\n--- END COMPUTE ---\n\n"
                        )
                        all_content.append(type("FakeText", (), {
                            "type": "text", "text": compute_log})())
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                    elif block.name == "remember" and CORTEX_ENABLED:
                        content = block.input.get("content", "")
                        status = block.input.get("status", "note")
                        print(f"  [REMEMBER] Storing {len(content)} chars [{status}]")
                        cortex_store(
                            content,
                            ["auto", status, "worker"],
                            f"Turn {getattr(self, '_current_turn', '?')}, worker remember",
                            "research" if status in ("proved", "conjecture") else "insight"
                        )
                        result = f"Stored to memory [{status}]: {content[:80]}..."
                        all_content.append(type("FakeText", (), {
                            "type": "text", "text": f"\n[MEMORY STORED: {status}] {content[:200]}\n"})())
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                    elif block.name == "recall" and CORTEX_ENABLED:
                        query = block.input.get("query", "")
                        print(f"  [RECALL] Searching: {query[:80]}")
                        results = cortex_semantic_search(query, limit=8, threshold=0.2)
                        if results:
                            result = "\n\n".join(f"[{i+1}] {r[:400]}" for i, r in enumerate(results))
                            print(f"  [RECALL] Found {len(results)} entries")
                        else:
                            result = "No relevant entries found in memory."
                            print(f"  [RECALL] No results")
                        all_content.append(type("FakeText", (), {
                            "type": "text", "text": f"\n[MEMORY RECALL: {len(results)} results for '{query}']\n"})())
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                if tool_results:
                    cont_msgs = list(messages)
                    cont_msgs.append({"role": "assistant",
                                      "content": response.content})
                    cont_msgs.append({"role": "user", "content": tool_results})
                    kwargs["messages"] = cont_msgs
                    response = self.client.beta.messages.create(**kwargs)
                    all_content.extend(response.content)
                    total_in += response.usage.input_tokens
                    total_out += response.usage.output_tokens
                else:
                    break  # No compute tool calls found, stop

        # Check for compaction
        compacted = False
        for block in all_content:
            if hasattr(block, "type") and block.type == "compaction":
                compacted = True

        # After compaction: refresh from Cortex to recover lost detail
        if compacted and CORTEX_ENABLED:
            prior = cortex_recall_prior_work(self._current_goal if hasattr(self, '_current_goal') else '')
            if prior:
                all_content.append(type("FakeText", (), {
                    "type": "text",
                    "text": f"\n\n[MEMORY REFRESH after compaction]\n{prior}"})())
                print(f"  [cortex] Post-compaction refresh: {len(prior)} chars injected")

        text_parts = []
        thinking_parts = []
        searches = 0
        for block in all_content:
            if hasattr(block, "type"):
                if block.type == "text" and hasattr(block, "text") and block.text.strip():
                    text_parts.append(block.text)
                elif block.type == "thinking" and hasattr(block, "thinking"):
                    thinking_parts.append(block.thinking)
                elif block.type == "web_search_tool_result":
                    searches += 1

        # Log thinking blocks (valuable even when text exists)
        if thinking_parts:
            thinking_combined = "\n---\n".join(thinking_parts)
            print(f"  [THINKING] {len(thinking_parts)} blocks, {len(thinking_combined)} chars")

        text = "\n".join(text_parts)
        if not text.strip():
            # Worker dumped everything into thinking.
            if thinking_parts and CORTEX_ENABLED:
                # Rescue thinking content to Cortex before it's lost
                thinking_combined = "\n".join(thinking_parts)
                cortex_store(
                    f"[Thinking rescue, turn {getattr(self, '_current_turn', '?')}] "
                    + thinking_combined[:3000],
                    ["auto", "thinking-rescue"],
                    f"Turn {getattr(self, '_current_turn', '?')}, thinking rescue",
                    "research"
                )
                print(f"  [cortex] Rescued {min(len(thinking_combined), 3000)} chars from thinking")

            # RETRY: ask worker to externalize, with hint from its thinking
            retry_msgs = list(messages)
            retry_msgs.append({"role": "assistant", "content": "[no visible output]"})
            retry_prompt = (
                "You produced no visible output -- your reasoning was entirely "
                "internal. Write your work out loud this time. Show the math."
            )
            if thinking_parts:
                hint = thinking_parts[-1][:1000]
                retry_prompt += (
                    f"\n\nHere is a fragment of your internal reasoning to "
                    f"reconstruct:\n{hint}"
                )
            retry_msgs.append({"role": "user", "content": retry_prompt})
            kwargs["messages"] = self._make_cacheable(retry_msgs)
            response = self.client.beta.messages.create(**kwargs)
            total_in += response.usage.input_tokens
            total_out += response.usage.output_tokens

            retry_parts = []
            for block in response.content:
                if hasattr(block, "type") and block.type == "text" and block.text.strip():
                    retry_parts.append(block.text)
            text = "\n".join(retry_parts)
            if not text.strip():
                text = "[Worker produced no visible output after retry. Evaluator should issue REFRAME.]"

        cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
        cache_create = getattr(response.usage, "cache_creation_input_tokens", 0)

        # Return the full content for message history (includes compaction blocks)
        return {
            "text": text,
            "thinking": "\n---\n".join(thinking_parts) if thinking_parts else "",
            "content": all_content,
            "in_tok": total_in,
            "out_tok": total_out,
            "searches": searches,
            "cache_read": cache_read,
            "cache_create": cache_create,
            "compacted": compacted,
        }

    def call_evaluator(self, messages):
        system = [{"type": "text", "text": EVALUATOR_SYSTEM,
                   "cache_control": {"type": "ephemeral"}}]
        kwargs = {
            "model": self.eval_model,
            "max_tokens": 4096,
            "system": system,
            "messages": self._make_cacheable(messages),
        }
        if self.enable_thinking:
            kwargs["temperature"] = 1
            kwargs["thinking"] = {"type": "adaptive"}
            kwargs["output_config"] = {"effort": "high"}

        response = self.client.messages.create(**kwargs)
        text = "".join(b.text for b in response.content if b.type == "text")
        cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
        cache_create = getattr(response.usage, "cache_creation_input_tokens", 0)

        return {
            "text": text,
            "in_tok": response.usage.input_tokens,
            "out_tok": response.usage.output_tokens,
            "cache_read": cache_read,
            "cache_create": cache_create,
        }

    def call_narrator(self, worker_text, eval_text, goal, turn):
        response = self.client.messages.create(
            model=self.narrator_model,
            max_tokens=500,
            system=NARRATOR_SYSTEM,
            messages=[{"role": "user", "content": (
                f"Goal: {goal}\nTurn: {turn}\n\n"
                f"Worker output:\n{worker_text[:3000]}\n\n"
                f"Evaluator response:\n{eval_text[:1000]}"
            )}],
        )
        return "".join(b.text for b in response.content if b.type == "text")


# ---------------------------------------------------------------------------
# Backend: GPT (OpenAI Responses API with stateful chaining)
# ---------------------------------------------------------------------------

class GPTBackend:
    def __init__(self, worker_model, eval_model, narrator_model):
        from openai import OpenAI
        self.client = OpenAI()
        self.worker_model = worker_model
        self.eval_model = eval_model
        self.narrator_model = narrator_model

    def call_worker(self, messages, prev_response_id=None):
        # For the first call, send the full input.
        # For subsequent calls, use previous_response_id for chaining.
        last_msg = messages[-1]["content"] if messages else ""

        # Compute tool definition for OpenAI function calling
        compute_function = {
            "type": "function",
            "name": "compute",
            "description": (
                "Run a short Python program for mathematical computation. "
                "You MUST use this tool instead of doing calculations in prose. "
                "Use this to verify conjectures on small cases, compute exact values, "
                "enumerate combinatorial objects, or check formulas numerically. "
                "ALLOWED modules: math, cmath, fractions, decimal, statistics, "
                "itertools, functools, collections, operator, random, bisect, "
                "heapq, copy, typing, dataclasses, enum, abc. "
                "NOT available: numpy, sympy, scipy, sage, matplotlib. "
                "No file I/O, no network, no os/subprocess. "
                "Print results to stdout. Timeout: 30 seconds. "
                "CALL THIS TOOL ON YOUR FIRST TURN for the smallest non-trivial case."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute. Must print results to stdout."
                    }
                },
                "required": ["code"],
            },
        }

        # Per-thread compute control: theorist gets NO compute tool
        allow_compute = getattr(self, '_allow_compute', True)
        if allow_compute:
            tools = [{"type": "web_search"}, compute_function]
        else:
            tools = [{"type": "web_search"}]

        kwargs = {
            "model": self.worker_model,
            "instructions": getattr(self, '_team_worker_system', WORKER_SYSTEM),
            "input": last_msg,
            "store": True,
            "tools": tools,
        }
        if prev_response_id:
            kwargs["previous_response_id"] = prev_response_id

        try:
            response = self.client.responses.create(**kwargs)
        except Exception as e:
            if "No tool output found" in str(e) or "not found" in str(e):
                print(f"  [WARN] Stale chain error, retrying fresh")
                kwargs.pop("previous_response_id", None)
                response = self.client.responses.create(**kwargs)
            else:
                raise

        total_in = response.usage.input_tokens
        total_out = response.usage.output_tokens
        compute_logs = []

        # Tool use loop: handle ALL function calls (compute + unknown)
        max_tool_rounds = 5
        tool_round = 0
        while tool_round < max_tool_rounds:
            all_fcs = [item for item in response.output
                       if getattr(item, "type", None) == "function_call"]
            if not all_fcs:
                break
            tool_round += 1

            import json as _json
            tool_outputs = []
            for fc in all_fcs:
                if getattr(fc, "name", None) == "compute":
                    args = _json.loads(fc.arguments) if isinstance(fc.arguments, str) else fc.arguments
                    code = args.get("code", "")
                    print(f"  [COMPUTE] Running {len(code)} chars of Python...")
                    result = safe_compute(code)
                    if result.startswith("ERROR"):
                        print(f"  [COMPUTE] {result}")
                    else:
                        print(f"  [COMPUTE] Result: {result[:200]}")
                    compute_logs.append(
                        f"\n\n--- COMPUTE ---\n```python\n{code}\n```\n"
                        f"**Output:**\n```\n{result}\n```\n--- END COMPUTE ---\n\n"
                    )
                else:
                    fn_name = getattr(fc, "name", "unknown")
                    print(f"  [TOOL] Unhandled function: {fn_name}")
                    result = f"ERROR: Function '{fn_name}' not available. Use 'compute'."
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": result,
                })

            # Send ALL outputs back in a single request
            kwargs2 = {
                "model": self.worker_model,
                "instructions": WORKER_SYSTEM,
                "input": tool_outputs,
                "store": True,
                "tools": [{"type": "web_search"}, compute_function],
                "previous_response_id": response.id,
            }
            response = self.client.responses.create(**kwargs2)
            total_in += response.usage.input_tokens
            total_out += response.usage.output_tokens


        text = response.output_text or ""
        if compute_logs:
            text = text + "\n".join(compute_logs)
        if not text.strip():
            text = "[Worker produced no visible output. Evaluator should issue REFRAME.]"

        cached = getattr(response.usage.input_tokens_details, "cached_tokens", 0)

        return {
            "text": text,
            "response_id": response.id,
            "in_tok": total_in,
            "out_tok": total_out,
            "searches": 0,  # TODO: count web search tool uses
            "cache_read": cached,
            "cache_create": 0,
            "compacted": False,
        }

    def call_evaluator(self, messages, prev_response_id=None):
        last_msg = messages[-1]["content"] if messages else ""

        kwargs = {
            "model": self.eval_model,
            "instructions": EVALUATOR_SYSTEM,
            "input": last_msg,
            "store": True,
        }
        if prev_response_id:
            kwargs["previous_response_id"] = prev_response_id

        response = self.client.responses.create(**kwargs)
        text = response.output_text or ""
        in_tok = response.usage.input_tokens
        out_tok = response.usage.output_tokens
        cached = getattr(response.usage.input_tokens_details, "cached_tokens", 0)

        return {
            "text": text,
            "response_id": response.id,
            "in_tok": in_tok,
            "out_tok": out_tok,
            "cache_read": cached,
            "cache_create": 0,
        }

    def call_narrator(self, worker_text, eval_text, goal, turn):
        response = self.client.responses.create(
            model=self.narrator_model,
            input=(
                f"Goal: {goal}\nTurn: {turn}\n\n"
                f"Worker output:\n{worker_text[:3000]}\n\n"
                f"Evaluator response:\n{eval_text[:1000]}"
            ),
            instructions=NARRATOR_SYSTEM,
        )
        return response.output_text or ""

    def compact_if_needed(self, response_id, threshold=80000):
        """Call /responses/compact if context is getting large."""
        try:
            result = self.client.responses.compact(response_id)
            return result
        except Exception:
            return None


# ---------------------------------------------------------------------------
# Backend: Gemini (Google GenAI with Interactions API or chat sessions)
# ---------------------------------------------------------------------------

class GeminiBackend:
    """
    Gemini backend using the google-genai SDK.

    Context strategy:
      - Uses client.chats for stateful multi-turn (SDK manages history locally)
      - Explicit context caching for the system prompt + seed (90% discount)
      - Implicit caching kicks in automatically for repeated prefixes
      - No native compaction endpoint; we do manual summarization when
        history grows past threshold (similar to old Thread C but using
        the same model)

    Models:
      - Worker: gemini-2.5-pro (1M context, strong reasoning, $1.25/$10 per MTok)
      - Evaluator: gemini-2.5-flash ($0.15/$0.60 per MTok)
      - Narrator: gemini-2.5-flash-lite ($0.10/$0.40 per MTok)

    Install: pip install google-genai
    Auth: export GEMINI_API_KEY=...
    """

    def __init__(self, worker_model, eval_model, narrator_model,
                 compact_threshold):
        from google import genai
        from google.genai import types
        self.genai = genai
        self.types = types
        self.client = genai.Client()
        self.worker_model = worker_model
        self.eval_model = eval_model
        self.narrator_model = narrator_model
        self.compact_threshold = compact_threshold

        # Create chat sessions for worker and evaluator
        self.worker_chat = self.client.chats.create(
            model=self.worker_model,
            config=types.GenerateContentConfig(
                system_instruction=WORKER_SYSTEM,
                temperature=1.0,
                max_output_tokens=16384,
                tools=[{"google_search": {}}],
            ),
        )
        self.eval_chat = self.client.chats.create(
            model=self.eval_model,
            config=types.GenerateContentConfig(
                system_instruction=EVALUATOR_SYSTEM,
                temperature=0.7,
                max_output_tokens=4096,
            ),
        )

    def _extract_usage(self, response):
        """Extract token counts from Gemini response."""
        meta = getattr(response, "usage_metadata", None)
        if meta:
            return {
                "in_tok": getattr(meta, "prompt_token_count", 0),
                "out_tok": getattr(meta, "candidates_token_count", 0),
                "cache_read": getattr(meta, "cached_content_token_count", 0),
            }
        return {"in_tok": 0, "out_tok": 0, "cache_read": 0}

    def _estimate_history_tokens(self, chat):
        """Rough estimate of tokens in chat history."""
        total = 0
        for msg in chat.get_history():
            for part in msg.parts:
                if hasattr(part, "text"):
                    total += len(part.text) // 4
        return total

    def _compress_if_needed(self, chat, role_name):
        """If history is too long, summarize and reset."""
        est = self._estimate_history_tokens(chat)
        if est <= self.compact_threshold:
            return False

        # Build history text
        history_text = ""
        for msg in chat.get_history():
            r = "WORKER" if msg.role == "model" else "INPUT"
            for part in msg.parts:
                if hasattr(part, "text"):
                    history_text += f"\n{r}: {part.text}\n"

        # Ask the model to summarize
        summary_response = self.client.models.generate_content(
            model=self.eval_model,
            contents=(
                "Compress this research conversation. Preserve ALL mathematical "
                "results, dead ends, current state, and next steps. Be precise.\n\n"
                + history_text[:100000]
            ),
        )
        summary = summary_response.text or ""

        # Reset the chat with compressed history
        if role_name == "worker":
            self.worker_chat = self.client.chats.create(
                model=self.worker_model,
                config=self.types.GenerateContentConfig(
                    system_instruction=WORKER_SYSTEM,
                    temperature=1.0,
                    max_output_tokens=16384,
                    tools=[{"google_search": {}}],
                ),
                history=[
                    self.types.Content(role="user", parts=[
                        self.types.Part.from_text(
                            f"COMPRESSED HISTORY:\n{summary}\n\nContinue. Do one meaningful step."
                        )
                    ]),
                ],
            )
        else:
            self.eval_chat = self.client.chats.create(
                model=self.eval_model,
                config=self.types.GenerateContentConfig(
                    system_instruction=EVALUATOR_SYSTEM,
                    temperature=0.7,
                    max_output_tokens=4096,
                ),
                history=[
                    self.types.Content(role="user", parts=[
                        self.types.Part.from_text(
                            f"COMPRESSED RESEARCH HISTORY:\n{summary}\n\nEvaluate the worker's next output."
                        )
                    ]),
                ],
            )
        return True

    def call_worker(self, messages):
        # Compress if needed
        compacted = self._compress_if_needed(self.worker_chat, "worker")

        last_msg = messages[-1]["content"] if messages else ""
        response = self.worker_chat.send_message(last_msg)
        text = response.text or ""

        if not text.strip():
            text = "[Worker produced no visible output. Evaluator should issue REFRAME.]"

        usage = self._extract_usage(response)
        searches = 0  # TODO: detect google_search tool use

        return {
            "text": text,
            "in_tok": usage["in_tok"],
            "out_tok": usage["out_tok"],
            "searches": searches,
            "cache_read": usage["cache_read"],
            "cache_create": 0,
            "compacted": compacted,
        }

    def call_evaluator(self, messages):
        compacted = self._compress_if_needed(self.eval_chat, "evaluator")

        last_msg = messages[-1]["content"] if messages else ""
        response = self.eval_chat.send_message(last_msg)
        text = response.text or ""
        usage = self._extract_usage(response)

        return {
            "text": text,
            "in_tok": usage["in_tok"],
            "out_tok": usage["out_tok"],
            "cache_read": usage["cache_read"],
            "cache_create": 0,
        }

    def call_narrator(self, worker_text, eval_text, goal, turn):
        response = self.client.models.generate_content(
            model=self.narrator_model,
            config=self.types.GenerateContentConfig(
                system_instruction=NARRATOR_SYSTEM,
                max_output_tokens=500,
            ),
            contents=(
                f"Goal: {goal}\nTurn: {turn}\n\n"
                f"Worker output:\n{worker_text[:3000]}\n\n"
                f"Evaluator response:\n{eval_text[:1000]}"
            ),
        )
        return response.text or ""


# ---------------------------------------------------------------------------
# Core loop (shared across architectures)
# ---------------------------------------------------------------------------

def run(session, backend, max_turns=20, max_cost=10.0):
    # Redirect all stdout and stderr to the log file
    log_handle = open(session.log_file, "a")
    _orig_stdout = sys.stdout
    _orig_stderr = sys.stderr
    sys.stdout = log_handle
    sys.stderr = log_handle

    try:
        _run_inner(session, backend, max_turns, max_cost)
    finally:
        sys.stdout = _orig_stdout
        sys.stderr = _orig_stderr
        log_handle.close()


def _run_inner(session, backend, max_turns=20, max_cost=10.0):
    print(f"\n{'='*70}")
    print(f"  MATH-AGENT -- Autonomous Research Agent")
    print(f"  Architecture: {session.arch.upper()}")
    print(f"  Goal: {session.goal}")
    if session.arch == "claude":
        print(f"  > Worker:  {backend.worker_model}")
        print(f"  > Eval:    {backend.eval_model}")
        print(f"  > Narrator: {backend.narrator_model}")
    else:
        print(f"  > Worker:  {backend.worker_model}")
        print(f"  > Eval:    {backend.eval_model}")
        print(f"  > Narrator: {backend.narrator_model}")
    print(f"  Cost limit: ${max_cost}")
    print(f"{'='*70}")
    print(f"\n  [f] Log file: {session.log_file}")

    # Set up initial message
    if session.turn == 0 and not session.thread_a_messages:
        initial = f"RESEARCH GOAL: {session.goal}\n"
        if session.seed:
            initial += f"\n--- SEED DOCUMENT ---\n{session.seed}\n--- END SEED ---\n"
            print(f"\n  [+] Seed: ~{len(session.seed)//4:,} tokens")
        # Cortex: inject prior research from previous runs
        prior = cortex_recall_prior_work(session.goal)
        if prior:
            initial += prior
            print(f"  [cortex] Injected {len(prior)} chars of prior research")
        initial += "\nBegin. Do one meaningful step."
        session.thread_a_messages.append({"role": "user", "content": initial})

    while session.turn < max_turns:
        session.turn += 1

        cost = session.estimate_cost()
        if cost > max_cost:
            print(f"\n{'='*70}")
            print(f"  [$] Cost limit: ${cost:.4f} > ${max_cost}")
            print(f"{'='*70}")
            session.save()
            save_output(session)
            return

        # --- Worker ---
        hdr = f"[W] [{datetime.now().strftime('%H:%M:%S')}] TURN {session.turn}/{max_turns}"
        print(f"\n{'-'*70}\n  {hdr}\n{'-'*70}")
        session.log_to_file(f"\n{'='*70}\n{hdr}\n{'='*70}")

        # Set context for Cortex tools
        backend._current_turn = session.turn
        backend._current_goal = session.goal

        if session.arch == "claude":
            w = backend.call_worker(session.thread_a_messages)
        elif session.arch == "gpt":
            w = backend.call_worker(session.thread_a_messages,
                                    prev_response_id=session.gpt_worker_prev_id)
            session.gpt_worker_prev_id = w.get("response_id")
        else:  # gemini
            w = backend.call_worker(session.thread_a_messages)

        session.total_input_tokens += w["in_tok"]
        session.total_output_tokens += w["out_tok"]
        session.total_cache_read += w["cache_read"]
        session.total_cache_create += w["cache_create"]
        session.searches += w["searches"]

        worker_text = w["text"].strip() if w["text"] else ""
        # Log thinking to dedicated file
        thinking_text = w.get("thinking", "")
        if thinking_text:
            thinking_file = session.session_file + "-thinking"
            with open(thinking_file, "a") as tf:
                tf.write(f"\n{'='*70}\nTURN {session.turn} THINKING ({len(thinking_text)} chars)\n{'='*70}\n")
                tf.write(thinking_text + "\n")
            print(f"  [THINKING] Logged {len(thinking_text)} chars to {thinking_file}")
            # Idea #1: extract claims from thinking via Haiku
            extract_claims_from_thinking(thinking_text, session.turn, session.goal)
        if not worker_text:
            worker_text = "(Worker produced empty output — possible failed search or API issue.)"
        display = worker_text[:2000]
        if len(worker_text) > 2000:
            display += f"\n  [...{len(worker_text)-2000} more chars...]"
        for line in display.split("\n"):
            print(f"  | {line}")
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] in={w['in_tok']:,} out={w['out_tok']:,} "
              f"cache={w['cache_read']:,} searches={w['searches']}"
              f"{' COMPACTED' if w.get('compacted') else ''}")

        session.log_to_file(f"\n{worker_text}\n[in={w['in_tok']:,} out={w['out_tok']:,}]")

        # For Claude, append the full content (with compaction blocks)
        if session.arch == "claude" and "content" in w:
            # Store serializable version
            session.thread_a_messages.append({"role": "assistant", "content": worker_text})
        else:
            session.thread_a_messages.append({"role": "assistant", "content": worker_text})

        if w.get("compacted"):
            session.compressions += 1
            print(f"  [C] Native compaction triggered (#{session.compressions})")
            # Idea #2: Thinking continuity — extract proof state from thinking
            # and inject it so the worker doesn't lose its thread after compaction
            if thinking_text and len(thinking_text) > 200:
                try:
                    from anthropic import Anthropic
                    _client = Anthropic()
                    _chunk = thinking_text[-8000:]  # last thinking block is most current
                    _resp = _client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=800,
                        system=(
                            "Summarize this mathematician's current proof strategy and state "
                            "in 3-5 sentences. Include: (1) what approach they're pursuing, "
                            "(2) what they've established so far, (3) what specific step they "
                            "were about to try next. Be precise with mathematical objects."
                        ),
                        messages=[{"role": "user", "content": _chunk}]
                    )
                    proof_state = _resp.content[0].text.strip()
                    # Inject as a user message so the worker sees it
                    session.thread_a_messages.append({
                        "role": "user",
                        "content": (
                            f"[CONTEXT RECOVERY after compaction]\n"
                            f"Your conversation history was compressed. Here is your "
                            f"proof state from your last reasoning:\n\n{proof_state}\n\n"
                            f"Continue from where you left off."
                        )
                    })
                    print(f"  [C] Injected {len(proof_state)} char proof state from thinking")
                except Exception as e:
                    print(f"  [C] Proof state extraction failed: {e}")

        if "[DONE]" in worker_text:
            print(f"\n{'='*70}")
            print(f"  [*] DONE at turn {session.turn} | ${session.estimate_cost():.4f}")
            print(f"{'='*70}")
            session.save()
            save_output(session)
            return

        # --- Evaluator ---
        ehdr = f"[E] [{datetime.now().strftime('%H:%M:%S')}] TURN {session.turn}/{max_turns}"
        print(f"\n{'-'*70}\n  {ehdr}\n{'-'*70}")
        session.log_to_file(f"\n{'='*70}\n{ehdr}\n{'='*70}")

        eval_msg = f"Worker output (turn {session.turn}):\n\n{worker_text}"
        # Include worker thinking for evaluator context
        if thinking_text:
            _tp = thinking_text[:3000]
            if len(thinking_text) > 3000:
                _tp += f"\n[...{len(thinking_text)-3000} more chars truncated...]"
            eval_msg += f"\n\n--- WORKER INTERNAL THINKING (not visible to worker) ---\n{_tp}\n--- END THINKING ---"
        if session.research_log:
            eval_msg = f"Research log so far:\n{session.research_log}\n\n---\n\n{eval_msg}"
        session.thread_b_messages.append({"role": "user", "content": eval_msg})

        if session.arch == "claude":
            e = backend.call_evaluator(session.thread_b_messages)
        elif session.arch == "gpt":
            e = backend.call_evaluator(session.thread_b_messages,
                                       prev_response_id=session.gpt_eval_prev_id)
            session.gpt_eval_prev_id = e.get("response_id")
        else:  # gemini
            e = backend.call_evaluator(session.thread_b_messages)

        eval_text = e["text"].strip() if e["text"] else ""
        if not eval_text:
            eval_text = "COMMIT\n\n(Evaluator produced empty output.)\n\n---LOG---\nEvaluator returned empty response."
        session.total_input_tokens += e["in_tok"]
        session.total_output_tokens += e["out_tok"]
        session.total_cache_read += e["cache_read"]
        session.total_cache_create += e["cache_create"]

        for line in eval_text.split("\n"):
            print(f"  | {line}")
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] in={e['in_tok']:,} out={e['out_tok']:,}")

        session.log_to_file(f"\n{eval_text}\n[in={e['in_tok']:,} out={e['out_tok']:,}]")
        session.thread_b_messages.append({"role": "assistant", "content": eval_text})

        # Extract log
        if "---LOG---" in eval_text:
            log_part = eval_text.split("---LOG---", 1)[1].strip()
            session.research_log += f"\n[Turn {session.turn}] {log_part}"
            # Auto-store evaluator log to Cortex
            if CORTEX_ENABLED and len(log_part) > 20:
                cortex_store(
                    f"[Turn {session.turn}] {log_part[:500]}",
                    ["auto", "evaluator-log", "turn-summary"],
                    f"Turn {session.turn}, evaluator, goal: {session.goal[:80]}",
                    "research"
                )

        eval_directive = eval_text.split("---LOG---")[0].strip() if "---LOG---" in eval_text else eval_text.strip()

        # --- Cortex: auto-store PROVEN/REFUTED results ---
        for _marker in ['PROVEN:', 'REFUTED:']:
            if _marker in worker_text or _marker in eval_text:
                _src = worker_text if _marker in worker_text else eval_text
                _idx = _src.index(_marker)
                _entry = _src[_idx:_idx+500].strip()
                _etype = 'research' if 'PROVEN' in _marker else 'insight'
                _tags = ['auto', _marker.rstrip(':').lower()]
                cortex_store(
                    _entry, _tags,
                    f'Turn {session.turn}, {session.arch}, goal: {session.goal[:80]}',
                    _etype
                )

        # --- Narrator ---
        narrator_text = backend.call_narrator(worker_text, eval_text, session.goal, session.turn)
        cost = session.estimate_cost()
        with open(session.briefing_file, "a") as f:
            f.write(f"### Round {session.turn}  ({datetime.now().strftime('%H:%M')})\n\n"
                    f"{narrator_text}\n\n"
                    f"**Cost so far: ${cost:.2f}** | "
                    f"Tokens: {session.total_input_tokens:,} in / "
                    f"{session.total_output_tokens:,} out\n\n")
        print(f"\n  [N] {narrator_text[:200]}")

        # Check for evaluator ABORT
        if "[STOP]" in eval_text:
            print(f"\n{'='*70}")
            print(f"  [!] EVALUATOR ABORT at turn {session.turn} | ${cost:.4f}")
            print(f"  [!] {eval_directive[:200]}")
            print(f"{'='*70}")
            with open(session.briefing_file, "a") as f:
                f.write(f"---\n\n**ABORTED by evaluator at turn {session.turn}.** "
                        f"Total cost: ${cost:.2f}\n\n")
            session.save()
            save_output(session)
            return

        # Feed back to worker
        feedback = f"EVALUATOR FEEDBACK (turn {session.turn}):\n{eval_directive}\n\nContinue. Do one meaningful step."
        session.thread_a_messages.append({"role": "user", "content": feedback})

        session.save()
        print(f"\n  [$] Cost: ${cost:.4f} | Tokens: {session.total_input_tokens:,} in / {session.total_output_tokens:,} out")

    print(f"\n{'='*70}\n  [!] Max turns ({max_turns}) | ${session.estimate_cost():.4f}\n{'='*70}")
    session.save()
    save_output(session)


def save_output(session):
    base = session.session_file
    result_file = f"{base}-result"
    with open(result_file, "w") as f:
        f.write(f"# Research Result\n\n**Goal:** {session.goal}\n**Arch:** {session.arch}\n"
                f"**Turns:** {session.turn}\n**Cost:** ${session.estimate_cost():.4f}\n\n"
                f"## Log\n\n{session.research_log}\n")
    print(f"  [R] {result_file}")

    trans_file = f"{base}-trans"
    with open(trans_file, "w") as f:
        f.write(f"# Transcript\n\n**Goal:** {session.goal}\n\n---\n\n")
        for i, msg in enumerate(session.thread_a_messages):
            role = "WORKER" if msg["role"] == "assistant" else "INPUT"
            content = msg["content"] if isinstance(msg["content"], str) else str(msg["content"])
            f.write(f"### {role} (msg {i+1})\n\n{content}\n\n---\n\n")
    print(f"  [T] {trans_file}")

    # Run post-mortem on thinking
    run_postmortem(session)


def run_postmortem(session):
    """Extract insights from thinking blocks using a cheap model.
    Runs on ABORT, max-turns, or DONE. Produces a postmortem file and
    stores extracted insights to Cortex."""
    thinking_file = session.session_file + "-thinking"
    postmortem_file = session.session_file + "-postmortem"

    try:
        with open(thinking_file, "r") as f:
            thinking_content = f.read()
    except FileNotFoundError:
        print(f"  [PM] No thinking file found, skipping post-mortem")
        return

    if len(thinking_content) < 200:
        print(f"  [PM] Thinking too short ({len(thinking_content)} chars), skipping")
        return

    print(f"  [PM] Running post-mortem on {len(thinking_content)} chars of thinking...")

    # Truncate if massive (Haiku context is 200K but let's be reasonable)
    if len(thinking_content) > 80000:
        thinking_content = thinking_content[:40000] + "\n\n[...MIDDLE TRUNCATED...]\n\n" + thinking_content[-40000:]

    try:
        from anthropic import Anthropic
        client = Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system=(
                "You are a mathematical research analyst. You are reading the internal "
                "thinking trace of a mathematician working on a hard problem. Extract "
                "the valuable content that should be preserved for future attempts.\n\n"
                "Produce a structured post-mortem with these sections:\n"
                "1. PARTIAL RESULTS: Lemmas or claims that were proved (even partially) "
                "during thinking. State each precisely.\n"
                "2. KEY INSIGHTS: Structural observations that could guide future work. "
                "What did the thinker LEARN about why the problem is hard?\n"
                "3. DEAD ENDS DISCOVERED: Approaches tried in thinking that failed, with "
                "the PRECISE reason for failure.\n"
                "4. NEAR MISSES: Arguments that almost worked. What specific gap "
                "prevented completion?\n"
                "5. RECOMMENDED NEXT STEP: The single most promising direction based "
                "on the thinking trace.\n\n"
                "Be concise but precise. Mathematical claims must be stated exactly. "
                "This document will be the seed for a future research run."
            ),
            messages=[{
                "role": "user",
                "content": f"RESEARCH GOAL: {session.goal}\n\n"
                           f"THINKING TRACE ({len(thinking_content)} chars):\n\n"
                           f"{thinking_content}"
            }]
        )

        postmortem_text = response.content[0].text
        pm_tokens = response.usage.input_tokens + response.usage.output_tokens
        print(f"  [PM] Post-mortem complete: {len(postmortem_text)} chars, {pm_tokens} tokens")

        # Write to file
        with open(postmortem_file, "w") as f:
            f.write(f"# Post-Mortem: {session.session_file}\n\n")
            f.write(f"**Goal:** {session.goal}\n")
            f.write(f"**Turns:** {session.turn}\n")
            f.write(f"**Cost:** ${session.estimate_cost():.2f}\n")
            f.write(f"**Thinking analyzed:** {len(thinking_content)} chars\n\n---\n\n")
            f.write(postmortem_text)
        print(f"  [PM] Written to {postmortem_file}")

        # Store to Cortex
        if CORTEX_ENABLED:
            cortex_store(
                f"POST-MORTEM ({session.session_file}, {session.turn} turns, "
                f"${session.estimate_cost():.2f}):\n\n{postmortem_text[:3000]}",
                ["auto", "postmortem", "thinking-extract"],
                f"Post-mortem of {session.session_file}, goal: {session.goal[:80]}",
                "research"
            )
            print(f"  [PM] Stored to Cortex")

    except Exception as e:
        print(f"  [PM] Post-mortem failed: {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# Team mode: run 3 specialized threads with coordinator
# ---------------------------------------------------------------------------

def call_coordinator(backend, briefings, turn_num, coord_system=None):
    """Call the coordinator to produce cross-pollination injections.
    
    briefings: dict of {thread_name: latest_briefing_text}
    Returns: dict of {thread_name: injection_text}
    """
    prompt = f"Current turn: {turn_num}\n\n"
    for name, text in briefings.items():
        prompt += f"=== THREAD {name.upper()} (latest briefing) ===\n{text}\n\n"
    prompt += "Write your injections for each thread."

    from openai import OpenAI
    client = OpenAI()
    response = client.responses.create(
        model=backend.narrator_model,  # use cheap model for coordinator
        instructions=coord_system or COORDINATOR_SYSTEM,
        input=prompt,
    )
    coord_text = ""
    for item in response.output:
        if hasattr(item, "text"):
            coord_text += item.text
        elif isinstance(item, dict) and "text" in item:
            coord_text += item["text"]
    if not coord_text:
        # Fallback: try to extract from output_text
        coord_text = getattr(response, "output_text", "") or ""

    # Parse injections
    injections = {}
    for thread_name in briefings:
        tag = thread_name.upper() + ":"
        if tag in coord_text:
            start = coord_text.index(tag) + len(tag)
            # Find next tag or end
            end = len(coord_text)
            for other_name in briefings:
                other_tag = other_name.upper() + ":"
                if other_tag != tag and other_tag in coord_text:
                    other_start = coord_text.index(other_tag)
                    if other_start > start and other_start < end:
                        end = other_start
            injections[thread_name] = coord_text[start:end].strip()
        else:
            injections[thread_name] = ""

    return injections, coord_text


def run_team(goal, seed, backend, max_turns_per_thread=8, max_cost=5.0,
             coord_interval=2, thread_config=None):
    """Run specialized threads in round-robin with periodic coordination.
    
    thread_config: optional dict with keys:
      - threads: list of {"name": str, "short": str, "addendum": str, "compute": bool}
      - coordinator_system: str (override COORDINATOR_SYSTEM)
    """
    if thread_config:
        thread_names = [t["name"] for t in thread_config["threads"]]
        thread_short = {t["name"]: t["short"] for t in thread_config["threads"]}
        custom_addenda = {t["name"]: t["addendum"] for t in thread_config["threads"]}
        compute_access = {t["name"]: t.get("compute", True) for t in thread_config["threads"]}
    else:
        thread_names = ["theorist", "computer", "critic"]
        thread_short = {"theorist": "T", "computer": "C", "critic": "K"}
        custom_addenda = None
        compute_access = {"theorist": False, "computer": True, "critic": True}

    # Compute team run number once
    import glob
    existing = glob.glob("team-*")
    if existing:
        nums = []
        for f_name in existing:
            parts = f_name.replace("team-", "").split("-")
            if parts[0].isdigit():
                nums.append(int(parts[0]))
        run_num = max(nums) + 1 if nums else 1
    else:
        run_num = 1

    # Create sessions for each thread
    sessions = {}
    for name in thread_names:
        s = Session(goal, seed=seed, arch="gpt")
        base = f"team-{run_num:03d}-{name}"
        s.session_file = base
        s.log_file = f"{base}-log"
        s.briefing_file = f"{base}-brief"
        with open(s.briefing_file, "w") as f:
            f.write(f"# Research Briefing ({name.upper()} thread)\n\n**Goal:** {goal}\n\n---\n\n")
        sessions[name] = s

    # Team-level briefing file
    team_brief_file = f"team-{run_num:03d}-brief"
    with open(team_brief_file, "w") as f:
        f.write(f"# Team Research Briefing\n\n**Goal:** {goal}\n"
                f"**Threads:** {', '.join(thread_names)}\n"
                f"**Max turns per thread:** {max_turns_per_thread}\n\n---\n\n")

    # Build thread-specific worker systems by appending addenda
    worker_systems = {}
    for name in thread_names:
        if custom_addenda and name in custom_addenda:
            worker_systems[name] = WORKER_SYSTEM + custom_addenda[name]
        else:
            addendum_key = {"theorist": "theorist", "computer": "computer",
                            "critic": "critic"}.get(name, name)
            if addendum_key in TEAM_THREAD_ADDENDA:
                worker_systems[name] = WORKER_SYSTEM + TEAM_THREAD_ADDENDA[addendum_key]
            else:
                worker_systems[name] = WORKER_SYSTEM

    # Set up initial messages for each thread
    for name in thread_names:
        s = sessions[name]
        initial = f"RESEARCH GOAL: {goal}\n"
        if seed:
            initial += f"\n--- SEED DOCUMENT ---\n{seed}\n--- END SEED ---\n"
        initial += "\nBegin. Do one meaningful step."
        s.thread_a_messages.append({"role": "user", "content": initial})

    # Redirect all output to a team log
    team_log = f"team-{run_num:03d}-log"
    log_handle = open(team_log, "a")
    _orig_stdout = sys.stdout
    _orig_stderr = sys.stderr
    sys.stdout = log_handle
    sys.stderr = log_handle

    try:
        coord_system = thread_config.get("coordinator_system") if thread_config else None
        _run_team_inner(sessions, thread_names, thread_short, backend,
                        worker_systems, max_turns_per_thread, max_cost,
                        coord_interval, team_brief_file, run_num,
                        compute_access=compute_access,
                        coord_system=coord_system)
    finally:
        sys.stdout = _orig_stdout
        sys.stderr = _orig_stderr
        log_handle.close()


def _run_team_inner(sessions, thread_names, thread_short, backend,
                    worker_systems, max_turns_per_thread, max_cost,
                    coord_interval, team_brief_file, run_num,
                    compute_access=None, coord_system=None):

    print(f"\n{'='*70}")
    print(f"  MATH-AGENT TEAM MODE -- 3 Specialized Threads")
    print(f"  Goal: {sessions[thread_names[0]].goal}")
    print(f"  Threads: {', '.join(n.upper() for n in thread_names)}")
    print(f"  Turns per thread: {max_turns_per_thread}")
    print(f"  Coordinator every: {coord_interval} turns")
    print(f"  Budget: ${max_cost}")
    print(f"  Backend: {backend.worker_model}")
    print(f"{'='*70}")

    # Track which threads are still alive
    alive = {name: True for name in thread_names}
    # Pending coordinator injections
    coord_injections = {name: "" for name in thread_names}

    total_global_turn = 0

    for round_num in range(1, max_turns_per_thread + 1):
        # Check if any threads still alive
        if not any(alive.values()):
            print(f"\n  [!] All threads stopped.")
            break

        # Total cost across all threads
        total_cost = sum(s.estimate_cost() for s in sessions.values())
        if total_cost > max_cost:
            print(f"\n  [$] Team budget exceeded: ${total_cost:.4f} > ${max_cost}")
            break

        # --- Coordinator call every coord_interval turns ---
        if round_num > 1 and (round_num - 1) % coord_interval == 0:
            print(f"\n{'#'*70}")
            print(f"  [COORD] Coordinating after round {round_num - 1}")
            print(f"{'#'*70}")

            # Gather latest briefings
            briefings = {}
            for name in thread_names:
                if alive[name]:
                    try:
                        with open(sessions[name].briefing_file) as f:
                            briefings[name] = f.read()[-2000:]  # last 2000 chars
                    except FileNotFoundError:
                        briefings[name] = "(no briefing yet)"
                else:
                    briefings[name] = "(thread stopped)"

            injections, coord_text = call_coordinator(
                backend, briefings, round_num, coord_system=coord_system)

            print(f"  [COORD] Full output:\n{coord_text}")

            for name, inj in injections.items():
                if inj and alive[name]:
                    coord_injections[name] = inj
                    print(f"  [COORD] -> {name.upper()}: {inj[:120]}")

            # Log to team brief
            with open(team_brief_file, "a") as f:
                f.write(f"\n### Coordination (after round {round_num - 1})\n\n"
                        f"{coord_text}\n\n---\n\n")

        # --- Run one turn for each alive thread ---
        for name in thread_names:
            if not alive[name]:
                continue

            session = sessions[name]
            session.turn += 1
            total_global_turn += 1
            tag = thread_short[name]

            hdr = (f"[{tag}:W] [{datetime.now().strftime('%H:%M:%S')}] "
                   f"{name.upper()} turn {session.turn}/{max_turns_per_thread}")
            print(f"\n{'-'*70}\n  {hdr}\n{'-'*70}")
            session.log_to_file(f"\n{'='*70}\n{hdr}\n{'='*70}")

            # --- Worker call ---
            # We need to temporarily override the worker system prompt
            orig_worker_system = None
            if hasattr(backend, '_team_worker_system'):
                orig_worker_system = backend._team_worker_system
            backend._team_worker_system = worker_systems[name]

            # Per-thread compute access: controlled by config
            orig_allow_compute = getattr(backend, '_allow_compute', True)
            if compute_access:
                backend._allow_compute = compute_access.get(name, True)
            else:
                backend._allow_compute = True

            w = backend.call_worker(session.thread_a_messages,
                                    prev_response_id=session.gpt_worker_prev_id)
            session.gpt_worker_prev_id = w.get("response_id")

            # Restore compute access
            backend._allow_compute = orig_allow_compute

            # Restore
            if orig_worker_system is not None:
                backend._team_worker_system = orig_worker_system

            session.total_input_tokens += w["in_tok"]
            session.total_output_tokens += w["out_tok"]
            session.total_cache_read += w["cache_read"]
            session.total_cache_create += w["cache_create"]
            session.searches += w["searches"]

            worker_text = w["text"].strip() if w["text"] else ""
            if not worker_text:
                worker_text = "(Worker produced empty output.)"
            display = worker_text[:1500]
            if len(worker_text) > 1500:
                display += f"\n  [...{len(worker_text)-1500} more chars...]"
            for line in display.split("\n"):
                print(f"  | {line}")
            print(f"  [{datetime.now().strftime('%H:%M:%S')}] in={w['in_tok']:,} "
                  f"out={w['out_tok']:,} cache={w['cache_read']:,}")

            session.log_to_file(f"\n{worker_text}\n[in={w['in_tok']:,} out={w['out_tok']:,}]")
            session.thread_a_messages.append({"role": "assistant", "content": worker_text})

            if "[DONE]" in worker_text:
                print(f"\n  [*] {name.upper()} DONE at turn {session.turn}")
                alive[name] = False
                session.save()
                save_output(session)
                continue

            # --- Evaluator ---
            ehdr = (f"[{tag}:E] [{datetime.now().strftime('%H:%M:%S')}] "
                    f"{name.upper()} eval turn {session.turn}")
            print(f"\n  {ehdr}")
            session.log_to_file(f"\n{'='*70}\n{ehdr}\n{'='*70}")

            eval_msg = f"Worker output (turn {session.turn}):\n\n{worker_text}"
            if session.research_log:
                eval_msg = (f"Research log so far:\n{session.research_log}"
                            f"\n\n---\n\n{eval_msg}")
            session.thread_b_messages.append({"role": "user", "content": eval_msg})

            e = backend.call_evaluator(session.thread_b_messages,
                                       prev_response_id=session.gpt_eval_prev_id)
            session.gpt_eval_prev_id = e.get("response_id")

            eval_text = e["text"].strip() if e["text"] else ""
            if not eval_text:
                eval_text = "COMMIT\n\n---LOG---\nEvaluator returned empty response."
            session.total_input_tokens += e["in_tok"]
            session.total_output_tokens += e["out_tok"]
            session.total_cache_read += e["cache_read"]
            session.total_cache_create += e["cache_create"]

            for line in eval_text.split("\n"):
                print(f"  | {line}")
            session.log_to_file(f"\n{eval_text}\n[in={e['in_tok']:,} out={e['out_tok']:,}]")
            session.thread_b_messages.append({"role": "assistant", "content": eval_text})

            # Extract log
            if "---LOG---" in eval_text:
                log_part = eval_text.split("---LOG---", 1)[1].strip()
                session.research_log += f"\n[Turn {session.turn}] {log_part}"

            eval_directive = (eval_text.split("---LOG---")[0].strip()
                              if "---LOG---" in eval_text else eval_text.strip())

            # --- Narrator ---
            narrator_text = backend.call_narrator(
                worker_text, eval_text, session.goal, session.turn)
            cost = session.estimate_cost()
            with open(session.briefing_file, "a") as f:
                f.write(f"### Round {session.turn}  "
                        f"({datetime.now().strftime('%H:%M')})\n\n"
                        f"{narrator_text}\n\n"
                        f"**Cost so far: ${cost:.2f}** | "
                        f"Tokens: {session.total_input_tokens:,} in / "
                        f"{session.total_output_tokens:,} out\n\n")
            print(f"\n  [N] {narrator_text[:150]}")

            # Log to team brief
            with open(team_brief_file, "a") as f:
                f.write(f"### {name.upper()} Round {session.turn}\n\n"
                        f"{narrator_text}\n\n")

            # Check for ABORT
            if "[STOP]" in eval_text:
                print(f"\n  [!] {name.upper()} ABORTED at turn {session.turn} | ${cost:.4f}")
                alive[name] = False
                session.save()
                save_output(session)
                continue

            # --- Feed back to worker with optional coordinator injection ---
            feedback = f"EVALUATOR FEEDBACK (turn {session.turn}):\n{eval_directive}"
            if coord_injections[name]:
                feedback += (f"\n\nCOORDINATOR NOTE (from other threads):\n"
                             f"{coord_injections[name]}")
                coord_injections[name] = ""  # consume injection
            feedback += "\n\nContinue. Do one meaningful step."
            session.thread_a_messages.append({"role": "user", "content": feedback})

            session.save()
            total_cost = sum(s.estimate_cost() for s in sessions.values())
            print(f"\n  [$] {name.upper()}: ${cost:.4f} | "
                  f"Team total: ${total_cost:.4f}")

    # --- Final summary ---
    total_cost = sum(s.estimate_cost() for s in sessions.values())
    print(f"\n{'='*70}")
    print(f"  TEAM RUN COMPLETE | Total cost: ${total_cost:.4f}")
    print(f"{'='*70}")

    with open(team_brief_file, "a") as f:
        f.write(f"\n---\n\n## Final Summary\n\n"
                f"**Total cost:** ${total_cost:.4f}\n\n")
        for name in thread_names:
            s = sessions[name]
            status = "DONE" if not alive[name] else f"Turn {s.turn}"
            f.write(f"- **{name.upper()}**: {status}, ${s.estimate_cost():.4f}, "
                    f"{s.turn} turns\n")

    for name in thread_names:
        sessions[name].save()
        save_output(sessions[name])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="math-agent -- Dual-arch research agent")
    parser.add_argument("--prove", type=str,
                        help="Path to file containing the research goal/problem statement")
    parser.add_argument("--arch", choices=["claude", "gpt", "gemini", "all", "team"], default="claude",
                        help="Backend architecture (default: claude). 'all' runs all three. 'team' runs 3 specialized GPT threads.")
    parser.add_argument("--seed", type=str, help="Path to seed document with detailed context")
    parser.add_argument("--max-turns", type=int, default=20)
    parser.add_argument("--budget", type=float, default=10.0,
                        help="Total budget in dollars (split across architectures in 'all' mode, default: 10)")
    parser.add_argument("--resume", type=str, help="Resume from session file")
    parser.add_argument("--threads", type=str, help="Path to JSON thread config file")
    parser.add_argument("--model", type=str, help="Override worker model")
    parser.add_argument("--eval-model", type=str, help="Override evaluator model")
    parser.add_argument("--compact-at", type=int, default=80000,
                        help="Compaction threshold in tokens (default: 80000)")
    parser.add_argument("--cortex", action="store_true",
                        help="Enable Cortex memory (uses autonomous.db on port 8082, isolated from personal cortex)")
    parser.add_argument("--cortex-task", type=str, default=None,
                        help="Task namespace for Cortex tags (e.g., 'eta-rank4'). Filters recall + prefixes stores.")
    args = parser.parse_args()

    # --- Cortex opt-in ---
    # Cortex opt-in: mutate module globals directly
    if args.cortex:
        globals()['CORTEX_ENABLED'] = True
        globals()['CORTEX_TASK'] = args.cortex_task
        print(f"  [cortex] ENABLED — autonomous.db (port 8082)")
        if CORTEX_TASK:
            print(f"  [cortex] Task namespace: {CORTEX_TASK}")

    if args.resume:
        session = Session.load(args.resume)
        arch = session.arch
        archs = [arch]
    elif args.prove:
        if not os.path.isfile(args.prove):
            parser.error(f"File not found: {args.prove}")
        with open(args.prove) as f:
            goal = f.read().strip()

        seed_text = ""
        if args.seed:
            if not os.path.isfile(args.seed):
                parser.error(f"Seed not found: {args.seed}")
            with open(args.seed) as f:
                seed_text = f.read()
        if args.arch == "all":
            archs = ["claude", "gpt", "gemini"]
        elif args.arch == "team":
            archs = ["team"]
        else:
            archs = [args.arch]
        # For resume path, session is already set above
        session = None
    else:
        parser.error("Provide --prove <file> or --resume <session>")

    def make_backend(arch_name):
        if arch_name == "claude":
            wm = args.model or "claude-opus-4-6"
            em = args.eval_model or "claude-opus-4-6"
            nm = "claude-haiku-4-5-20251001"
            return ClaudeBackend(worker_model=wm, eval_model=em,
                                narrator_model=nm, enable_thinking=True,
                                compact_threshold=args.compact_at)
        elif arch_name == "gpt":
            wm = args.model or "gpt-5.2"
            em = args.eval_model or "gpt-5.2"
            nm = "gpt-5-mini"
            return GPTBackend(worker_model=wm, eval_model=em,
                              narrator_model=nm)
        else:  # gemini
            wm = args.model or "gemini-2.5-pro"
            em = args.eval_model or "gemini-2.5-flash"
            nm = "gemini-2.5-flash-lite"
            return GeminiBackend(worker_model=wm, eval_model=em,
                                narrator_model=nm,
                                compact_threshold=args.compact_at)

    # --- Team mode: special handling ---
    if archs == ["team"]:
        backend = make_backend("gpt")
        thread_config = None
        if args.threads:
            with open(args.threads) as f:
                thread_config = json.load(f)
        try:
            run_team(goal, seed_text, backend,
                     max_turns_per_thread=args.max_turns,
                     max_cost=args.budget,
                     coord_interval=2,
                     thread_config=thread_config)
        except KeyboardInterrupt:
            print("  [!] Team run interrupted.")
        except Exception as e:
            import traceback
            traceback.print_exc()
        sys.exit(0)

    for arch in archs:
        per_arch_cost = args.budget / len(archs)
        if session and len(archs) == 1:
            # Resuming a single session
            s = session
        else:
            s = Session(goal, seed=seed_text, arch=arch)

        backend = make_backend(arch)

        if len(archs) > 1:
            with open(s.log_file, "a") as lf:
                lf.write(f"\n{'#'*70}\n  STARTING RUN: --arch {arch}\n{'#'*70}\n")

        try:
            run(s, backend, max_turns=args.max_turns, max_cost=per_arch_cost)
        except KeyboardInterrupt:
            s.save()
            break
        except Exception as e:
            # Log error to log file
            with open(s.log_file, "a") as lf:
                lf.write(f"\n{'='*70}\n")
                lf.write(f"  [X] Error ({arch}) at turn {s.turn} | ${s.estimate_cost():.4f}\n")
                lf.write(f"  {e}\n")
                lf.write(f"{'='*70}\n")
                import traceback
                traceback.print_exc(file=lf)
            s.save()
            if len(archs) > 1:
                continue
            raise

    # Summary table for --arch all
    if len(archs) > 1:
        import glob
        summary_file = "comparison-summary"
        with open(summary_file, "w") as sf:
            sf.write("COMPARISON SUMMARY\n" + "="*70 + "\n")
            for bf in sorted(glob.glob("*-brief")):
                sf.write(f"  Briefing: {bf}\n")
