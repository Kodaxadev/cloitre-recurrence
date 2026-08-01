use conjecture::{dq, enter, step, State};

#[test]
fn parameterized_rebounds_match_literal_transitions() {
    let mut checked = 0u64;
    for n in 2..=160u64 {
        for q in 0..=n {
            for r in 0..n {
                let state = State { n, q, r };
                if dq(state) != -1 {
                    continue;
                }
                for length in 2..=7u32 {
                    if n < (1u64 << (length + 2)) * q {
                        continue;
                    }
                    let mut current = step(state);
                    for _ in 0..length {
                        assert_eq!(dq(current), 1, "n={n} q={q} r={r} length={length}");
                        current = step(current);
                    }
                    checked += 1;
                }
            }
        }
    }
    assert!(checked > 1_000, "cascade test too weak: {checked}");
}

#[test]
fn finite_sharp_growth_bound_holds_on_literal_orbits() {
    let mut checked = 0u64;
    for m in 1..=4_000u64 {
        let mut state = enter(m);
        let entry_n = state.n;
        for _ in 0..20_000 {
            if state.absorbed() {
                break;
            }
            if state.n >= 4 {
                let scale = u128::from(64 - state.n.leading_zeros());
                for length in 2..=7u32 {
                    let numerator = u128::from(length - 1);
                    let denominator = u128::from(length + 1);
                    let cascade_scale = 1u128 << (length + 2);
                    if denominator * scale < numerator * cascade_scale {
                        continue;
                    }
                    assert!(
                        denominator * scale * u128::from(state.q + entry_n + 5)
                            >= numerator * u128::from(state.n),
                        "m={m} n={} q={} n0={entry_n} length={length}",
                        state.n,
                        state.q
                    );
                    checked += 1;
                }
            }
            state = step(state);
        }
    }
    assert!(checked > 100_000, "growth test too weak: {checked}");
}

#[test]
fn explicit_unit_leading_rate_holds_on_record_orbit() {
    let mut state = enter(31_873);
    let entry_n = state.n;
    let mut checked = 0u64;
    for _ in 0..100_000 {
        assert!(
            !state.absorbed(),
            "record orbit absorbed before test horizon"
        );
        let scale = u128::from(64 - state.n.leading_zeros());
        let log_scale = 127 - scale.leading_zeros() as u128;
        if log_scale >= 4 {
            assert!(
                (log_scale - 1) * scale * u128::from(state.q + entry_n + 5)
                    >= (log_scale - 3) * u128::from(state.n),
                "n={} q={} n0={entry_n} L={log_scale}",
                state.n,
                state.q
            );
            checked += 1;
        }
        state = step(state);
    }
    assert!(checked > 50_000, "explicit-rate test too weak: {checked}");
}

#[test]
fn low_window_downstep_charge_holds_on_arbitrary_states() {
    let mut checked = 0u64;
    for initial_n in [128u64, 256, 512] {
        let stride = initial_n / 32;
        for initial_q in 1..=8 {
            for initial_r in (0..initial_n).step_by(stride as usize) {
                let mut state = State {
                    n: initial_n,
                    q: initial_q,
                    r: initial_r,
                };
                let mut counts = [(0u64, 0u64); 6];
                for _ in 0..500 {
                    let change = dq(state);
                    for (offset, count) in counts.iter_mut().enumerate() {
                        let length = offset as u64 + 2;
                        if state.n < (1u64 << (length + 2)) * state.q {
                            *count = (0, 0);
                            continue;
                        }
                        count.0 += u64::from(change != 0);
                        count.1 += u64::from(change == -1);
                        assert!(
                            (length + 1) * count.1 <= count.0 + length,
                            "state={state:?} length={length} counts={count:?}"
                        );
                        checked += 1;
                    }
                    state = step(state);
                }
            }
        }
    }
    assert!(checked > 100_000, "window test too weak: {checked}");
}

#[test]
fn weighted_rebound_budget_holds_on_arbitrary_prefixes() {
    let mut checked = 0u64;
    for initial_n in [128u64, 256, 512] {
        let stride = initial_n / 32;
        for initial_q in 1..=8 {
            for initial_r in (0..initial_n).step_by(stride as usize) {
                let mut state = State {
                    n: initial_n,
                    q: initial_q,
                    r: initial_r,
                };
                let mut ups = 0u64;
                let mut weight = 0u64;
                for _ in 0..500 {
                    let change = dq(state);
                    if change == 1 {
                        ups += 1;
                    } else if change == -1 {
                        assert!(state.q >= 1);
                        weight += (state.n / state.q).ilog2().saturating_sub(2) as u64;
                    }
                    let endpoint_log = (state.n + 1).ilog2() as u64;
                    assert!(
                        weight <= ups + endpoint_log,
                        "state={state:?} weight={weight} ups={ups}"
                    );
                    checked += 1;
                    state = step(state);
                }
            }
        }
    }
    assert!(checked > 300_000, "weighted test too weak: {checked}");
}

#[test]
fn post_down_dyadic_zero_budget_is_exact() {
    let mut checked = 0u64;
    for n in [32u64, 64, 128] {
        for q in 1..=24 {
            for r in 0..(q + 1) / 2 {
                let parent = State { n, q, r };
                assert_eq!(dq(parent), -1);
                let start = step(parent);
                let gap = start.n - start.r;
                assert!((1..=start.q + 1).contains(&gap));

                let mut current = start;
                let mut zeros = Vec::new();
                for offset in 0..60u32 {
                    if current.absorbed() || dq(current) == -1 {
                        break;
                    }
                    if dq(current) == 0 {
                        zeros.push(offset);
                    }
                    current = step(current);
                }

                let length = u32::try_from(current.n - start.n).unwrap();
                let terminal_e = i128::from(current.r) - i128::from(current.q);
                let left = i128::from(start.q + gap + 3) << length;
                let mut right = i128::from(start.n + u64::from(length) + 3) - terminal_e;
                for offset in zeros {
                    right += i128::from(start.n + u64::from(offset) + 2) << (length - offset - 1);
                }
                assert_eq!(left, right, "parent={parent:?} end={current:?}");
                checked += 1;
            }
        }
    }
    assert!(checked > 400, "ridge-budget test too weak: {checked}");
}
