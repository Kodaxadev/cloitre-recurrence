//! Tests for Theorem 130, Lemma 131 and Corollary 132.
//!
//! The reduced map is re-derived here from the inequalities of Corollary 115
//! and is cross-checked against the project's literal safe map.

use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

/// Lemma 117.
fn unit_state(n: i128, quotient: i128, returned: i128) -> bool {
    let d_coord = n - 2 * quotient;
    (n + 3 + returned) % 4 == 0
        && returned >= 1
        && returned <= d_coord - 3
        && 4 * returned <= n + d_coord + 2
}

/// Every admissible exponent, found by scanning rather than by (130.2).
fn admissible_exponents(n: i128, quotient: i128, returned: i128) -> Vec<(u32, i128)> {
    let d_coord = n - 2 * quotient;
    let defect = d_coord - 3 - returned;
    if defect < 4 || defect % 2 != 0 {
        return Vec::new();
    }
    let mut answer = Vec::new();
    for exponent in 2..=80u32 {
        let Some(scaled) = (1i128 << exponent).checked_mul(returned) else {
            break;
        };
        let spacing = 1i128 << (exponent + 2);
        let child = scaled - n - i128::from(exponent) - 3;
        if child < 1 {
            continue;
        }
        if child > spacing {
            continue;
        }
        if d_coord + i128::from(exponent) - 2 - 3 - child < spacing {
            continue;
        }
        answer.push((exponent, child));
    }
    answer
}

/// The forced exponent of (130.2).
fn forced_exponent(n: i128, returned: i128) -> u32 {
    let mut exponent = 2u32;
    while (1i128 << exponent) * returned < n + i128::from(exponent) + 4 {
        exponent += 1;
    }
    exponent
}

/// One step of the deterministic map (130.3).
fn forced_step(n: i128, quotient: i128, returned: i128) -> Option<(u32, i128, i128, i128)> {
    let d_coord = n - 2 * quotient;
    let defect = d_coord - 3 - returned;
    if defect < 4 || defect % 2 != 0 {
        return None;
    }
    let exponent = forced_exponent(n, returned);
    let spacing = 1i128 << (exponent + 2);
    let child = (1i128 << exponent) * returned - n - i128::from(exponent) - 3;
    if child < 1 || child > spacing {
        return None;
    }
    if d_coord + i128::from(exponent) - 5 - child < spacing {
        return None;
    }
    Some((exponent, child, n + i128::from(exponent), quotient + 1))
}

fn chain_length(n: i128, quotient: i128, returned: i128) -> u32 {
    let mut state = (n, quotient, returned);
    let mut length = 0;
    while let Some((_, child, child_n, child_q)) = forced_step(state.0, state.1, state.2) {
        state = (child_n, child_q, child);
        length += 1;
        assert!(
            length < 4096,
            "runaway chain from {n} {quotient} {returned}"
        );
    }
    length
}

/// Read the gap and returned residue off a literal safe-map trace.
fn literal_gate(n: i128, quotient: i128, returned: i128) -> Option<(u32, i128)> {
    let start = SafeState {
        e: u64::try_from((n + 3 + returned) / 4).ok()?,
        w: u64::try_from(n - quotient).ok()?,
        wraps: u64::try_from(quotient).ok()?,
    };
    let mut word = Vec::new();
    let mut states = vec![start];
    let mut current = start;
    for _ in 0..4096 {
        match safe_step(current) {
            SafeOutcome::Continue { state, digit } => {
                word.push(digit);
                states.push(state);
                current = state;
            }
            SafeOutcome::Terminated { .. } => break,
        }
    }
    if word.len() < 3 || word[0] != SafeDigit::Zero || word[1] != SafeDigit::Wrap {
        return None;
    }
    if i128::from(states[2].e) != returned {
        return None;
    }
    let mut index = 2;
    let mut zeros = 0u32;
    while index < word.len() && word[index] == SafeDigit::Zero {
        zeros += 1;
        index += 1;
    }
    if zeros == 0 || index >= word.len() || word[index] != SafeDigit::Wrap {
        return None;
    }
    if index + 1 >= word.len() || word[index + 1] != SafeDigit::Zero {
        return None;
    }
    Some((zeros + 1, i128::from(states[index + 1].e)))
}

#[test]
fn theorem_130_has_no_branching() {
    let mut live = 0u64;
    let mut states = 0u64;
    for n in 6i128..=420 {
        for quotient in 0..=(n - 6) / 2 {
            if n - 2 * quotient < 8 {
                continue;
            }
            for returned in 1..n - 2 * quotient - 2 {
                if !unit_state(n, quotient, returned) {
                    continue;
                }
                states += 1;
                let found = admissible_exponents(n, quotient, returned);
                assert!(found.len() <= 1, "branching at {n} {quotient} {returned}");
                match forced_step(n, quotient, returned) {
                    Some((exponent, child, child_n, child_q)) => {
                        assert_eq!(found, vec![(exponent, child)]);
                        // The image is again a unit state, and (130.7) holds.
                        assert!(unit_state(child_n, child_q, child));
                        assert_eq!(child_n + 3 + child, (1i128 << exponent) * returned);
                        live += 1;
                    }
                    None => assert!(found.is_empty()),
                }
            }
        }
    }
    assert!(states > 200_000, "thin grid: {states}");
    assert!(live > 10_000, "no live gates: {live}");
}

#[test]
fn forced_gate_matches_the_literal_safe_map() {
    let mut matched = 0u64;
    for n in 6i128..=200 {
        for quotient in 0..=(n - 6) / 2 {
            if n - 2 * quotient < 8 {
                continue;
            }
            for returned in 1..n - 2 * quotient - 2 {
                if !unit_state(n, quotient, returned) {
                    continue;
                }
                if let Some((exponent, child, _, _)) = forced_step(n, quotient, returned) {
                    let literal = literal_gate(n, quotient, returned)
                        .expect("forced gate absent from the literal trace");
                    assert_eq!(literal, (exponent, child));
                    matched += 1;
                }
            }
        }
    }
    assert!(matched > 3_000, "too few literal comparisons: {matched}");
}

#[test]
fn lemma_131_wrap_count_is_inert() {
    let mut strict = 0u64;
    for n in 6i128..=300 {
        for quotient in 1..=(n - 6) / 2 {
            if n - 2 * quotient < 8 {
                continue;
            }
            for returned in 1..n - 2 * quotient - 2 {
                if !unit_state(n, quotient, returned) {
                    continue;
                }
                // The (n, f) projections agree step by step.
                let mut raised = (n, quotient, returned);
                let mut lowered = (n, 0i128, returned);
                while let Some(step) = forced_step(raised.0, raised.1, raised.2) {
                    let low = forced_step(lowered.0, lowered.1, lowered.2)
                        .expect("lowered chain died first");
                    assert_eq!(step.0, low.0);
                    assert_eq!(step.1, low.1);
                    assert_eq!(step.2, low.2);
                    raised = (step.2, step.3, step.1);
                    lowered = (low.2, low.3, low.1);
                }
                let high = chain_length(n, quotient, returned);
                let low = chain_length(n, 0, returned);
                assert!(
                    high <= low,
                    "chain grew with U at {n} {quotient} {returned}"
                );
                if high < low {
                    strict += 1;
                }
            }
        }
    }
    assert!(strict > 0, "monotonicity never strict");
}

#[test]
fn corollary_132_repeats_descend() {
    let mut seen_repeats = 0u64;
    for n in 6i128..=1200 {
        for returned in 1..n - 2 {
            if !unit_state(n, 0, returned) {
                continue;
            }
            let mut history: Vec<((i128, u32), (i128, i128))> = Vec::new();
            let mut state = (n, 0i128, returned);
            while let Some((exponent, child, child_n, child_q)) =
                forced_step(state.0, state.1, state.2)
            {
                let key = (state.2, exponent);
                if let Some((_, (prev_n, prev_child))) =
                    history.iter().rev().find(|(seen, _)| *seen == key)
                {
                    // (132.1)
                    assert_eq!(child, prev_child - (child_n - prev_n));
                    assert!(child < *prev_child);
                    seen_repeats += 1;
                }
                history.push((key, (child_n, child)));
                state = (child_n, child_q, child);
            }
        }
    }
    assert!(seen_repeats > 0, "no repeated (f, h) pair in range");
}

#[test]
fn k14_witness_and_chain_ceiling() {
    // K14: the length-5 record, reached from (978, 11, 127).
    assert_eq!(chain_length(978, 11, 127), 5);
    assert_eq!(chain_length(978, 0, 127), 5);

    let mut gaps = Vec::new();
    let mut state = (978i128, 11i128, 127i128);
    while let Some((exponent, child, child_n, child_q)) = forced_step(state.0, state.1, state.2) {
        gaps.push(exponent - 2);
        state = (child_n, child_q, child);
    }
    assert_eq!(gaps, vec![1, 3, 3, 1, 5]);

    // No six-gate chain starts below this bound (K15 at a CI-sized bound).
    let mut best = 0;
    let mut best_at = (0i128, 0i128);
    for n in 6i128..=40_000 {
        for returned in 1..n - 2 {
            if !unit_state(n, 0, returned) {
                continue;
            }
            let length = chain_length(n, 0, returned);
            if length > best {
                best = length;
                best_at = (n, returned);
            }
        }
    }
    assert_eq!(best, 5, "chain ceiling changed: {best} at {best_at:?}");
    assert_eq!(best_at, (978, 127));
}
