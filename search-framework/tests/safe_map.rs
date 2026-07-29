use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

fn signed_coordinates(state: SafeState) -> (u64, i128) {
    let s = state.n() + 2;
    let x = i128::from(s) + 1 - 2 * i128::from(state.e);
    (s, x)
}

#[test]
fn signed_distance_form_matches_safe_map() {
    for w in 2..=120u64 {
        for wraps in 0..=120u64 {
            for e in 1..w {
                let state = SafeState { e, w, wraps };
                let (s, x) = signed_coordinates(state);
                assert!(x.abs() < i128::from(s));
                assert_eq!(x.rem_euclid(2), (i128::from(s) + 1).rem_euclid(2));

                match safe_step(state) {
                    SafeOutcome::Continue {
                        state: next,
                        digit: SafeDigit::Zero,
                    } => {
                        assert!(x >= i128::from(wraps) + 3);
                        let (next_s, next_x) = signed_coordinates(next);
                        assert_eq!(next_s, s + 1);
                        assert_eq!(next_x, 2 * x - i128::from(s));
                        assert_eq!(next.wraps, wraps);
                    }
                    SafeOutcome::Continue {
                        state: next,
                        digit: SafeDigit::Wrap,
                    } => {
                        assert!(x <= 0);
                        let (next_s, next_x) = signed_coordinates(next);
                        assert_eq!(next_s, s + 1);
                        assert_eq!(next_x, 2 * x + i128::from(s));
                        assert_eq!(next.wraps, wraps + 1);
                    }
                    SafeOutcome::Terminated { .. } => {
                        assert!(x >= 1);
                        assert!(x <= i128::from(wraps) + 2);
                    }
                }
            }
        }
    }
}

fn assert_restart_dominates(mut larger: SafeState, transitions: usize) {
    let quotient_gap = larger.wraps;
    let mut restarted = SafeState {
        e: larger.e,
        w: larger.n(),
        wraps: 0,
    };
    for _ in 0..transitions {
        let larger_next = match safe_step(larger) {
            SafeOutcome::Continue { state, .. } => state,
            SafeOutcome::Terminated { .. } => {
                panic!("larger-quotient path terminated before its prefix")
            }
        };
        let restarted_next = match safe_step(restarted) {
            SafeOutcome::Continue { state, .. } => state,
            SafeOutcome::Terminated { .. } => {
                panic!("quotient-zero restart terminated first")
            }
        };
        assert_eq!(restarted_next.e, larger_next.e);
        assert_eq!(larger_next.wraps - restarted_next.wraps, quotient_gap);
        larger = larger_next;
        restarted = restarted_next;
    }
}

#[test]
fn every_finite_safe_prefix_propagates_to_the_next_checkpoint() {
    for n in 2..=150u64 {
        for e in 1..n {
            let mut path = Vec::new();
            let mut state = SafeState { e, w: n, wraps: 0 };
            for _ in 0..2_000 {
                path.push(state);
                match safe_step(state) {
                    SafeOutcome::Continue { state: next, .. } => state = next,
                    SafeOutcome::Terminated { .. } => break,
                }
            }

            for (offset, &checkpoint_state) in path.iter().enumerate().skip(1) {
                let remaining = path.len() - offset - 1;
                assert_restart_dominates(checkpoint_state, remaining);
            }
        }
    }
}

#[test]
fn accelerated_zero_epoch_matches_safe_map() {
    for w in 2..=100u64 {
        for wraps in 0..=60u64 {
            for e in 1..w {
                if 2 * e > w {
                    continue;
                }
                let start = SafeState { e, w, wraps };
                let slack = w - 2 * e;
                let mut current = match safe_step(start) {
                    SafeOutcome::Continue {
                        state,
                        digit: SafeDigit::Zero,
                    } => state,
                    _ => panic!("zero-epoch premise did not take a zero step"),
                };
                let mut run = 0u32;
                let stop = loop {
                    match safe_step(current) {
                        SafeOutcome::Continue {
                            state,
                            digit: SafeDigit::Wrap,
                        } => {
                            current = state;
                            run += 1;
                        }
                        outcome => break outcome,
                    }
                };

                let scale = |j: u32| (1u128 << (j + 1)) * u128::from(wraps + slack + 4);
                for j in 0..run {
                    assert!(scale(j) < u128::from(w + wraps + u64::from(j) + 5));
                }
                assert!(scale(run) >= u128::from(w + wraps + u64::from(run) + 5));
                if run > 0 {
                    let prior = (1u128 << run) * u128::from(wraps + slack + 4);
                    assert!(prior < u128::from(w + wraps + u64::from(run) + 4));
                    assert!((1u128 << run) * u128::from(wraps) < u128::from(w + wraps));
                }

                let candidate = i128::try_from(scale(run)).unwrap()
                    - i128::from(w)
                    - 2 * i128::from(wraps)
                    - 2 * i128::from(run)
                    - 7;
                let next_overshoot =
                    i128::try_from(scale(run)).unwrap() - i128::from(current.n() + 2);
                assert_eq!(current.w, w + 1);
                assert_eq!(current.wraps, wraps + u64::from(run));
                assert!((2..=i128::from(current.n() + 2)).contains(&next_overshoot));
                assert_eq!(next_overshoot.rem_euclid(2), i128::from(current.n() % 2));
                assert_eq!(candidate, next_overshoot - i128::from(current.wraps) - 4);
                match stop {
                    SafeOutcome::Continue {
                        digit: SafeDigit::Zero,
                        ..
                    } => {
                        assert!(candidate >= 0);
                        assert!(next_overshoot >= i128::from(current.wraps + 4));
                        assert_eq!(candidate, i128::from(current.w - 2 * current.e));
                    }
                    SafeOutcome::Terminated { .. } => {
                        assert!(candidate < 0);
                        assert!(next_overshoot <= i128::from(current.wraps + 3));
                    }
                    SafeOutcome::Continue {
                        digit: SafeDigit::Wrap,
                        ..
                    } => unreachable!("loop stops at the first non-wrap"),
                }
            }
        }
    }
}
