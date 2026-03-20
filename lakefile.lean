import Lake
open Lake DSL

package «davenport» where

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

lean_lib «Davenport» where
  srcDir := "."
  roots := #[`DavenportAll]
