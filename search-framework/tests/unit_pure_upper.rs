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
                current = state;
                wraps += 1;
            }
            SafeOutcome::Continue {
                digit: SafeDigit::Zero,
                ..
            } => return Some((wraps, Some(current))),
            SafeOutcome::Terminated { .. } => {
                return Some((wraps, None));
            }
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
                SafeOutcome::Continue { state: next, .. } => {
                    state = next;
                }
                SafeOutcome::Terminated { .. } => break,
            }
        }
    }
    blocks
}

fn pure_unit(blocks: &[Block], left: usize, right: usize) -> bool {
    let parent = blocks[left];
    let child = blocks[right];
    if parent.wraps != 1 || child.wraps != 1 {
        return false;
    }
    let gap = u32::try_from(right - left - 1).unwrap();
    let spacing = 1u128 << (gap + 4);
    let parent_defect =
        parent.start.n() - parent.start.wraps - 2 * parent.start.e;
    let child_defect =
        child.start.n() - child.start.wraps - 2 * child.start.e;
    let returned = child.next_zero.unwrap().e;
    parent_defect >= 2
        && u128::from(returned) <= spacing
        && 2 * u128::from(child_defect) >= spacing
}

#[test]
fn three_unit_blocks_obey_residue_compatibility() {
    let mut unit_triples = 0u64;
    let mut pure_triples = 0u64;
    let mut six_unit_windows = 0u64;
    for n in 2..=120u64 {
        for e in 1..n {
            let blocks = zero_blocks(SafeState { e, w: n, wraps: 0 });
            let positive: Vec<_> = blocks
                .iter()
                .enumerate()
                .filter(|(_, block)| {
                    block.wraps > 0 && block.next_zero.is_some()
                })
                .map(|(index, _)| index)
                .collect();
            for triple in positive.windows(3) {
                let [first, second, third] = triple else {
                    unreachable!()
                };
                let parents = [blocks[*first], blocks[*second], blocks[*third]];
                if parents.iter().any(|block| block.wraps != 1) {
                    continue;
                }
                let gap = u32::try_from(*second - *first - 1).unwrap();
                let next_gap =
                    u32::try_from(*third - *second - 1).unwrap();
                let f0 = parents[0].next_zero.unwrap().e;
                let f1 = parents[1].next_zero.unwrap().e;
                let f2 = parents[2].next_zero.unwrap().e;
                let n1 = parents[1].start.n();

                assert_eq!(
                    (1u128 << (gap + 2)) * u128::from(f0)
                        + u128::from(f2 + u64::from(next_gap) + 2),
                    ((1u128 << (next_gap + 2)) + 1) * u128::from(f1)
                );
                let modulus = 1i128 << (gap.min(next_gap) + 2);
                assert_eq!(
                    (i128::from(f2) - i128::from(f1)
                        + i128::from(next_gap)
                        + 2)
                        .rem_euclid(modulus),
                    0
                );
                assert_eq!(
                    u128::from(n1 + 3 + f1),
                    (1u128 << (gap + 2)) * u128::from(f0)
                );
                assert_eq!(
                    gap + 2,
                    (n1 + 3 + f1).trailing_zeros() - f0.trailing_zeros()
                );
                unit_triples += 1;

                if pure_unit(&blocks, *first, *second)
                    && pure_unit(&blocks, *second, *third)
                {
                    let n2 = parents[2].start.n();
                    let quotient2 = parents[2].start.wraps;
                    assert!(u128::from(f1) <= 1u128 << (gap + 4));
                    assert!(f1 >= 5);
                    assert!(
                        u128::from((f1 - 4) * n2)
                            >= u128::from(
                                2 * f1 * quotient2 + 4 * f1 + 12 + 4 * f2
                            )
                    );
                    assert_eq!(
                        u128::from(n2 + 3 + f2),
                        (1u128 << (next_gap + 2)) * u128::from(f1)
                    );
                    pure_triples += 1;
                }
            }
            for window in positive.windows(6) {
                let parents: Vec<_> =
                    window.iter().map(|index| blocks[*index]).collect();
                if parents.iter().any(|block| block.wraps != 1) {
                    continue;
                }
                let gaps: Vec<_> = window
                    .windows(2)
                    .map(|pair| pair[1] - pair[0] - 1)
                    .collect();
                let residues: Vec<_> = parents
                    .iter()
                    .map(|block| block.next_zero.unwrap().e)
                    .collect();
                assert!(
                    gaps[0] != gaps[2]
                        || gaps[2] != gaps[4]
                        || residues[1] != residues[3]
                        || residues[3] != residues[5]
                );
                six_unit_windows += 1;
            }
        }
    }
    assert_eq!((unit_triples, pure_triples), (3_250, 580));
    assert_eq!(six_unit_windows, 167);
}

#[test]
fn strict_alternating_renewal_growth_is_too_large() {
    let mut checked = 0u64;
    for renewal_gap in 0..=2u32 {
        let scale = 1u32 << (renewal_gap + 2);
        assert!(scale >= renewal_gap + 4);
        for residue in 1..=16u128 {
            for quotient in 1..=4u32 {
                let large_gap = scale * quotient - renewal_gap - 4;
                let numerator = residue
                    * (1u128 << (large_gap + 2))
                    * ((1u128 << scale) - 1);
                assert!(
                    numerator
                        > u128::from((quotient + 1) * (scale + 1))
                );
                checked += 1;
            }
        }
    }
    assert_eq!(checked, 192);
}
