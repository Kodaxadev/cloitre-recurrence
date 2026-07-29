use conjecture::{dq, step, State};

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
