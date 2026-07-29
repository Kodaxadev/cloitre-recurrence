use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy, Debug)]
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
                digit: SafeDigit::Wrap,
                state,
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
            if let Some(next) = next_zero {
                state = next;
                continue;
            }
            break;
        }
        match safe_step(state) {
            SafeOutcome::Continue { state: next, .. } => state = next,
            SafeOutcome::Terminated { .. } => break,
        }
    }
    blocks
}

fn gate_candidates(m: u64, wraps: u64, k: u32, r: u32) -> Vec<u64> {
    let width = m - wraps;
    let parent_n = m - u64::from(k) - 1;
    let parent_wraps = wraps - u64::from(k);
    let modulus = 1i128 << (k + 1);
    let target = (i128::from(m + 3) - (1i128 << k) * i128::from(parent_n)).rem_euclid(modulus);
    (1..width)
        .filter(|&value| {
            i128::from(value).rem_euclid(modulus) == target
                && (1u128 << (r + 2)) * u128::from(value) > u128::from(m + u64::from(r) + 3)
                && (1u128 << (r + 1)) * u128::from(value) <= u128::from(width + u64::from(r))
                && {
                    let parent_overshoot = (m + 3 - value) / (1u64 << k);
                    (parent_wraps + 4..=parent_n + 2).contains(&parent_overshoot)
                }
        })
        .collect()
}

fn assert_candidate_realizes(m: u64, wraps: u64, k: u32, r: u32, residue: u64) {
    let parent_n = m - u64::from(k) - 1;
    let parent_wraps = wraps - u64::from(k);
    let parent_overshoot = (m + 3 - residue) / (1u64 << k);
    let parent_e = (parent_n + 4 - parent_overshoot) / 2;
    assert_eq!(
        accelerate_zero(SafeState {
            e: parent_e,
            w: parent_n - parent_wraps,
            wraps: parent_wraps,
        }),
        Some((
            k,
            Some(SafeState {
                e: residue,
                w: m - wraps,
                wraps,
            })
        ))
    );

    let mut current = SafeState {
        e: residue,
        w: m - wraps,
        wraps,
    };
    for _ in 0..r {
        let (block_wraps, next) = accelerate_zero(current).unwrap();
        assert_eq!(block_wraps, 0);
        current = next.unwrap();
    }
    assert!(accelerate_zero(current).unwrap().0 > 0);
}

#[test]
fn adjacent_positive_blocks_obey_the_dyadic_gate() {
    let mut gates = 0u64;
    let mut unique = 0u64;
    let mut multiple = 0u64;

    for n in 2..=120u64 {
        for e in 1..n {
            let blocks = zero_blocks(SafeState { e, w: n, wraps: 0 });
            for (index, block) in blocks.iter().enumerate() {
                let Some(next_zero) = block.next_zero else {
                    continue;
                };
                if block.wraps == 0 {
                    continue;
                }

                let mut next_positive = index + 1;
                while next_positive < blocks.len()
                    && blocks[next_positive].wraps == 0
                    && blocks[next_positive].next_zero.is_some()
                {
                    next_positive += 1;
                }
                if next_positive == blocks.len() || blocks[next_positive].wraps == 0 {
                    continue;
                }

                let r = u32::try_from(next_positive - index - 1).unwrap();
                let m = next_zero.n();
                let old_overshoot = block.start.n() + 4 - 2 * block.start.e;
                assert_eq!(m + 3 - next_zero.e, (1u64 << block.wraps) * old_overshoot);

                let candidates = gate_candidates(m, next_zero.wraps, block.wraps, r);
                assert!(candidates.contains(&next_zero.e));
                for &candidate in &candidates {
                    assert_candidate_realizes(m, next_zero.wraps, block.wraps, r, candidate);
                }
                let gap = m - 2 * next_zero.wraps;
                let numerator = gap + u64::from(r) - 3;
                let denominator = 1u64 << (block.wraps + r + 3);
                let bound = numerator.div_ceil(denominator);
                assert!(u64::try_from(candidates.len()).unwrap() <= bound);

                let parent_a = block.start.n() + 4 - 2 * block.start.e;
                let parent_d = parent_a - block.start.wraps - 4;
                let excess = (1u128 << (r + 2)) * u128::from(next_zero.e)
                    - u128::from(m + u64::from(r) + 3);
                let spacing = 1u128 << (block.wraps + r + 3);
                let next_start = blocks[next_positive].start;
                let child_d =
                    next_start.n() - next_start.wraps - 2 * next_start.e;
                assert_eq!(
                    u128::from(numerator) - excess,
                    2 * u128::from(child_d)
                );
                let boundary_unique = excess <= spacing
                    && (parent_d <= 1
                        || 2 * u128::from(child_d) < spacing);
                assert_eq!(candidates.len() == 1, boundary_unique);
                let boundary_multiple = excess > spacing
                    || (parent_d >= 2
                        && 2 * u128::from(child_d) >= spacing);
                assert_eq!(candidates.len() >= 2, boundary_multiple);

                if candidates.len() == 1 {
                    unique += 1;
                } else {
                    multiple += 1;
                    assert!(denominator < numerator);
                }
                gates += 1;
            }
        }
    }

    assert_eq!(gates, 29_630);
    assert_eq!(unique, 9_718);
    assert_eq!(multiple, 19_912);
}

#[test]
fn three_parent_boundary_starts_force_the_terminal_pattern() {
    let mut solutions = Vec::new();
    for r in 0..=64u32 {
        let scale = 1i128 << (r + 2);
        for next_r in 0..=64u32 {
            let next_scale = 1i128 << (next_r + 2);
            for delta in [3i128, 5] {
                let next_delta = if r % 2 == 1 { delta } else { 8 - delta };
                let final_delta = if next_r % 2 == 1 {
                    next_delta
                } else {
                    8 - next_delta
                };
                let numerator = next_scale * i128::from(r) + scale * delta
                    - (next_scale + 1) * next_delta
                    - 2 * i128::from(next_r)
                    - 2
                    + final_delta;
                let denominator = scale - next_scale;
                if denominator == 0 {
                    assert_ne!(numerator, 0);
                    continue;
                }
                if numerator % denominator != 0 {
                    continue;
                }
                let gap = numerator / denominator;
                let n = (scale - 1) * gap - scale * delta - 2 * i128::from(r) - 5 + next_delta;
                if gap < delta + 1 || n < gap || (n - gap) % 2 != 0 {
                    continue;
                }
                solutions.push((r, next_r, delta, next_delta, final_delta, gap, n));
            }
        }
    }

    assert_eq!(solutions, vec![(0, 1, 3, 5, 5, 8, 12)]);
    assert_eq!(
        accelerate_zero(SafeState {
            e: 5,
            w: 10,
            wraps: 2,
        }),
        Some((
            1,
            Some(SafeState {
                e: 5,
                w: 11,
                wraps: 3,
            })
        ))
    );
    assert_eq!(
        accelerate_zero(SafeState {
            e: 5,
            w: 11,
            wraps: 3,
        }),
        Some((
            1,
            Some(SafeState {
                e: 3,
                w: 12,
                wraps: 4,
            })
        ))
    );
    assert_eq!(
        accelerate_zero(SafeState {
            e: 3,
            w: 12,
            wraps: 4,
        }),
        Some((
            0,
            Some(SafeState {
                e: 6,
                w: 13,
                wraps: 4,
            })
        ))
    );
    assert_eq!(
        accelerate_zero(SafeState {
            e: 6,
            w: 13,
            wraps: 4,
        }),
        Some((
            1,
            Some(SafeState {
                e: 4,
                w: 14,
                wraps: 5,
            })
        ))
    );
    assert_eq!(
        accelerate_zero(SafeState {
            e: 4,
            w: 14,
            wraps: 5,
        }),
        Some((0, None))
    );
}
