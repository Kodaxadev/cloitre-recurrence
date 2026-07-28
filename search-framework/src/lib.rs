//! Research framework for the stabilization conjecture of OEIS A073117 / A117846.
//!
//! The recurrence is
//!     b_1 = m,   b_{n+1} = b_n + (b_n mod n)
//! with `mod` the least nonnegative remainder. The conjecture (Cloitre 2002,
//! Abercrombie 2007) is that for every m the increments are eventually constant.
//!
//! All arithmetic here is exact. Two representations are used:
//!
//!   * `b`-form    : the raw value b_n; one division per step.
//!   * `(q,r)`-form: b_n = q_n*n + r_n, 0 <= r_n < n; DIVISION-FREE per step
//!                   once q_n <= n, which holds after O(sqrt(m)) steps.
//!
//! See `docs/partial-proofs.md` for the proofs of the facts asserted here.

pub mod cli;
pub mod dynamics;
pub mod hash;
pub mod monotone;
pub mod sweep;
pub mod witness;

pub use dynamics::{absorbed_b, dq, enter, solve, solve_fast, step, step_b, Outcome, State};
pub use hash::Fnv;
