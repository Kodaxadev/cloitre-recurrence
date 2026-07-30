//! Tests for Lemmas 135/136 and Theorem 137: the closed block-chain map.
//!
//! The closed forms are re-derived here and compared against the project's
//! literal safe map, so a change to either side has to be reflected in the
//! other to keep this passing.

use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Description {
    n: i128,
    wraps: i128,
    length: i128,
    returned: i128,
}

/// (136.1): least r >= 0 with 2^(r+2) f >= m + r + 4.
fn forced_gap(m: i128, returned: i128) -> u32 {
    let mut gap = 0u32;
    while (returned << (gap + 2)) < m + i128::from(gap) + 4 {
        gap += 1;
    }
    gap
}

/// (135.2): least K >= 1 with 2^(K+1) A >= n + K + 5.
fn forced_length(n: i128, overshoot: i128) -> u32 {
    let mut length = 1u32;
    while (overshoot << (length + 1)) < n + i128::from(length) + 5 {
        length += 1;
    }
    length
}

/// (137.1): the closed successor of a block description.
fn psi(current: Description) -> Description {
    let m = current.n + current.length + 1;
    let gap = forced_gap(m, current.returned);
    let child_n = m + i128::from(gap);
    let overshoot = child_n + 4 - (current.returned << (gap + 1));
    let length = forced_length(child_n, overshoot);
    Description {
        n: child_n,
        wraps: current.wraps + current.length,
        length: i128::from(length),
        returned: child_n + i128::from(length) + 4 - (overshoot << length),
    }
}

/// Literal block descriptions along the safe path from `start`.
fn literal_descriptions(start: SafeState, limit: usize) -> Vec<Description> {
    let mut out = Vec::new();
    let mut current = start;
    for _ in 0..limit {
        let after_zero = match safe_step(current) {
            SafeOutcome::Continue {
                state,
                digit: SafeDigit::Zero,
            } => state,
            SafeOutcome::Continue { state, .. } => {
                current = state;
                continue;
            }
            SafeOutcome::Terminated { .. } => return out,
        };
        let mut walker = after_zero;
        let mut wraps = 0i128;
        let next_zero = loop {
            match safe_step(walker) {
                SafeOutcome::Continue {
                    digit: SafeDigit::Zero,
                    ..
                } => break Some(walker),
                SafeOutcome::Continue { state, .. } => {
                    wraps += 1;
                    walker = state;
                }
                SafeOutcome::Terminated { .. } => break None,
            }
        };
        if wraps > 0 {
            if let Some(returned) = next_zero {
                out.push(Description {
                    n: i128::from(current.n()),
                    wraps: i128::from(current.wraps),
                    length: wraps,
                    returned: i128::from(returned.e),
                });
            }
        }
        match next_zero {
            Some(state) => current = state,
            None => return out,
        }
    }
    out
}

#[test]
fn theorem_137_iterated_map_matches_literal_traces() {
    let mut paths = 0u64;
    let mut steps = 0u64;
    for n in 8u64..=200 {
        for e in 1..n {
            let start = SafeState { e, w: n, wraps: 0 };
            if !start.check() {
                continue;
            }
            let chain = literal_descriptions(start, 400);
            if chain.len() < 2 {
                continue;
            }
            paths += 1;
            let mut state = chain[0];
            for expected in &chain[1..] {
                state = psi(state);
                assert_eq!(state, *expected, "closed map diverged from {n} {e}");
                steps += 1;
            }
        }
    }
    assert!(paths > 5_000, "too few paths: {paths}");
    assert!(steps > 50_000, "too few successive descriptions: {steps}");
}

#[test]
fn lemma_135_forced_length_holds_for_terminating_blocks_too() {
    let mut returning = 0u64;
    let mut terminating = 0u64;
    for n in 8u64..=140 {
        for e in 1..n {
            let start = SafeState { e, w: n, wraps: 0 };
            if !start.check() {
                continue;
            }
            // Walk blocks manually so terminating ones are seen as well.
            let mut current = start;
            for _ in 0..400 {
                let after_zero = match safe_step(current) {
                    SafeOutcome::Continue {
                        state,
                        digit: SafeDigit::Zero,
                    } => state,
                    SafeOutcome::Continue { state, .. } => {
                        current = state;
                        continue;
                    }
                    SafeOutcome::Terminated { .. } => break,
                };
                let block_n = i128::from(current.n());
                let overshoot = block_n + 4 - 2 * i128::from(current.e);
                let mut walker = after_zero;
                let mut wraps = 0u32;
                let next_zero = loop {
                    match safe_step(walker) {
                        SafeOutcome::Continue {
                            digit: SafeDigit::Zero,
                            ..
                        } => break Some(walker),
                        SafeOutcome::Continue { state, .. } => {
                            wraps += 1;
                            walker = state;
                        }
                        SafeOutcome::Terminated { .. } => break None,
                    }
                };
                if wraps > 0 {
                    assert_eq!(
                        forced_length(block_n, overshoot),
                        wraps,
                        "block length formula failed at {n} {e}"
                    );
                    if next_zero.is_some() {
                        returning += 1;
                    } else {
                        terminating += 1;
                    }
                }
                match next_zero {
                    Some(state) => current = state,
                    None => break,
                }
            }
        }
    }
    assert!(returning > 10_000, "too few returning blocks: {returning}");
    assert!(terminating > 100, "no terminating blocks seen: {terminating}");
}

#[test]
fn theorem_130_is_the_unit_fibre() {
    // At k = k' = 1 the recurrence (137.2) collapses to (130.7).
    let unit = Description {
        n: 978,
        wraps: 11,
        length: 1,
        returned: 127,
    };
    let next = psi(unit);
    assert_eq!(next.length, 1);
    let gap = forced_gap(unit.n + 2, unit.returned);
    assert_eq!(next.n, unit.n + 2 + i128::from(gap));
    // (130.7): f' = 2^(r+2) f - n' - 3.
    assert_eq!(
        next.returned,
        (unit.returned << (gap + 2)) - next.n - 3,
        "unit fibre does not match (130.7)"
    );
}
