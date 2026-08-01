use std::collections::BTreeMap;

use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy)]
struct Block {
    start: SafeState,
    wraps: u32,
    next_zero: Option<SafeState>,
}

fn accelerate_zero(state: SafeState) -> Option<(u32, Option<SafeState>)> {
    let mut current = match safe_step(state) {
        SafeOutcome::Continue {
            state,
            digit: SafeDigit::Zero,
        } => state,
        _ => return None,
    };
    let mut wraps = 0;
    loop {
        match safe_step(current) {
            SafeOutcome::Continue {
                state,
                digit: SafeDigit::Wrap,
            } => {
                wraps += 1;
                current = state;
            }
            SafeOutcome::Continue {
                digit: SafeDigit::Zero,
                ..
            } => return Some((wraps, Some(current))),
            SafeOutcome::Terminated { .. } => return Some((wraps, None)),
        }
    }
}

fn zero_blocks(mut state: SafeState) -> Vec<Block> {
    let mut blocks = Vec::new();
    for _ in 0..2_000 {
        if let Some((wraps, next_zero)) = accelerate_zero(state) {
            blocks.push(Block {
                start: state,
                wraps,
                next_zero,
            });
            let Some(next) = next_zero else {
                break;
            };
            state = next;
        } else {
            match safe_step(state) {
                SafeOutcome::Continue { state: next, .. } => state = next,
                SafeOutcome::Terminated { .. } => break,
            }
        }
    }
    blocks
}

fn candidate_count(m: u64, wraps: u64, k: u32, r: u32) -> usize {
    let width = m - wraps;
    let parent_n = m - u64::from(k) - 1;
    let parent_wraps = wraps - u64::from(k);
    let modulus = 1i128 << (k + 1);
    let target = (i128::from(m + 3)
        - (1i128 << k) * i128::from(parent_n))
    .rem_euclid(modulus);
    (1..width)
        .filter(|&f| {
            i128::from(f).rem_euclid(modulus) == target
                && (1u128 << (r + 2)) * u128::from(f)
                    > u128::from(m + u64::from(r) + 3)
                && (1u128 << (r + 1)) * u128::from(f)
                    <= u128::from(width + u64::from(r))
                && {
                    let a = (m + 3 - f) / (1u64 << k);
                    (parent_wraps + 4..=parent_n + 2).contains(&a)
                }
        })
        .count()
}

fn unit_conditions(n: u64, quotient: u64, returned: u64) -> bool {
    let n = i128::from(n);
    let quotient = i128::from(quotient);
    let returned = i128::from(returned);
    let gap_coordinate = n - 2 * quotient;
    (n + 3 + returned).rem_euclid(4) == 0
        && returned >= 1
        && returned <= gap_coordinate - 3
        && 4 * returned <= n + gap_coordinate + 2
}

#[test]
fn exact_gate_multiplicity_matches_both_headrooms() {
    let mut histogram = BTreeMap::new();
    let mut upper_nonunique = 0u64;
    let mut unit_states = 0u64;
    let mut critical_pairs = 0u64;
    for n in 2..=120u64 {
        for e in 1..n {
            let blocks = zero_blocks(SafeState { e, w: n, wraps: 0 });
            for block in &blocks {
                if block.wraps == 1 {
                    if let Some(returned) = block.next_zero {
                        let start_n = i128::from(block.start.n());
                        let quotient = i128::from(block.start.wraps);
                        let returned_e = i128::from(returned.e);
                        let gap_coordinate = start_n - 2 * quotient;
                        let defect = start_n - quotient - 2 * i128::from(block.start.e);
                        assert!(unit_conditions(
                            block.start.n(),
                            block.start.wraps,
                            returned.e
                        ));
                        assert_eq!(i128::from(block.start.e), (start_n + 3 + returned_e) / 4);
                        assert_eq!(defect, (gap_coordinate - 3 - returned_e) / 2);
                        unit_states += 1;
                    }
                }
            }
            let positive: Vec<_> = blocks
                .iter()
                .enumerate()
                .filter(|(_, block)| {
                    block.wraps > 0 && block.next_zero.is_some()
                })
                .map(|(index, _)| index)
                .collect();
            let mut previous_pure_unit_gap = None;
            for pair in positive.windows(2) {
                let [left, right] = pair else {
                    unreachable!()
                };
                let block = blocks[*left];
                let returned = block.next_zero.unwrap();
                let child = blocks[*right].start;
                let k = block.wraps;
                let r = u32::try_from(*right - *left - 1).unwrap();
                let spacing = 1u128 << (k + r + 3);
                let expression = (1i128 << (r + 2))
                    * i128::from(block.start.n() + u64::from(k) + 4)
                    - (1i128 << (k + r + 2)) * i128::from(block.start.n())
                    - i128::from(block.start.n())
                    - i128::from(k + r)
                    - 4;
                let residue = expression.rem_euclid(spacing as i128);
                let rho = if residue == 0 {
                    spacing
                } else {
                    residue as u128
                };
                let excess = (1u128 << (r + 2)) * u128::from(returned.e)
                    - u128::from(returned.n() + u64::from(r) + 3);
                let translate = (excess - rho) / spacing;
                let parent_d =
                    block.start.n() - block.start.wraps - 2 * block.start.e;
                let child_d = child.n() - child.wraps - 2 * child.e;
                let child_block = blocks[*right];
                let child_k = child_block.wraps;
                let child_returned = child_block.next_zero.unwrap();
                let child_a = child.n() + 4 - 2 * child.e;
                assert_eq!(
                    2 * u128::from(child_a),
                    u128::from(child.n() + 5) - excess
                );
                let transfer = (1u128 << (child_k - 1))
                    * (u128::from(child.n() + 5) - excess);
                assert_eq!(
                    u128::from(child_returned.e),
                    u128::from(child.n() + u64::from(child_k) + 4) - transfer
                );
                if child_k == 1 {
                    assert_eq!(u128::from(child_returned.e), excess);
                }
                assert!(translate <= u128::from(block.start.e - 1));
                let lower = translate;
                let upper = u128::from(parent_d / 2)
                    .min(u128::from(2 * child_d) / spacing);
                let actual =
                    candidate_count(returned.n(), returned.wraps, k, r);
                assert_eq!(actual as u128, 1 + lower + upper);
                let child_gap = u128::from(child.n() - 2 * child.wraps);
                assert!((actual as u128 - 1) * spacing <= child_gap - 3 - rho);
                if parent_d >= 2 && 2 * child_d >= spacing as u64 {
                    assert!(
                        1u128 << (k + r + child_k + 2)
                            < u128::from(child.n() + u64::from(child_k) + 4)
                    );
                    upper_nonunique += 1;
                }
                let pure_unit = k == 1
                    && child_k == 1
                    && translate == 0
                    && parent_d >= 2
                    && 2 * u128::from(child_d) >= spacing;
                if pure_unit {
                    if let Some(previous_gap) = previous_pure_unit_gap {
                        assert!(u128::from(block.start.n()) < 1u128 << (previous_gap + r + 6));
                        critical_pairs += 1;
                    }
                    previous_pure_unit_gap = Some(r);
                } else {
                    previous_pure_unit_gap = None;
                }
                *histogram.entry(actual).or_insert(0u64) += 1;
            }
        }
    }
    assert_eq!(
        histogram,
        BTreeMap::from([
            (1, 8_411), (2, 5_776), (3, 4_578), (4, 3_021),
            (5, 1_127), (6, 1_370), (7, 2_204), (8, 543),
        ])
    );
    assert_eq!(upper_nonunique, 12_021);
    assert_eq!(unit_states, 18_852);
    assert_eq!(critical_pairs, 580);
}

#[test]
fn returning_unit_conditions_are_an_iff_on_bounded_states() {
    let mut literal = 0u64;
    let mut reconstructed = 0u64;
    for n in 2..=120u64 {
        for quotient in 0..n {
            for e in 1..n - quotient {
                let start = SafeState {
                    e,
                    w: n - quotient,
                    wraps: quotient,
                };
                let SafeOutcome::Continue {
                    state: after_zero,
                    digit: SafeDigit::Zero,
                } = safe_step(start)
                else {
                    continue;
                };
                let SafeOutcome::Continue {
                    state: returned,
                    digit: SafeDigit::Wrap,
                } = safe_step(after_zero)
                else {
                    continue;
                };
                let SafeOutcome::Continue {
                    digit: SafeDigit::Zero,
                    ..
                } = safe_step(returned)
                else {
                    continue;
                };
                assert!(unit_conditions(n, quotient, returned.e));
                assert_eq!(e, (n + 3 + returned.e) / 4);
                literal += 1;
            }
            for returned in 1..=n {
                if !unit_conditions(n, quotient, returned) {
                    continue;
                }
                let e = (n + 3 + returned) / 4;
                let start = SafeState {
                    e,
                    w: n - quotient,
                    wraps: quotient,
                };
                let SafeOutcome::Continue {
                    state: after_zero,
                    digit: SafeDigit::Zero,
                } = safe_step(start)
                else {
                    panic!("reconstructed state did not start with zero");
                };
                let SafeOutcome::Continue {
                    state: returned_state,
                    digit: SafeDigit::Wrap,
                } = safe_step(after_zero)
                else {
                    panic!("reconstructed state did not wrap");
                };
                assert_eq!(returned_state.e, returned);
                assert!(matches!(
                    safe_step(returned_state),
                    SafeOutcome::Continue {
                        digit: SafeDigit::Zero,
                        ..
                    }
                ));
                reconstructed += 1;
            }
        }
    }
    assert_eq!((literal, reconstructed), (24_140, 24_140));
}

#[test]
fn quotient_erasure_preserves_bounded_safe_words() {
    let mut transitions = 0u64;
    for n in 2..=60u64 {
        for quotient in 0..n - 1 {
            for e in 1..n - quotient {
                let mut original = SafeState {
                    e,
                    w: n - quotient,
                    wraps: quotient,
                };
                let mut lowered = SafeState { e, w: n, wraps: 0 };
                for _ in 0..80 {
                    let SafeOutcome::Continue {
                        state: next_original,
                        digit: original_digit,
                    } = safe_step(original)
                    else {
                        break;
                    };
                    let SafeOutcome::Continue {
                        state: next_lowered,
                        digit: lowered_digit,
                    } = safe_step(lowered)
                    else {
                        panic!("lowered path terminated before original path");
                    };
                    assert_eq!(lowered_digit, original_digit);
                    assert_eq!(next_lowered.n(), next_original.n());
                    assert_eq!(next_lowered.e, next_original.e);
                    assert_eq!(next_lowered.wraps, next_original.wraps - quotient);
                    original = next_original;
                    lowered = next_lowered;
                    transitions += 1;
                }
            }
        }
    }
    assert_eq!(transitions, 166_156);
}

#[test]
fn six_consecutive_pure_upper_gates_exist() {
    let blocks = zero_blocks(SafeState {
        e: 482,
        w: 966,
        wraps: 5,
    });
    let positive: Vec<_> = blocks
        .iter()
        .enumerate()
        .filter(|(_, block)| block.wraps > 0 && block.next_zero.is_some())
        .map(|(index, _)| index)
        .collect();
    let expected = [
        (971, 5, 482, 6, 0, 2, 413),
        (978, 11, 277, 1, 1, 413, 461),
        (981, 12, 254, 1, 3, 461, 461),
        (986, 13, 256, 1, 3, 461, 417),
        (991, 14, 280, 1, 1, 417, 475),
        (994, 15, 252, 1, 5, 475, 281),
    ];

    for (pair, expected_gate) in positive.windows(2).take(6).zip(expected) {
        let [left, right] = pair else { unreachable!() };
        let parent = blocks[*left];
        let returned = parent.next_zero.unwrap();
        let child = blocks[*right].start;
        let k = parent.wraps;
        let r = u32::try_from(*right - *left - 1).unwrap();
        let spacing = 1u128 << (k + r + 3);
        let excess = (1u128 << (r + 2)) * u128::from(returned.e)
            - u128::from(returned.n() + u64::from(r) + 3);
        let parent_d = parent.start.n() - parent.start.wraps - 2 * parent.start.e;
        let child_d = child.n() - child.wraps - 2 * child.e;
        assert_eq!(
            (
                parent.start.n(),
                parent.start.wraps,
                parent.start.e,
                k,
                r,
                parent_d,
                child_d,
            ),
            expected_gate
        );
        assert!(1 <= excess && excess <= spacing);
        assert!(parent_d >= 2);
        assert!(2 * u128::from(child_d) >= spacing);
    }
}
