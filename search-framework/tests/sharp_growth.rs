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
