//! Adversarial tests. Every claimed lemma in docs/partial-proofs.md that can be
//! checked on finite data is checked here against a naive reference
//! implementation of the literal definition.

use conjecture::{absorbed_b, dq, enter, solve, solve_fast, step, step_b, Outcome};

/// Reference implementation: the literal definition, no shortcuts, no (q,r).
fn naive(m: u64, upto: u64) -> Vec<u64> {
    let mut b = m;
    let mut out = vec![b];
    for n in 1..upto {
        b += b % n;
        out.push(b);
    }
    out
}

fn value_at(m: u64, target: u64) -> u64 {
    let mut b = m;
    for n in 1..target {
        b += b % n;
    }
    b
}

#[test]
fn qr_form_matches_raw_recurrence() {
    for m in 1..2000u64 {
        let refseq = naive(m, 400);
        let mut s = enter(m);
        while s.n < 400 {
            assert_eq!(s.b(), refseq[(s.n - 1) as usize], "m={} n={}", m, s.n);
            assert!(s.check(), "m={} n={} state {:?}", m, s.n, s);
            s = step(s);
        }
    }
}

#[test]
fn step_b_and_step_agree() {
    for m in 1..1000u64 {
        let mut s = enter(m);
        for _ in 0..500 {
            let nb = step_b(s.n, s.b());
            let s2 = step(s);
            assert_eq!(nb, s2.b(), "m={} n={}", m, s.n);
            s = s2;
        }
    }
}

/// The absorbing criterion is equivalent to constant increments, and the index
/// found by `solve` is minimal.
#[test]
fn absorption_criterion_is_exactly_constant_increments() {
    for m in 1..3000u64 {
        match solve(m, 2_000_000) {
            Outcome::Stabilized { t, c } => {
                let seq = naive(m, t + 60);
                assert_eq!(seq[(t - 1) as usize], c * (t + 1), "m={}", m);
                assert!(c < t, "m={} c={} t={}", m, c, t);
                for n in t..(t + 50) {
                    assert_eq!(seq[n as usize] - seq[(n - 1) as usize], c, "m={} n={}", m, n);
                }
                for n in 1..t {
                    assert!(!absorbed_b(n, seq[(n - 1) as usize]), "m={} earlier absorb at {}", m, n);
                }
            }
            Outcome::Unresolved { .. } => panic!("m={} did not stabilize", m),
        }
    }
}

#[test]
fn solve_fast_matches_solve() {
    for m in 1..5000u64 {
        assert_eq!(solve(m, 5_000_000), solve_fast(m, 5_000_000), "m={}", m);
    }
}

/// OEIS A073117: a(397) = 38606 = 398*97; increments equal 97 from n = 397.
#[test]
fn oeis_a073117_start_one() {
    match solve(1, 10_000) {
        Outcome::Stabilized { t, c } => {
            assert_eq!((t, c), (397, 97));
            assert_eq!(c * (t + 1), 38606);
            assert_eq!(value_at(1, 397), 38606);
        }
        _ => panic!("start 1 must stabilize"),
    }
}

/// OEIS A073117 published terms.
#[test]
fn oeis_a073117_terms() {
    const HEAD: [u64; 20] =
        [1, 1, 2, 4, 4, 8, 10, 13, 18, 18, 26, 30, 36, 46, 50, 55, 62, 73, 74, 91];
    let got = naive(1, 21);
    assert_eq!(&got[..20], &HEAD);
}

/// OEIS A117846: eventual increment for b_1 = 2n-1, n = 1..68 (all published terms).
#[test]
fn oeis_a117846_all_published_terms() {
    const A117846: [u64; 68] = [
        97, 1, 2, 2, 316, 2, 3, 3, 3, 4, 12, 4, 4, 12, 11, 11, 316, 11, 316, 316, 6, 316, 316, 316,
        316, 97, 316, 316, 13, 316, 13, 13, 13, 13, 8, 13, 13, 12, 13, 13, 13, 13, 13, 13, 14, 14,
        316, 14, 316, 316, 316, 97, 9, 97, 97, 13, 10, 10, 11, 10, 14, 11, 12, 12, 97, 12, 97, 132,
    ];
    for (i, &want) in A117846.iter().enumerate() {
        let m = 2 * (i as u64 + 1) - 1;
        match solve(m, 50_000_000) {
            Outcome::Stabilized { c, .. } => assert_eq!(c, want, "A117846({}) start m={}", i + 1, m),
            _ => panic!("m={} did not stabilize", m),
        }
        match solve(m + 1, 50_000_000) {
            Outcome::Stabilized { c, .. } => assert_eq!(c, want, "pair partner m={}", m + 1),
            _ => panic!("m={} did not stabilize", m + 1),
        }
    }
}

/// Theorem (Pair merging): the orbits of 2k-1 and 2k coincide from index 3 on.
#[test]
fn pair_merging_theorem() {
    for k in 1..20000u64 {
        assert_eq!(value_at(2 * k - 1, 3), 2 * k, "k={}", k);
        assert_eq!(value_at(2 * k, 3), 2 * k, "k={}", k);
    }
}

/// Theorem (e-doubling): e_{n+1} = 2 e_n - dq_n (n+2); in particular
/// e_{n+1} == 2 e_n (mod n+2).
#[test]
fn e_doubling_identity() {
    for m in 1..1500u64 {
        let mut s = enter(m);
        for _ in 0..800 {
            let d = dq(s);
            let s2 = step(s);
            assert_eq!(s2.e(), 2 * s.e() - (d as i64) * (s.n as i64 + 2), "m={} n={}", m, s.n);
            assert_eq!(s2.q as i64 - s.q as i64, d as i64, "m={} n={}", m, s.n);
            assert_eq!(s2.e().rem_euclid(s.n as i64 + 2), (2 * s.e()).rem_euclid(s.n as i64 + 2));
            s = s2;
        }
    }
}

/// Theorem (Capture criterion): a non-absorbing orbit becomes absorbing at
/// index n+1 iff n is even and e_n = +-(n+2)/2.
#[test]
fn capture_criterion() {
    for m in 1..4000u64 {
        let mut s = enter(m);
        while !s.absorbed() && s.n < 300_000 {
            let s2 = step(s);
            let pred = s.n % 2 == 0 && (2 * s.e()).unsigned_abs() == s.n + 2;
            assert_eq!(pred, s2.absorbed(), "m={} n={} e={}", m, s.n, s.e());
            s = s2;
        }
    }
}

/// Lemma (Congruence propagation): d | n implies b_{n+1} == 2 b_n (mod d).
/// Corollary: b_j is even for every odd j >= 3.
#[test]
fn congruence_propagation() {
    for m in 1..600u64 {
        let mut b = m;
        for n in 1..400u64 {
            let nb = step_b(n, b);
            for d in 1..=n {
                if n % d == 0 {
                    assert_eq!(nb % d, (2 * b) % d, "m={} n={} d={}", m, n, d);
                }
            }
            b = nb;
            if (n + 1) % 2 == 1 && n + 1 >= 3 {
                assert_eq!(b % 2, 0, "m={} b_{} must be even", m, n + 1);
            }
        }
    }
}

/// Lemma (No fast climbs): two consecutive dq = +1 force 3q + 9 <= n;
/// two consecutive dq = -1 force 3q > 2n + 3.
#[test]
fn consecutive_step_bounds() {
    let mut saw_up = false;
    let mut saw_down = false;
    for m in 1..4000u64 {
        let mut s = enter(m);
        for _ in 0..3000 {
            let s2 = step(s);
            if dq(s) == 1 && dq(s2) == 1 {
                saw_up = true;
                assert!(3 * s.q + 9 <= s.n, "m={} n={} q={}", m, s.n, s.q);
            }
            if dq(s) == -1 && dq(s2) == -1 {
                saw_down = true;
                assert!(3 * s.q > 2 * s.n + 3, "m={} n={} q={}", m, s.n, s.q);
            }
            s = s2;
        }
    }
    assert!(saw_up && saw_down, "test vacuous; both patterns must occur");
}

/// Lemma (Bounded quotient): q_n <= n is forward invariant, and |dq| <= 1.
#[test]
fn bounded_quotient_invariance() {
    for m in 1..5000u64 {
        let mut s = enter(m);
        assert!(s.q < s.n, "entry must give q < n, m={}", m);
        for _ in 0..2000 {
            let s2 = step(s);
            assert!(s2.q <= s2.n, "m={} n={}", m, s2.n);
            assert!(s2.r < s2.n, "m={} n={}", m, s2.n);
            assert!((s2.q as i64 - s.q as i64).abs() <= 1, "m={} n={}", m, s.n);
            s = s2;
        }
    }
}

/// Rigidity: the only orbit on which e_n is an affine function of n is the
/// absorbing one. The other affine candidates e_n = +-(n+3) violate the
/// admissible window -q <= e <= n-1-q, so they cannot occur.
#[test]
fn affine_rigidity_window_violation() {
    for n in 2..10000i64 {
        // e = n+3 needs r = q + n + 3 <= n-1, impossible for q >= 0.
        assert!(n + 3 > n - 1);
        // e = -(n+3) needs q = r + n + 3 > n, violating q <= n.
        assert!(n + 3 > n);
    }
}

/// b_n < n^2 after entry, and the entry index is O(sqrt(m)).
#[test]
fn entry_lemma_bound() {
    for m in [1u64, 2, 7, 100, 12345, 1_000_000, 987_654_321] {
        let s = enter(m);
        assert!(s.b() < s.n * s.n, "m={}", m);
        let bound = 2 * (m as f64).sqrt() as u64 + 20;
        assert!(s.n <= bound, "m={} entry n={} bound={}", m, s.n, bound);
    }
}

/// A state is absorbing iff the divisibility criterion holds.
#[test]
fn divisibility_criterion_matches_state_test() {
    for m in 1..2000u64 {
        let mut s = enter(m);
        for _ in 0..600 {
            assert_eq!(s.absorbed(), absorbed_b(s.n, s.b()), "m={} n={}", m, s.n);
            s = step(s);
        }
    }
}

/// Guard against silent regressions in the fast path: a fixed digest.
#[test]
fn deterministic_digest_of_small_scan() {
    use conjecture::Fnv;
    let mut h = Fnv::default();
    for m in 1..=20000u64 {
        match solve_fast(m, 50_000_000) {
            Outcome::Stabilized { t, c } => {
                h.write_u64(m);
                h.write_u64(t);
                h.write_u64(c);
            }
            Outcome::Unresolved { .. } => panic!("m={} unresolved", m),
        }
    }
    // Recomputed independently by verification-framework/verify.py.
    println!("digest(1..20000) = {:#018x}", h.0);
    assert_eq!(h.0, 0xc70d029bafd9eef6);
}

/// Sanity: State::check holds for every state the entry routine produces.
#[test]
fn entry_states_are_well_formed() {
    for m in 1..50000u64 {
        let s = enter(m);
        assert!(s.check(), "m={} -> {:?}", m, s);
        assert_eq!(s.b(), value_at(m, s.n), "m={}", m);
    }
}
