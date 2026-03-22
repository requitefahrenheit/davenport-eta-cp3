# Task: Fill Three Lean 4 Sorrys in UpperBound.lean

You have access to the AWS instance via the dev MCP tools. The Lean project is at ~/lean_work/ on AWS.

IMPORTANT: Use the aws-dev tools (dev_run, dev_read_file, dev_write_file) to access AWS. The lean/lake commands are at ~/.elan/bin/ on AWS. Always prefix commands with: export PATH=$HOME/.elan/bin:$PATH

The file ~/lean_work/UpperBound.lean has THREE sorrys to fill. The math is done — these are Lean API plumbing, not proof gaps. The helper modules (Involution.lean, Newton.lean, ModArith.lean, Fourier.lean, PrimRoot.lean, PinningStep.lean) are all sorry-free.

## Sorry 1: fourier_subst (line ~107)

```lean
lemma fourier_subst (x : ZMod p) (hx : x ≠ 0) (chi : MulChar (ZMod p) ℂ) :
    ∑ mu : (ZMod p)ˣ, (ZMod.val (mu.val * x) : ℂ) * chi (mu⁻¹ : (ZMod p)ˣ) =
    chi x * charWeightSum chi := by sorry
```

This is a Finset reindexing lemma. The key steps:
1. Substitute nu = mu * (IsUnit.unit (isUnit_of_ne_zero hx)) in the sum
2. Use Units.val_mul and the fact that multiplication by a unit permutes (ZMod p)ˣ
3. Factor out chi(x) using MulChar multiplicativity: chi(mu⁻¹ * x⁻¹) = chi(mu⁻¹) * chi(x⁻¹)
4. Use chi(x) * chi(x⁻¹) = 1

Key Mathlib lemmas: Finset.sum_bijective, MulChar.map_mul, Units.val_mul, ZMod.unitOfCoprime

## Sorry 2: chars_pin_sum (line ~112)

```lean
lemma chars_pin_sum ... :
    chi a + chi b + chi c = chi (a+b+c) := by sorry
```

The proof uses:
1. h_pin tells us f3(mu) = p + modRep(mu*s) for all mu (where s = a+b+c)
2. Multiply both sides by chi(mu⁻¹) and sum over mu
3. LHS becomes chi(a)*W + chi(b)*W + chi(c)*W where W = charWeightSum(chi)
4. RHS becomes (p-1)*p + chi(s)*W (the p*(p-1) term vanishes mod character orthogonality)
5. bernoulli_nonvanishing gives W ≠ 0, so divide

Key: use fourier_subst (sorry 1) for the substitution step. Use MulChar.sum_eq_zero_of_ne_one for the orthogonality.

## Sorry 3: pinning_step (line ~134)

```lean
lemma pinning_step (hp2 : p ≠ 2) ... (h_all_ge : ∀ mu, mu≠0 → p ≤ f3 a b c mu) : False
```

This chains everything together:
1. From h_all_ge + involution_identity: f3(mu) = p + modRep(mu*s) for all mu≠0
2. From chars_pin_sum: chi(a) + chi(b) + chi(c) = chi(s) for all odd nontrivial chi
3. Extract a primitive root g of (ZMod p)ˣ (use IsCyclic + Fintype.card)
4. Define omega = exp(2πi/(p-1)), set z_i = omega^(log_g(a_i))
5. The character identity becomes z1^m + z2^m + z3^m = s^m for all odd m
6. Apply roots_of_unity_odd_power_sum → antipodal pair
7. Antipodal pair contradicts hab/hac/hbc

Key Mathlib: IsCyclic, ZMod.IsPrimitiveRoot, orderOf_eq_card_of_forall_mem_zpowers
Also use the helper modules: PrimRoot.lean sets up the primitive root, Fourier.lean has character sum manipulation.

READ the helper modules first:
```
cat ~/lean_work/UpperBound/PrimRoot.lean
cat ~/lean_work/UpperBound/Fourier.lean  
cat ~/lean_work/UpperBound/PinningStep.lean
```

These contain the heavy lifting. Your job is to wire them into the top-level file.

## Build and test

```bash
export PATH=$HOME/.elan/bin:$PATH
cd ~/lean_work
lake build UpperBound 2>&1 | tail -20
```

Goal: zero sorrys, zero errors, clean build. The axiom bernoulli_nonvanishing stays (it's Dirichlet's theorem).

Start with sorry 1 (fourier_subst) — it's the most self-contained. Then sorry 2 which depends on sorry 1. Then sorry 3 which depends on sorry 2.
