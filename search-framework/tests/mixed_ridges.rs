use conjecture::{dq, step, State};

#[derive(Clone, Copy, Debug)]
struct MixedRidge {
    end: State,
    prefix: u32,
    defect: u128,
    value: u64,
    suffix_zeros: u32,
    terminal_run: u32,
    width: u64,
    mixed: bool,
}

fn mixed_ridge(parent: State) -> Option<MixedRidge> {
    assert_eq!(dq(parent), -1);
    let start = step(parent);
    let mut current = start;
    let mut states = vec![start];
    let mut changes = Vec::new();

    for _ in 0..500 {
        if current.absorbed() || dq(current) == -1 {
            break;
        }
        changes.push(dq(current));
        current = step(current);
        states.push(current);
    }
    if current.absorbed() || dq(current) != -1 {
        return None;
    }

    let last_up = changes.iter().rposition(|&change| change == 1)?;
    assert!(changes[last_up + 1..].iter().all(|&change| change == 0));
    let prefix = last_up + 1;
    assert!(prefix < 120);
    let positive_zeros: Vec<usize> = changes[..prefix]
        .iter()
        .enumerate()
        .filter_map(|(offset, &change)| (change == 0).then_some(offset))
        .collect();
    let defect = positive_zeros.iter().fold(0u128, |sum, &offset| {
        sum + (u128::from(start.n) + offset as u128 + 2) * (1u128 << (prefix - 1 - offset))
    });
    let value = states[prefix].q - states[prefix].r;
    let suffix_zeros = u32::try_from(changes.len() - prefix).unwrap();
    let width = start.q + start.n - start.r + 3;
    let terminal_run = positive_zeros
        .last()
        .map_or(prefix, |&offset| prefix - 1 - offset);

    assert!(value >= 1);
    assert_eq!(
        (1u128 << prefix) * u128::from(width) - defect,
        u128::from(start.n) + prefix as u128 + 3 + u128::from(value)
    );
    let terminal_quotient = states[prefix].q;
    assert_eq!(suffix_zeros, (terminal_quotient / value).ilog2());
    let next_start = step(current);
    let next_width = next_start.q + next_start.n - next_start.r + 3;
    assert_eq!(
        u128::from(next_width),
        (1u128 << (suffix_zeros + 1)) * u128::from(value) + 2
    );
    assert_eq!(defect % (1u128 << terminal_run), 0);
    if let Some(&last_zero) = positive_zeros.last() {
        let last_zero_index = start.n + last_zero as u64;
        let last_zero_e = i128::from(states[last_zero].r) - i128::from(states[last_zero].q);
        assert_eq!(
            (1i128 << terminal_run) * (i128::from(last_zero_index) + 4 - 2 * last_zero_e),
            i128::from(last_zero_index)
                + i128::try_from(terminal_run).unwrap()
                + 4
                + i128::from(value)
        );
        for up_offset in 0..=terminal_run {
            let ladder_state = states[last_zero + 1 + up_offset];
            assert_eq!(
                i128::from(ladder_state.n) + 3
                    - (i128::from(ladder_state.r) - i128::from(ladder_state.q)),
                (1i128 << up_offset) * (i128::from(last_zero_index) + 4 - 2 * last_zero_e)
            );
        }
        assert_eq!(
            (defect >> terminal_run) % 2,
            (u128::from(start.n) + last_zero as u128 + 2) % 2
        );
    }

    Some(MixedRidge {
        end: current,
        prefix: u32::try_from(prefix).unwrap(),
        defect,
        value,
        suffix_zeros,
        terminal_run: u32::try_from(terminal_run).unwrap(),
        width,
        mixed: !positive_zeros.is_empty(),
    })
}

#[test]
fn arbitrary_mixed_ridges_obey_defect_compatibility() {
    let mut checked = 0u64;
    let mut mixed = 0u64;
    let mut adjacent = 0u64;

    for n in [64u64, 128, 256, 512] {
        for q in 1..=n.min(80) {
            for r in 0..(q + 1) / 2 {
                let parent = State { n, q, r };
                let Some(first) = mixed_ridge(parent) else {
                    continue;
                };
                checked += 1;
                mixed += u64::from(first.mixed);
                let Some(second) = mixed_ridge(first.end) else {
                    continue;
                };
                adjacent += 1;

                let first_base = (1u128 << first.prefix) * u128::from(first.width) - first.defect;
                let next_start = step(first.end);
                let next_width = next_start.q + next_start.n - next_start.r + 3;
                let second_base = (1u128 << second.prefix) * u128::from(next_width) - second.defect;
                assert_eq!(
                    first_base
                        + u128::from(first.suffix_zeros)
                        + u128::from(second.prefix)
                        + 1
                        + u128::from(second.value),
                    second_base + u128::from(first.value)
                );

                let representative = i128::from(first.suffix_zeros)
                    + i128::from(second.prefix)
                    + 1
                    + i128::from(second.value)
                    - i128::from(first.value);
                let rho = first.terminal_run.min(second.terminal_run);
                assert_eq!(representative.rem_euclid(1i128 << rho), 0);
            }
        }
    }
    assert!(checked > 4_000);
    assert!(mixed > 2_500);
    assert!(adjacent > 4_000);
}

#[test]
fn long_local_chain_need_not_grow_terminal_runs() {
    let mut current = State { n: 64, q: 4, r: 0 };
    for _ in 0..100 {
        let segment = mixed_ridge(current).expect("expected another ridge");
        assert!(segment.terminal_run <= 2);
        current = segment.end;
    }
    assert_eq!(
        current,
        State {
            n: 878,
            q: 215,
            r: 55
        }
    );
}
