//! Regression tests for the structural theorems in partial-proofs.md that were
//! discovered in this project. These are the load-bearing claims, so each is
//! tested against the literal orbit rather than against derived quantities.

use conjecture::{dq, enter, solve, step, Outcome, State};
use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

/// Recompute the proof-chain quantities of Theorem 18 straight from the orbit:
/// n0 = entry index, n* = max{n >= n0 : 3q_n > n+1}, plus (t, c).
fn witnesses(m: u64) -> (u64, Option<(u64, u64)>, u64, u64) {
    let mut b = m;
    let mut n = 2u64;
    let mut n0 = None;
    let mut nstar: Option<(u64, u64)> = None;
    loop {
        let (q, r) = (b / n, b % n);
        if n0.is_none() && b < n * n {
            n0 = Some(n);
        }
        if n0.is_some() && 3 * q > n + 1 {
            nstar = Some((n, b));
        }
        if q == r {
            return (n0.unwrap(), nstar, n, q);
        }
        b += r;
        n += 1;
    }
}

/// Theorem 18 (sharpened): c(m) = c implies m < (c+3)(3c+5).
#[test]
fn theorem18_increment_bounds_the_start() {
    let mut worst = 0.0f64;
    for m in 1..200_000u64 {
        match solve(m, 50_000_000) {
            Outcome::Stabilized { c, .. } => {
                let bound = (c + 3) * (3 * c + 5);
                assert!(m < bound, "m={m} c={c} bound={bound}");
                worst = worst.max(m as f64 / bound as f64);
            }
            Outcome::Unresolved { .. } => panic!("m={m} unresolved"),
        }
    }
    // Guard against the bound silently becoming vacuous if the proof is edited.
    assert!(worst > 0.3, "bound looks vacuous: worst ratio only {worst}");
}

/// Every intermediate link of the Theorem 18 proof chain.
#[test]
fn theorem18_proof_chain_links() {
    for m in 1..20_000u64 {
        let (n0, nstar, t, c) = witnesses(m);
        assert!(n0 >= 2);
        if let Some((ns, b_ns)) = nstar {
            assert!(ns >= n0, "m={m}: n*={ns} < n0={n0}");
            assert!(ns < 3 * c + 5, "m={m}: n*={ns} not < {}", 3 * c + 5);
            // sharpened link: q(n*) <= c+2, hence b(n*) < (c+3)*n*
            assert!(b_ns < (c + 3) * ns, "m={m}: b(n*)={b_ns} not < {}", (c + 3) * ns);
            assert!(m <= b_ns, "m={m}: m > b(n*)={b_ns}");
        } else {
            // Case S = empty: the ratchet runs from n0, so q_(n0) <= c+1.
            let s = enter(m);
            assert_eq!(s.n, n0);
            assert!(s.q <= c + 1, "m={m}: q(n0)={} > c+1={}", s.q, c + 1);
        }
        assert!(c < t);
    }
}

/// Theorem 13 (Forced rebound): dq = -1 and 3q <= n+1 force the next step to +1.
#[test]
fn theorem13_forced_rebound() {
    let mut hits = 0u64;
    for m in 1..6000u64 {
        let mut s = enter(m);
        for _ in 0..4000 {
            let s2 = step(s);
            if dq(s) == -1 && 3 * s.q <= s.n + 1 {
                hits += 1;
                assert_eq!(dq(s2), 1, "m={} n={} q={} r={}", m, s.n, s.q, s.r);
            }
            s = s2;
        }
    }
    assert!(hits > 100_000, "test too weak: only {hits} applicable steps");
}

/// Theorem 14 (Ratchet): while 3q <= n+1 holds, q never drops more than 1 below
/// its value at the window start, and every drop is undone immediately.
#[test]
fn theorem14_ratchet() {
    for m in 1..6000u64 {
        let mut s = enter(m);
        let mut window: Option<State> = None;
        for _ in 0..4000 {
            if 3 * s.q <= s.n + 1 {
                match window {
                    None => window = Some(s),
                    Some(w) => assert!(s.q + 1 >= w.q, "m={m}: q={} fell below q0-1={}", s.q, w.q - 1),
                }
            } else {
                window = None;
            }
            if s.absorbed() {
                break;
            }
            s = step(s);
        }
    }
}

/// Corollary 20: the excluded increments really are absent, and Theorem 18
/// places their whole search range inside the scanned interval.
#[test]
fn corollary20_excluded_increments() {
    const EXCLUDED: [u64; 13] = [5, 7, 25, 38, 39, 47, 48, 88, 90, 91, 118, 143, 144];
    let mut seen = std::collections::HashSet::new();
    let limit = EXCLUDED.iter().map(|&c| (c + 3) * (3 * c + 5)).max().unwrap();
    assert!(limit <= 200_000, "search range {limit} exceeds what this test scans");
    for m in 1..=limit {
        if let Outcome::Stabilized { c, .. } = solve(m, 50_000_000) {
            seen.insert(c);
        }
    }
    for &c in &EXCLUDED {
        assert!(!seen.contains(&c), "c={c} was supposed to be unattainable");
    }
    // Control: neighbouring values ARE attained, so the test is not vacuous.
    for &c in &[4u64, 6, 8, 24, 26] {
        assert!(seen.contains(&c), "control value c={c} should be attained");
    }
}

/// Lemma 21: at the first index n >= 3 with b_n < n^2, the quotient is on
/// the entry ridge q_n in {n-2, n-1}.
#[test]
fn entry_ridge_has_only_two_quotient_levels() {
    for m in 1..=200_000u64 {
        let mut n = 2u64;
        let mut b = m;
        while b >= n * n {
            b += b % n;
            n += 1;
        }
        if n >= 3 {
            let q = b / n;
            assert!(
                q == n - 2 || q == n - 1,
                "m={m}: first entry at n={n}, b={b}, q={q}"
            );
            assert!((n - 1) * (n - 1) <= b);
        }
    }
}

/// Theorem 22: after a down-step, the exact deficit formula predicts each
/// subsequent forced up-step. This checks arbitrary admissible states rather
/// than only states reached from b_1=m.
#[test]
fn exact_rebound_cascade() {
    let mut two_step_cascades = 0u64;
    for n in 2..=160u64 {
        for q in 0..=n {
            for r in 0..n {
                let s = State { n, q, r };
                if dq(s) != -1 {
                    continue;
                }
                let h = q - 2 * r;
                let mut current = step(s);
                for k in 0..6u32 {
                    let power = 1i128 << (k + 1);
                    let threshold =
                        power * (h + q + 2) as i128 - q as i128 - 2 * k as i128 - 4;
                    let predicted_up = (n + 1) as i128 >= threshold;
                    assert_eq!(
                        dq(current) == 1,
                        predicted_up,
                        "n={n} q={q} r={r} h={h} k={k}"
                    );
                    if !predicted_up {
                        break;
                    }
                    if k == 1 {
                        two_step_cascades += 1;
                    }
                    current = step(current);
                }
            }
        }
    }
    assert!(two_step_cascades > 10_000, "cascade test too weak");
}

/// Lemma 26: before absorption, a run of zero quotient changes cannot be
/// longer than floor(log2 of the ending index).
#[test]
fn zero_quotient_run_is_logarithmically_bounded() {
    for m in 1..=4000u64 {
        let mut s = enter(m);
        let n0 = s.n;
        let mut run = 0u32;
        for _ in 0..20_000 {
            if s.absorbed() {
                break;
            }
            if s.n >= 4 {
                let h = 63 - s.n.leading_zeros() as u64;
                let scale = h + 1;
                assert!(
                    3 * scale * s.q + scale * n0 + 9 * scale >= s.n,
                    "m={m} n={} q={} n0={n0} H={h}",
                    s.n,
                    s.q
                );
            }
            if dq(s) == 0 {
                run += 1;
            } else {
                run = 0;
            }
            s = step(s);
            if run > 0 {
                assert!(
                    (1u128 << run) <= s.n as u128,
                    "m={m} n={} zero_run={run}",
                    s.n
                );
            }
        }
    }
}

/// Lemma 40's local core: a positive state whose next digit is not down and
/// whose next e stays positive follows least-residue doubling and lies outside
/// the danger interval.
#[test]
fn positive_monotone_step_is_moving_modulus_doubling() {
    let mut checked = 0u64;
    for n in 2..=300u64 {
        for q in 0..=n {
            for r in q.saturating_add(1)..n {
                let state = State { n, q, r };
                let digit = dq(state);
                if digit == -1 {
                    continue;
                }
                let next = step(state);
                if next.e() <= 0 {
                    continue;
                }
                let twice_e = 2 * state.e();
                let modulus = (n + 2) as i64;
                assert_eq!(next.e(), twice_e.rem_euclid(modulus));
                assert!(
                    twice_e < (n + 1 - q) as i64 || twice_e > modulus,
                    "danger interval entered at {state:?}"
                );
                checked += 1;
            }
        }
    }
    assert!(checked > 1_000_000, "local test too weak: {checked}");
}

/// Lemma 41: lowering the starting quotient to zero preserves every positive
/// no-down transition of the larger-quotient state.
#[test]
fn quotient_zero_dominates_positive_no_down_paths() {
    for n in 3..=100u64 {
        for e in 1..n {
            for q in 0..n - e {
                let mut larger = State {
                    n,
                    q,
                    r: q + e,
                };
                let mut zero = State { n, q: 0, r: e };
                for _ in 0..500 {
                    if larger.absorbed() || dq(larger) == -1 {
                        break;
                    }
                    let larger_next = step(larger);
                    if larger_next.e() <= 0 {
                        break;
                    }
                    assert_ne!(dq(zero), -1, "zero quotient failed first");
                    let zero_next = step(zero);
                    assert_eq!(zero_next.e(), larger_next.e());
                    assert_eq!(larger_next.q - zero_next.q, q);
                    assert!(zero_next.e() > 0);
                    larger = larger_next;
                    zero = zero_next;
                }
            }
        }
    }
}

/// Lemmas 42--43: the safe map agrees with the original recurrence, and its
/// `(e,h,U)` form is the claimed binary-Euclidean transformation.
#[test]
fn safe_map_matches_recurrence_and_gap_coordinates() {
    for n0 in 3..=150u64 {
        for e0 in 1..n0 {
            let mut safe = SafeState {
                e: e0,
                w: n0,
                wraps: 0,
            };
            for _ in 0..1_000 {
                let original = State {
                    n: safe.n(),
                    q: safe.wraps,
                    r: safe.wraps + safe.e,
                };
                let h = safe.h();
                match safe_step(safe) {
                    SafeOutcome::Continue { state, digit } => {
                        let next = step(original);
                        assert_eq!(next.e(), state.e as i64);
                        assert_eq!(next.q, state.wraps);
                        assert!(next.e() > 0);
                        match digit {
                            SafeDigit::Zero => {
                                assert!(safe.e <= h);
                                assert_eq!(state.e, 2 * safe.e);
                                assert_eq!(state.h(), h - safe.e + 1);
                            }
                            SafeDigit::Wrap => {
                                assert!(safe.e > h + safe.wraps + 2);
                                assert_eq!(
                                    state.e,
                                    safe.e - h - safe.wraps - 2
                                );
                                assert_eq!(
                                    state.h(),
                                    2 * h + safe.wraps + 2
                                );
                            }
                        }
                        safe = state;
                    }
                    SafeOutcome::Terminated { capture } => {
                        let next = step(original);
                        assert_eq!(capture, next.e() == 0);
                        assert!(next.e() <= 0);
                        break;
                    }
                }
            }
        }
    }
}

/// Lemma 44: during consecutive wraps, `h + q + 3` doubles exactly.
#[test]
fn positive_wrap_run_has_exact_doubling_coordinate() {
    for n in 3..=300u64 {
        for q in 0..n {
            for e in 1..n - q {
                let mut state = State { n, q, r: q + e };
                let h0 = state.n - state.r;
                let base = h0 + state.q + 3;
                let mut wraps = 0u32;
                while dq(state) == 1 {
                    let next = step(state);
                    if next.e() <= 0 {
                        break;
                    }
                    wraps += 1;
                    state = next;
                    let h = state.n - state.r;
                    assert_eq!(
                        h + state.q + 3,
                        (1u64 << wraps) * base
                    );
                }
            }
        }
    }
}
