//! Exact auxiliary dynamics for a positive tail with no quotient down-step.
//!
//! `SafeState` is the quotient-zero dominant state from Lemmas 40--43:
//! `wraps` is its quotient, `w = n - wraps`, and `0 < e < w`.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct SafeState {
    pub e: u64,
    pub w: u64,
    pub wraps: u64,
}

impl SafeState {
    #[inline]
    pub fn n(self) -> u64 {
        self.w
            .checked_add(self.wraps)
            .expect("safe-state index overflow")
    }

    #[inline]
    pub fn h(self) -> u64 {
        self.w - self.e
    }

    #[inline]
    pub fn check(self) -> bool {
        self.e > 0 && self.e < self.w
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SafeDigit {
    Zero,
    Wrap,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SafeOutcome {
    Continue {
        state: SafeState,
        digit: SafeDigit,
    },
    Terminated {
        capture: bool,
    },
}

/// One transition of Lemma 42's exact safe map.
#[inline]
pub fn safe_step(state: SafeState) -> SafeOutcome {
    debug_assert!(state.check(), "invalid safe state: {state:?}");
    let doubled = state.e.checked_mul(2).expect("safe e overflow");
    let modulus = state
        .n()
        .checked_add(2)
        .expect("safe modulus overflow");
    if doubled <= state.w {
        SafeOutcome::Continue {
            state: SafeState {
                e: doubled,
                w: state.w + 1,
                wraps: state.wraps,
            },
            digit: SafeDigit::Zero,
        }
    } else if doubled > modulus {
        SafeOutcome::Continue {
            state: SafeState {
                e: doubled - modulus,
                w: state.w,
                wraps: state.wraps + 1,
            },
            digit: SafeDigit::Wrap,
        }
    } else {
        SafeOutcome::Terminated {
            capture: doubled == modulus,
        }
    }
}
