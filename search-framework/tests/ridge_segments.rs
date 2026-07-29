use conjecture::{dq, step, State};

#[derive(Clone, Copy, Debug)]
struct PureSegment {
    ups: u32,
    value: i128,
    zeros: u32,
    end: State,
}

fn pure_segment(parent: State) -> Option<PureSegment> {
    assert_eq!(dq(parent), -1);
    let start = step(parent);
    let mut states = vec![start];
    let mut changes = Vec::new();
    let mut current = start;
    for _ in 0..500 {
        if current.absorbed() {
            return None;
        }
        if dq(current) == -1 {
            break;
        }
        changes.push(dq(current));
        current = step(current);
        states.push(current);
    }
    if dq(current) != -1 {
        return None;
    }

    let ups = changes.iter().take_while(|&&change| change == 1).count();
    if ups == 0 || changes[ups..].iter().any(|&change| change != 0) {
        return None;
    }
    let zeros = changes.len() - ups;
    let after_up = states[ups];
    let value = i128::from(after_up.q) - i128::from(after_up.r);
    assert!(value >= 1);

    let quotient = i128::from(start.q);
    let gap = i128::from(start.n - start.r);
    let width = quotient + gap + 3;
    assert_eq!(
        i128::from(start.n),
        (1i128 << ups) * width - ups as i128 - 3 - value
    );

    let terminal_quotient = quotient + ups as i128;
    let ratio = u64::try_from(terminal_quotient / value).unwrap();
    assert_eq!(u32::try_from(zeros).unwrap(), ratio.ilog2());
    let next_gap = i128::from(current.q) - 2 * i128::from(current.r);
    assert_eq!(next_gap, (1i128 << (zeros + 1)) * value - terminal_quotient);
    let next_start = step(current);
    assert_eq!(
        i128::from(next_start.q + next_start.n - next_start.r + 3),
        (1i128 << (zeros + 1)) * value + 2
    );
    Some(PureSegment {
        ups: u32::try_from(ups).unwrap(),
        value,
        zeros: u32::try_from(zeros).unwrap(),
        end: current,
    })
}

#[test]
fn terminal_negative_suffix_matches_next_ridge_gap() {
    let mut checked = 0u64;
    let mut defect_checked = 0u64;
    for n in [64u64, 128, 256] {
        for q in 1..=40 {
            for r in 0..(q + 1) / 2 {
                let parent = State { n, q, r };
                assert_eq!(dq(parent), -1);
                let start = step(parent);
                if i128::from(start.r) - i128::from(start.q) <= 0 {
                    continue;
                }

                let mut states = vec![start];
                let mut changes = Vec::new();
                let mut current = start;
                for _ in 0..300 {
                    if current.absorbed() || dq(current) == -1 {
                        break;
                    }
                    changes.push(dq(current));
                    current = step(current);
                    states.push(current);
                }
                if current.absorbed() || dq(current) != -1 {
                    continue;
                }

                let Some(last_up) = changes.iter().rposition(|&change| change == 1) else {
                    continue;
                };
                assert!(changes[last_up + 1..].iter().all(|&change| change == 0));

                let after = states[last_up + 1];
                let value = i128::from(after.q) - i128::from(after.r);
                let quotient = i128::from(after.q);
                let zeros = u32::try_from(changes.len() - last_up - 1).unwrap();
                assert!((1..=quotient).contains(&value));
                assert_eq!(i128::from(current.q), quotient);
                assert_eq!(
                    i128::from(current.r) - i128::from(current.q),
                    -(1i128 << zeros) * value
                );
                assert!((1i128 << zeros) * value <= quotient);
                assert!(quotient < (1i128 << (zeros + 1)) * value);

                let next_gap = i128::from(current.q) - 2 * i128::from(current.r);
                assert_eq!(next_gap, (1i128 << (zeros + 1)) * value - quotient);
                assert!((1..=quotient).contains(&next_gap));

                let distance = u32::try_from(current.n - parent.n).unwrap();
                if distance < 120 {
                    let parent_gap = parent.q - 2 * parent.r;
                    let parent_budget = parent.q + parent_gap + 2;
                    let next_budget = current.q + u64::try_from(next_gap).unwrap() + 2;
                    let mut scaled_right =
                        (u128::from(current.n + 2) * 2) + u128::from(next_budget);
                    for (offset, &change) in changes.iter().enumerate() {
                        if change == 0 {
                            let digit_index = parent.n + offset as u64 + 1;
                            let shift = distance - u32::try_from(offset).unwrap() - 1;
                            scaled_right += u128::from(digit_index + 2) << shift;
                        }
                    }
                    assert_eq!(
                        u128::from(parent_budget) << distance,
                        scaled_right,
                        "parent={parent:?} end={current:?}"
                    );
                    defect_checked += 1;
                }
                checked += 1;
            }
        }
    }
    assert!(checked > 500, "ridge-segment test too weak: {checked}");
    assert!(
        defect_checked > 500,
        "defect recurrence test too weak: {defect_checked}"
    );
}

#[test]
fn explicit_ridge_family_has_vanishing_up_fraction() {
    for k in 1u32..=7 {
        let quotient = 1u64 << (k * k);
        let gap = 3u64;
        let start_n = (1u64 << k) * (quotient + gap + 3) - u64::from(k) - 4;
        let mut current = State {
            n: start_n - 1,
            q: quotient + 1,
            r: (quotient + 1 - gap) / 2,
        };
        assert_eq!(dq(current), -1);
        current = step(current);

        for _ in 0..k {
            assert_eq!(dq(current), 1);
            current = step(current);
        }
        assert_eq!(current.q, quotient + u64::from(k));
        assert_eq!(i128::from(current.r) - i128::from(current.q), -1);

        for zero_offset in 0..(k * k) {
            assert_eq!(dq(current), 0);
            assert_eq!(
                i128::from(current.r) - i128::from(current.q),
                -(1i128 << zero_offset)
            );
            current = step(current);
        }
        assert_eq!(dq(current), -1);
        assert_eq!(
            i128::from(current.r) - i128::from(current.q),
            -(1i128 << (k * k))
        );
    }
}

#[test]
fn three_unit_terminal_ridges_have_incompatible_scales() {
    for first_ups in 1u32..=12 {
        for first_zeros in 1u32..=12 {
            let left_scale = (1u128 << first_ups) * ((1u128 << (first_zeros + 1)) + 2);
            for next_ups in 1u32..=12 {
                for next_zeros in first_zeros..=12 {
                    let left = left_scale + u128::from(next_zeros + next_ups + 1);
                    let right = (1u128 << next_ups) * ((1u128 << (next_zeros + 1)) + 2);
                    assert_ne!(left, right);
                }
            }
        }
    }
}

#[test]
fn arbitrary_terminal_pure_ridges_obey_the_dyadic_congruence() {
    let mut pure_checked = 0u64;
    let mut adjacent_checked = 0u64;
    for n in [64u64, 128, 256] {
        for q in 1..=40 {
            for r in 0..(q + 1) / 2 {
                let parent = State { n, q, r };
                let Some(first) = pure_segment(parent) else {
                    continue;
                };
                pure_checked += 1;
                let Some(second) = pure_segment(first.end) else {
                    continue;
                };
                adjacent_checked += 1;

                let start = step(parent);
                let width = i128::from(start.q + start.n - start.r + 3);
                let next_start = step(first.end);
                let next_width = i128::from(next_start.q + next_start.n - next_start.r + 3);
                let defect = i128::from(first.zeros + second.ups + 1) + second.value - first.value;
                assert_eq!(
                    (1i128 << first.ups) * width + defect,
                    (1i128 << second.ups) * next_width
                );
                assert_eq!(defect.rem_euclid(1i128 << first.ups.min(second.ups)), 0);
            }
        }
    }
    assert!(pure_checked > 100);
    assert!(adjacent_checked > 20);

    let expected = [
        (1, 13, 0),
        (1, 11, 0),
        (1, 1, 4),
        (1, 15, 0),
        (1, 9, 1),
        (1, 18, 0),
        (1, 16, 0),
        (1, 6, 1),
    ];
    let mut parent = State { n: 38, q: 18, r: 5 };
    for want in expected {
        let segment = pure_segment(parent).expect("expected a pure ridge");
        assert_eq!(
            (segment.ups, segment.value, segment.zeros),
            (want.0, want.1, want.2)
        );
        parent = segment.end;
    }
    assert!(pure_segment(parent).is_none());
}
