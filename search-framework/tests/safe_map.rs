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
