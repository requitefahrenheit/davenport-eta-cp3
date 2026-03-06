/-
  DavenportAll.lean — Complete proof in one file

  THEOREM (Proposition 6):
  For every odd prime p >= 3 and every nonzero c in ker(M) subset F_p^8,
  the lift-weight w(c) >= p + 1.

  This implies eta(C_p^3) >= 8(p-1)+1 for all odd primes p.
-/
import Mathlib

namespace Davenport

/-! ===================================================================
    S1  Definitions  (from Defs.lean)
    =================================================================== -/

structure Params (p : ℤ) where
  t₀ : ℤ
  t₁ : ℤ
  t₂ : ℤ
  t₃ : ℤ
  t₄ : ℤ
  h₀_lo : 0 ≤ t₀
  h₀_hi : t₀ ≤ p - 1
  h₁_lo : 0 ≤ t₁
  h₁_hi : t₁ ≤ p - 1
  h₂_lo : 0 ≤ t₂
  h₂_hi : t₂ ≤ p - 1
  h₃_lo : 0 ≤ t₃
  h₃_hi : t₃ ≤ p - 1
  h₄_lo : 0 ≤ t₄
  h₄_hi : t₄ ≤ p - 1

section CoreDefs
variable {p : ℤ} (t : Params p)

def A : ℤ := t.t₀ + t.t₁ + 2 * t.t₃ + t.t₄
def B : ℤ := t.t₀ + t.t₂ + t.t₃ + 2 * t.t₄
def S₄ : ℤ := t.t₁ + t.t₂ + t.t₃ + t.t₄
def T : ℤ := t.t₃ + t.t₄
def R : ℤ := t.t₀ + T t
def c₀int : ℤ := t.t₀ - t.t₁ - t.t₂ + T t
def isNonzero : Prop :=
  t.t₀ ≠ 0 ∨ t.t₁ ≠ 0 ∨ t.t₂ ≠ 0 ∨ t.t₃ ≠ 0 ∨ t.t₄ ≠ 0

end CoreDefs

/-! ===================================================================
    S2  Identities  (from Identities.lean)
    =================================================================== -/

variable {p : ℤ}

section Identities
variable (t : Params p)

theorem A_eq_R_add : A t = R t + t.t₁ + t.t₃ := by unfold A R T; ring
theorem B_eq_R_add : B t = R t + t.t₂ + t.t₄ := by unfold B R T; ring
theorem c₀int_eq_R_sub : c₀int t = R t - (t.t₁ + t.t₂) := by unfold c₀int R T; ring
theorem A_add_B : A t + B t = 2 * R t + S₄ t := by unfold A B R S₄ T; ring
theorem A_eq_t₀_S₄_t₃_sub_t₂ : A t = t.t₀ + S₄ t + t.t₃ - t.t₂ := by unfold A S₄; ring
theorem B_eq_t₀_S₄_t₄_sub_t₁ : B t = t.t₀ + S₄ t + t.t₄ - t.t₁ := by unfold B S₄; ring
theorem S₄_eq_T_add : S₄ t = t.t₁ + t.t₂ + T t := by unfold S₄ T; ring
theorem R_eq_t₀_T : R t = t.t₀ + T t := by unfold R; ring

theorem A_nonneg : 0 ≤ A t := by unfold A; linarith [t.h₀_lo, t.h₁_lo, t.h₃_lo, t.h₄_lo]
theorem B_nonneg : 0 ≤ B t := by unfold B; linarith [t.h₀_lo, t.h₂_lo, t.h₃_lo, t.h₄_lo]
theorem S₄_nonneg : 0 ≤ S₄ t := by unfold S₄; linarith [t.h₁_lo, t.h₂_lo, t.h₃_lo, t.h₄_lo]
theorem T_nonneg : 0 ≤ T t := by unfold T; linarith [t.h₃_lo, t.h₄_lo]
theorem R_nonneg : 0 ≤ R t := by unfold R T; linarith [t.h₀_lo, t.h₃_lo, t.h₄_lo]

theorem S₄_le (hp : 3 ≤ p) : S₄ t ≤ 4 * (p - 1) := by
  unfold S₄; linarith [t.h₁_hi, t.h₂_hi, t.h₃_hi, t.h₄_hi]
theorem T_le (hp : 3 ≤ p) : T t ≤ 2 * (p - 1) := by
  unfold T; linarith [t.h₃_hi, t.h₄_hi]
theorem R_le (hp : 3 ≤ p) : R t ≤ 3 * (p - 1) := by
  unfold R T; linarith [t.h₀_hi, t.h₃_hi, t.h₄_hi]

theorem A_ge_S₄_sub : A t ≥ S₄ t - (p - 1) := by
  have := A_eq_t₀_S₄_t₃_sub_t₂ t; linarith [t.h₀_lo, t.h₃_lo, t.h₂_hi]
theorem B_ge_S₄_sub : B t ≥ S₄ t - (p - 1) := by
  have := B_eq_t₀_S₄_t₄_sub_t₁ t; linarith [t.h₀_lo, t.h₄_lo, t.h₁_hi]

end Identities

/-! ===================================================================
    S3  Weight formula  (from WeightFormula.lean)
    =================================================================== -/

theorem weight_identity (t : Params p) (n₀ n₁ n₂ : ℤ) :
    (t.t₀ + S₄ t) + (p * n₁ - A t) + (p * n₂ - B t) + (c₀int t + p * n₀)
    = p * (n₀ + n₁ + n₂) - S₄ t := by
  have hAB := A_add_B t; have hc0 := c₀int_eq_R_sub t
  have hR := R_eq_t₀_T t; have hS := S₄_eq_T_add t
  unfold A B c₀int R S₄ T at *; linarith

/-! ===================================================================
    S4  N >= 2  (from NGeq2.lean)
    =================================================================== -/

theorem n₁_pos_of_A_pos (t : Params p) (hp : 0 < p)
    (n₁ : ℤ) (h1 : 0 ≤ p * n₁ - A t) (hA : 0 < A t) :
    1 ≤ n₁ := by
  by_contra h; push_neg at h
  have : n₁ ≤ 0 := by omega
  nlinarith

theorem n₂_pos_of_B_pos (t : Params p) (hp : 0 < p)
    (n₂ : ℤ) (h1 : 0 ≤ p * n₂ - B t) (hB : 0 < B t) :
    1 ≤ n₂ := by
  by_contra h; push_neg at h
  have : n₂ ≤ 0 := by omega
  nlinarith

theorem impossible_neg1_1_1 (t : Params p) (_ : 3 ≤ p)
    (_ : 1 ≤ t.t₀) (hA_le : A t ≤ p) (hB_le : B t ≤ p)
    (hc₀_ge : p ≤ c₀int t) : False := by
  have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by
    rw [c₀int_eq_R_sub] at hc₀_ge; linarith
  have h1 : t.t₁ + t.t₃ ≤ -(t.t₁ + t.t₂) := by
    have := A_eq_R_add t; linarith
  have h_t₁ : t.t₁ = 0 := by linarith [t.h₁_lo, t.h₃_lo, t.h₂_lo]
  have h_t₃ : t.t₃ = 0 := by linarith [t.h₁_lo, t.h₃_lo, t.h₂_lo]
  have h2 : t.t₂ + t.t₄ ≤ -t.t₂ := by
    have := B_eq_R_add t; rw [h_t₁] at hR_ge; linarith
  have h_t₂ : t.t₂ = 0 := by linarith [t.h₂_lo, t.h₄_lo]
  have h_t₄ : t.t₄ = 0 := by linarith [t.h₂_lo, t.h₄_lo]
  have : c₀int t = t.t₀ := by unfold c₀int T; rw [h_t₁, h_t₂, h_t₃, h_t₄]; ring
  linarith [t.h₀_hi]

theorem N_ge_two (t : Params p) (hp : 3 ≤ p) (hne : isNonzero t)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p) :
    2 ≤ n₀ + n₁ + n₂ := by
  have hp_pos : (0 : ℤ) < p := by linarith
  have hn₁_nn : 0 ≤ n₁ := by have := A_nonneg t; nlinarith
  have hn₂_nn : 0 ≤ n₂ := by have := B_nonneg t; nlinarith
  have ht₀_lo := t.h₀_lo; have ht₀_hi := t.h₀_hi
  have ht₁_lo := t.h₁_lo; have ht₁_hi := t.h₁_hi
  have ht₂_lo := t.h₂_lo; have ht₂_hi := t.h₂_hi
  have ht₃_lo := t.h₃_lo; have ht₃_hi := t.h₃_hi
  have ht₄_lo := t.h₄_lo; have ht₄_hi := t.h₄_hi
  by_cases ht₀ : t.t₀ = 0
  · by_cases hT : T t = 0
    · have h_t₃ : t.t₃ = 0 := by unfold T at hT; linarith
      have h_t₄ : t.t₄ = 0 := by unfold T at hT; linarith
      have hA_eq : A t = t.t₁ := by unfold A; rw [ht₀, h_t₃, h_t₄]; ring
      have hB_eq : B t = t.t₂ := by unfold B; rw [ht₀, h_t₃, h_t₄]; ring
      have hc₀_eq : c₀int t = -(t.t₁ + t.t₂) := by
        unfold c₀int T; rw [ht₀, h_t₃, h_t₄]; ring
      have hne12 : 0 < t.t₁ ∨ 0 < t.t₂ := by
        unfold isNonzero at hne
        rcases hne with h | h | h | h | h
        · exact absurd ht₀ h
        · left; omega
        · right; omega
        · exact absurd h_t₃ h
        · exact absurd h_t₄ h
      have hc₀_neg : c₀int t ≤ -1 := by
        rw [hc₀_eq]; rcases hne12 with h | h <;> linarith
      have hn₀_pos : 1 ≤ n₀ := by nlinarith
      rcases hne12 with h | h
      · have : 0 < A t := by rw [hA_eq]; linarith
        have := n₁_pos_of_A_pos t hp_pos n₁ hw1 this
        linarith
      · have : 0 < B t := by rw [hB_eq]; linarith
        have := n₂_pos_of_B_pos t hp_pos n₂ hw3 this
        linarith
    · have hT_pos : 0 < T t := by have := T_nonneg t; omega
      have hR_eq : R t = T t := by unfold R; rw [ht₀]; ring
      have hA_pos : 0 < A t := by rw [A_eq_R_add]; linarith
      have hn₁_pos := n₁_pos_of_A_pos t hp_pos n₁ hw1 hA_pos
      have hB_pos : 0 < B t := by rw [B_eq_R_add]; linarith
      have hn₂_pos := n₂_pos_of_B_pos t hp_pos n₂ hw3 hB_pos
      by_cases hc₀ : c₀int t < p
      · have : 0 ≤ n₀ := by nlinarith
        linarith
      · push_neg at hc₀
        have hT_ge_p : T t ≥ p := by
          rw [c₀int_eq_R_sub, hR_eq] at hc₀; linarith
        have : 0 < t.t₃ := by unfold T at hT_ge_p; linarith
        have : 0 < t.t₄ := by unfold T at hT_ge_p; linarith
        have : A t ≥ p + 1 := by rw [A_eq_R_add, hR_eq]; linarith
        have hn₁_ge2 : 2 ≤ n₁ := by nlinarith
        have : B t ≥ p + 1 := by rw [B_eq_R_add, hR_eq]; linarith
        have hn₂_ge2 : 2 ≤ n₂ := by nlinarith
        have : c₀int t < 2 * p := by
          rw [c₀int_eq_R_sub, hR_eq]; have := T_le t (by linarith : 3 ≤ p); linarith
        have : -1 ≤ n₀ := by nlinarith
        linarith
  · push_neg at ht₀
    have ht₀_pos : 1 ≤ t.t₀ := by omega
    have hA_pos : 0 < A t := by rw [A_eq_R_add]; unfold R T; linarith
    have hB_pos : 0 < B t := by rw [B_eq_R_add]; unfold R T; linarith
    have hn₁_pos := n₁_pos_of_A_pos t hp_pos n₁ hw1 hA_pos
    have hn₂_pos := n₂_pos_of_B_pos t hp_pos n₂ hw3 hB_pos
    by_cases hn₀ : 0 ≤ n₀
    · linarith
    · push_neg at hn₀
      have hc₀_ge_p : p ≤ c₀int t := by nlinarith
      by_cases hn₀_eq : n₀ = -1
      · by_cases hn₁₂ : n₁ + n₂ ≥ 3
        · rw [hn₀_eq]; linarith
        · push_neg at hn₁₂
          have : n₁ = 1 := by omega
          have : n₂ = 1 := by omega
          have hA_le : A t ≤ p := by nlinarith
          have hB_le : B t ≤ p := by nlinarith
          exact absurd (impossible_neg1_1_1 t hp ht₀_pos hA_le hB_le hc₀_ge_p) not_false
      · have hn₀_le : n₀ ≤ -2 := by omega
        have hc₀_ge_2p : c₀int t ≥ 2 * p := by nlinarith
        have hR_ge : R t ≥ 2 * p := by
          have h := hc₀_ge_2p; rw [c₀int_eq_R_sub] at h; linarith
        have hT_big : T t ≥ p + 1 := by rw [R_eq_t₀_T] at hR_ge; linarith
        have : t.t₃ ≥ 2 := by unfold T at hT_big; linarith
        have : t.t₄ ≥ 2 := by unfold T at hT_big; linarith
        have : A t ≥ 2 * p + 2 := by rw [A_eq_R_add]; linarith [R_nonneg t]
        have : n₁ ≥ 3 := by nlinarith
        have : B t ≥ 2 * p + 2 := by rw [B_eq_R_add]; linarith [R_nonneg t]
        have : n₂ ≥ 3 := by nlinarith
        have h_n₁ : n₁ ≥ 3 := ‹n₁ ≥ 3›
        have h_n₂ : n₂ ≥ 3 := ‹n₂ ≥ 3›
        have hn₀_ge : n₀ ≥ -2 := by
          by_contra h_neg
          push_neg at h_neg
          have h3 : n₀ ≤ -3 := by omega
          have hc₀_le : c₀int t ≤ R t := by
            rw [c₀int_eq_R_sub]; linarith [t.h₁_lo, t.h₂_lo]
          have hR_le := R_le t (show 3 ≤ p from hp)
          have h_pn₀ : p * n₀ ≥ -(3 * (p - 1)) := by linarith [hw5]
          nlinarith [hp_pos]
        linarith only [hn₀_ge, h_n₁, h_n₂]

/-! ===================================================================
    S5  Case N = 4  (from CaseN4.lean)
    =================================================================== -/

theorem case_N4 (t : Params p) (hp : 3 ≤ p)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p)
    (hN : n₀ + n₁ + n₂ = 4) (hS : S₄ t ≥ 3 * p) : False := by
  have hA_ge := A_ge_S₄_sub t
  have hA_big : A t ≥ 2 * p + 1 := by linarith
  have hn₁ : 3 ≤ n₁ := by nlinarith
  have hB_ge := B_ge_S₄_sub t
  have hB_big : B t ≥ 2 * p + 1 := by linarith
  have hn₂ : 3 ≤ n₂ := by nlinarith
  have hn₀ : n₀ ≤ -2 := by omega
  have hc₀_ge : c₀int t ≥ 2 * p := by nlinarith
  have hT_le := T_le t hp
  have hS₄_eq := S₄_eq_T_add t
  have h_t₁t₂ : t.t₁ + t.t₂ ≥ p + 2 := by linarith
  have hR_le := R_le t hp
  have hc₀_le : c₀int t ≤ 2 * p - 5 := by
    rw [c₀int_eq_R_sub]; linarith
  linarith

theorem weight_bound_N4 (t : Params p) (hp : 3 ≤ p)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p)
    (hN : n₀ + n₁ + n₂ = 4) : p * 4 - S₄ t ≥ p + 1 := by
  by_contra h
  push_neg at h
  have hS : S₄ t ≥ 3 * p := by omega
  exact case_N4 t hp n₀ n₁ n₂ hw1 hw2 hw3 hw4 hw5 hw6 hN hS

/-! ===================================================================
    S6  Case N = 3  (from CaseN3.lean)
    =================================================================== -/

theorem case_N3_111 (t : Params p) (_ : 3 ≤ p)
    (hA_le : A t ≤ p) (hB_le : B t ≤ p) (hS : S₄ t ≥ 2 * p) : False := by
  have hAB := A_add_B t
  have hR := R_nonneg t
  have : R t ≤ 0 := by linarith
  have hR_eq : R t = 0 := by linarith
  have ht₀ : t.t₀ = 0 := by rw [R_eq_t₀_T] at hR_eq; linarith [t.h₀_lo, T_nonneg t]
  have hT : T t = 0 := by rw [R_eq_t₀_T] at hR_eq; linarith [t.h₀_lo, T_nonneg t]
  have : S₄ t = t.t₁ + t.t₂ := by rw [S₄_eq_T_add, hT]; ring
  linarith [t.h₁_hi, t.h₂_hi]

theorem case_N3_021 (t : Params p) (_ : 3 ≤ p)
    (hB_le : B t ≤ p) (hc₀_ge : 0 ≤ c₀int t) (hS : S₄ t ≥ 2 * p) : False := by
  have hR_ge : R t ≥ S₄ t - T t := by
    rw [c₀int_eq_R_sub] at hc₀_ge; rw [S₄_eq_T_add]; linarith
  have h_sum : t.t₀ + 2 * T t ≥ 2 * p := by rw [R_eq_t₀_T] at hR_ge; linarith
  have hR_t₄ : R t + t.t₄ ≤ p := by have := B_eq_R_add t; linarith [t.h₂_lo]
  have key : t.t₀ + 2 * T t = (R t + t.t₄) + t.t₃ := by
    rw [R_eq_t₀_T]; unfold T; ring
  linarith [t.h₃_hi]

theorem case_N3_012 (t : Params p) (_ : 3 ≤ p)
    (hA_le : A t ≤ p) (hc₀_ge : 0 ≤ c₀int t) (hS : S₄ t ≥ 2 * p) : False := by
  have hR_ge : R t ≥ S₄ t - T t := by
    rw [c₀int_eq_R_sub] at hc₀_ge; rw [S₄_eq_T_add]; linarith
  have h_sum : t.t₀ + 2 * T t ≥ 2 * p := by rw [R_eq_t₀_T] at hR_ge; linarith
  have hR_t₃ : R t + t.t₃ ≤ p := by have := A_eq_R_add t; linarith [t.h₁_lo]
  have key : t.t₀ + 2 * T t = (R t + t.t₃) + t.t₄ := by
    rw [R_eq_t₀_T]; unfold T; ring
  linarith [t.h₄_hi]

theorem case_N3_neg122_full (t : Params p) (hp : 3 ≤ p)
    (hA_le : A t ≤ 2 * p) (hB_le : B t ≤ 2 * p)
    (hc₀_ge : p ≤ c₀int t) (hS : S₄ t ≥ 2 * p) : False := by
  have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by rw [c₀int_eq_R_sub] at hc₀_ge; linarith
  by_cases h12 : t.t₁ + t.t₂ ≥ 1
  · have hAB := A_add_B t
    have : S₄ t ≤ 4 * p - 2 * R t := by linarith
    linarith
  · push_neg at h12
    have h_t₁ : t.t₁ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
    have h_t₂ : t.t₂ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
    have : S₄ t = T t := by rw [S₄_eq_T_add, h_t₁, h_t₂]; ring
    linarith [T_le t hp]

theorem weight_bound_N3 (t : Params p) (hp : 3 ≤ p)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p)
    (hN : n₀ + n₁ + n₂ = 3) (hn₀_ge : -1 ≤ n₀) :
    p * 3 - S₄ t ≥ p + 1 := by
  by_contra h; push_neg at h
  have hS : S₄ t ≥ 2 * p := by omega
  have hp_pos : (0 : ℤ) < p := by linarith
  have hn₁_nn : 0 ≤ n₁ := by have := A_nonneg t; nlinarith
  have hn₂_nn : 0 ≤ n₂ := by have := B_nonneg t; nlinarith
  have hn₁_pos : 1 ≤ n₁ := n₁_pos_of_A_pos t hp_pos n₁ hw1 (by linarith [A_ge_S₄_sub t])
  have hn₂_pos : 1 ≤ n₂ := n₂_pos_of_B_pos t hp_pos n₂ hw3 (by linarith [B_ge_S₄_sub t])
  rcases (show n₀ = -1 ∨ n₀ = 0 ∨ n₀ = 1 by omega) with rfl | rfl | rfl
  · -- n₀ = -1
    have hc₀_ge_p : p ≤ c₀int t := by nlinarith
    rcases (show (n₁ = 2 ∧ n₂ = 2) ∨ (n₁ = 1 ∧ n₂ = 3) ∨ (n₁ = 3 ∧ n₂ = 1)
              ∨ n₁ + n₂ > 4 ∨ n₁ = 0 ∨ n₂ = 0 by omega)
      with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | h | h | h
    · exact case_N3_neg122_full t hp (by nlinarith) (by nlinarith) hc₀_ge_p hS
    · have hAB := A_add_B t
      have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by rw [c₀int_eq_R_sub] at hc₀_ge_p; linarith
      have hS₄_le : S₄ t ≤ 4 * p - 2 * R t := by linarith
      have h_t₁ : t.t₁ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
      have h_t₂ : t.t₂ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
      have : S₄ t = T t := by rw [S₄_eq_T_add, h_t₁, h_t₂]; ring
      linarith [T_le t hp]
    · have hAB := A_add_B t
      have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by rw [c₀int_eq_R_sub] at hc₀_ge_p; linarith
      have hS₄_le : S₄ t ≤ 4 * p - 2 * R t := by linarith
      have h_t₁ : t.t₁ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
      have h_t₂ : t.t₂ = 0 := by linarith [t.h₁_lo, t.h₂_lo]
      have : S₄ t = T t := by rw [S₄_eq_T_add, h_t₁, h_t₂]; ring
      linarith [T_le t hp]
    · omega
    · omega
    · omega
  · -- n₀ = 0
    have hc₀_lo : 0 ≤ c₀int t := by linarith
    rcases (show (n₁ = 2 ∧ n₂ = 1) ∨ (n₁ = 1 ∧ n₂ = 2) ∨ n₁ = 0 ∨ n₂ = 0 by omega)
      with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | h | h
    · exact case_N3_021 t hp (by nlinarith) hc₀_lo hS
    · exact case_N3_012 t hp (by nlinarith) hc₀_lo hS
    · omega
    · omega
  · -- n₀ = 1: n₁ = n₂ = 1
    have : n₁ = 1 := by omega
    have : n₂ = 1 := by omega
    subst_vars
    exact case_N3_111 t hp (by linarith) (by linarith) hS

/-! ===================================================================
    S7  Case N = 2  (from CaseN2.lean)
    =================================================================== -/

theorem case_N2_011 (t : Params p) (hp : 3 ≤ p) (hodd : p % 2 = 1)
    (hA_le : A t ≤ p) (hB_le : B t ≤ p)
    (hc₀_lo : 0 ≤ c₀int t) (hS : S₄ t ≥ p) : False := by
  have hAB := A_add_B t
  have h2R_le : 2 * R t ≤ p := by linarith
  have hR_ge : R t ≥ S₄ t - T t := by
    rw [c₀int_eq_R_sub] at hc₀_lo; rw [S₄_eq_T_add]; linarith
  have hRT : R t + T t ≥ p := by linarith
  have h2T_ge : 2 * T t ≥ p := by linarith
  have ht₀_le : t.t₀ ≤ 0 := by rw [R_eq_t₀_T] at h2R_le; linarith
  have ht₀_eq : t.t₀ = 0 := by linarith [t.h₀_lo]
  have hR_T : R t = T t := by unfold R; linarith
  have h2T_le : 2 * T t ≤ p := by linarith
  have h2T_eq : 2 * T t = p := by omega
  have : (2 * T t) % 2 = 0 := by omega
  rw [h2T_eq] at this; omega

theorem case_N2_neg121 (t : Params p) (hp : 3 ≤ p)
    (hA_le : A t ≤ 2 * p) (hB_le : B t ≤ p)
    (hc₀_ge : p ≤ c₀int t) (hS : S₄ t ≥ p) : False := by
  have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by rw [c₀int_eq_R_sub] at hc₀_ge; linarith
  have : t.t₂ + t.t₄ ≤ 0 := by
    have := B_eq_R_add t; linarith [t.h₁_lo, t.h₂_lo]
  have h_t₂ : t.t₂ = 0 := by linarith [t.h₂_lo, t.h₄_lo]
  have h_t₄ : t.t₄ = 0 := by linarith [t.h₂_lo, t.h₄_lo]
  have hT_eq : T t = t.t₃ := by unfold T; linarith
  have hA_ge : A t ≥ p + 2 * t.t₁ + t.t₃ := by
    have := A_eq_R_add t; linarith
  have h_bound : 2 * t.t₁ + t.t₃ ≤ p := by linarith
  have hS₄_eq : S₄ t = t.t₁ + t.t₃ := by rw [S₄_eq_T_add, h_t₂, hT_eq]; ring
  have : t.t₃ ≥ p - t.t₁ := by linarith
  have : t.t₁ = 0 := by linarith [t.h₁_lo]
  linarith [t.h₃_hi]

theorem case_N2_neg112 (t : Params p) (hp : 3 ≤ p)
    (hA_le : A t ≤ p) (hB_le : B t ≤ 2 * p)
    (hc₀_ge : p ≤ c₀int t) (hS : S₄ t ≥ p) : False := by
  have hR_ge : R t ≥ p + t.t₁ + t.t₂ := by rw [c₀int_eq_R_sub] at hc₀_ge; linarith
  have : t.t₁ + t.t₃ ≤ 0 := by
    have := A_eq_R_add t; linarith [t.h₁_lo, t.h₂_lo]
  have h_t₁ : t.t₁ = 0 := by linarith [t.h₁_lo, t.h₃_lo]
  have h_t₃ : t.t₃ = 0 := by linarith [t.h₁_lo, t.h₃_lo]
  have hT_eq : T t = t.t₄ := by unfold T; linarith
  have hB_ge : B t ≥ p + 2 * t.t₂ + t.t₄ := by
    have := B_eq_R_add t; linarith
  have h_bound : 2 * t.t₂ + t.t₄ ≤ p := by linarith
  have hS₄_eq : S₄ t = t.t₂ + t.t₄ := by rw [S₄_eq_T_add, h_t₁, hT_eq]; ring
  have : t.t₄ ≥ p - t.t₂ := by linarith
  have : t.t₂ = 0 := by linarith [t.h₂_lo]
  linarith [t.h₄_hi]

theorem weight_bound_N2 (t : Params p) (hp : 3 ≤ p) (hodd : p % 2 = 1)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p)
    (hN : n₀ + n₁ + n₂ = 2) (hn₀_ge : -1 ≤ n₀) :
    p * 2 - S₄ t ≥ p + 1 := by
  by_contra h; push_neg at h
  have hS : S₄ t ≥ p := by omega
  have hp_pos : (0 : ℤ) < p := by linarith
  have hn₁_pos : 1 ≤ n₁ := n₁_pos_of_A_pos t hp_pos n₁ hw1 (by linarith [A_ge_S₄_sub t])
  have hn₂_pos : 1 ≤ n₂ := n₂_pos_of_B_pos t hp_pos n₂ hw3 (by linarith [B_ge_S₄_sub t])
  rcases (show n₀ = 0 ∨ n₀ = -1 by omega) with rfl | rfl
  · have : n₁ = 1 := by omega
    have : n₂ = 1 := by omega
    subst_vars
    exact case_N2_011 t hp hodd (by linarith) (by linarith) (by linarith) hS
  · have hc₀_ge_p : p ≤ c₀int t := by nlinarith
    rcases (show (n₁ = 2 ∧ n₂ = 1) ∨ (n₁ = 1 ∧ n₂ = 2) ∨ n₁ = 0 ∨ n₂ = 0 by omega)
      with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | h | h
    · exact case_N2_neg121 t hp (by nlinarith) (by nlinarith) hc₀_ge_p hS
    · exact case_N2_neg112 t hp (by nlinarith) (by nlinarith) hc₀_ge_p hS
    · omega
    · omega

/-! ===================================================================
    S8  Main theorem  (from Main.lean)
    =================================================================== -/

/-- For all odd primes p and all nonzero kernel parameters with valid
    wrap counts, the weight satisfies w = p*N - S4 >= p + 1.

    This is the core computational content of eta(C_p^3) >= 8(p-1)+1. -/
theorem min_lift_weight (p : ℤ) (hp : 3 ≤ p) (hodd : p % 2 = 1)
    (t : Params p) (hne : isNonzero t)
    (n₀ n₁ n₂ : ℤ)
    (hw1 : 0 ≤ p * n₁ - A t) (hw2 : p * n₁ - A t < p)
    (hw3 : 0 ≤ p * n₂ - B t) (hw4 : p * n₂ - B t < p)
    (hw5 : 0 ≤ c₀int t + p * n₀) (hw6 : c₀int t + p * n₀ < p) :
    p * (n₀ + n₁ + n₂) - S₄ t ≥ p + 1 := by
  have hN_ge := N_ge_two t hp hne n₀ n₁ n₂ hw1 hw2 hw3 hw4 hw5 hw6
  set N := n₀ + n₁ + n₂ with hN_def
  by_cases hN5 : N ≥ 5
  · have := S₄_le t hp; nlinarith
  · push_neg at hN5
    by_cases hN4 : N = 4
    · rw [hN4]
      exact weight_bound_N4 t hp n₀ n₁ n₂
        hw1 hw2 hw3 hw4 hw5 hw6 (by omega)
    · have hN_le3 : N ≤ 3 := by omega
      have hn₀_ge : -1 ≤ n₀ := by
        by_contra h_n₀
        push_neg at h_n₀
        have hn₀_le : n₀ ≤ -2 := by omega
        have hc₀_ge : c₀int t ≥ 2 * p := by nlinarith
        have hR_ge : R t ≥ 2 * p := by
          have h := hc₀_ge; rw [c₀int_eq_R_sub] at h; linarith [t.h₁_lo, t.h₂_lo]
        have hT_big : T t ≥ p + 1 := by
          rw [R_eq_t₀_T] at hR_ge; linarith [t.h₀_hi]
        have : t.t₃ ≥ 2 := by unfold T at hT_big; linarith [t.h₄_hi]
        have : t.t₄ ≥ 2 := by unfold T at hT_big; linarith [t.h₃_hi]
        have : A t ≥ 2 * p + 2 := by rw [A_eq_R_add]; linarith [t.h₁_lo]
        have hn₁_ge3 : n₁ ≥ 3 := by nlinarith
        have : B t ≥ 2 * p + 2 := by rw [B_eq_R_add]; linarith [t.h₂_lo]
        have hn₂_ge3 : n₂ ≥ 3 := by nlinarith
        have hn₀_ge_neg2 : n₀ ≥ -2 := by
          by_contra h2; push_neg at h2
          have h3 : n₀ ≤ -3 := by omega
          have hc₀_le : c₀int t ≤ R t := by
            rw [c₀int_eq_R_sub]; linarith [t.h₁_lo, t.h₂_lo]
          have hR_le := R_le t hp
          have h_pn₀ : p * n₀ ≥ -(3 * (p - 1)) := by linarith [hw5]
          nlinarith [show 0 < p from by linarith]
        linarith only [hn₀_ge_neg2, hn₁_ge3, hn₂_ge3, hN_le3, hN_def]
      interval_cases N
      · exact weight_bound_N2 t hp hodd n₀ n₁ n₂
          hw1 hw2 hw3 hw4 hw5 hw6 hN_def.symm hn₀_ge
      · exact weight_bound_N3 t hp n₀ n₁ n₂
          hw1 hw2 hw3 hw4 hw5 hw6 hN_def.symm hn₀_ge

end Davenport

/-! ===================================================================
    S9  Computational verification for p = 3, 5, 7  (from Verify.lean)
    =================================================================== -/

namespace Davenport.Verify

def liftWeightNat (p : Nat) (t₀ t₁ t₂ t₃ t₄ : Nat) : Nat :=
  let a := t₀ + t₁ + 2 * t₃ + t₄
  let b := t₀ + t₂ + t₃ + 2 * t₄
  let c₀raw : Int := (t₀ : Int) - t₁ - t₂ + t₃ + t₄
  let c₁ := (p - a % p) % p
  let c₂ := (p - b % p) % p
  let c₀ := ((c₀raw % (p : Int) + p) % p).toNat
  t₀ + t₁ + t₂ + t₃ + t₄ + c₀ + c₁ + c₂

def checkAllVectors (p : Nat) : Bool :=
  let range := List.range p
  range.all fun t₀ =>
  range.all fun t₁ =>
  range.all fun t₂ =>
  range.all fun t₃ =>
  range.all fun t₄ =>
    if t₀ == 0 && t₁ == 0 && t₂ == 0 && t₃ == 0 && t₄ == 0 then true
    else liftWeightNat p t₀ t₁ t₂ t₃ t₄ ≥ p + 1

#eval checkAllVectors 3
#eval checkAllVectors 5
#eval checkAllVectors 7

end Davenport.Verify
