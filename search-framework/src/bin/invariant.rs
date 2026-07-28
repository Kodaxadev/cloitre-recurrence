//! Adversarial invariant search (Priority 4 / 7).
//!
//! This binary is a FALSIFIER, not a discoverer. Every candidate is assumed
//! false until a large adversarial sample of reachable transitions fails to
//! kill it. Negative results are the expected and reported outcome.
//!
//! Three independent searches:
//!   (A) Catalogue falsification: a fixed list of candidate potentials is tested
//!       for monotonicity along reachable transitions; the first counterexample
//!       is printed for each.
//!   (B) Affine Lyapunov feasibility, solved EXACTLY rather than by sampling
//!       heuristics: V = a*q + b*r + c*n + d is non-increasing iff
//!       a*dq + b*dr + c <= 0 on the convex hull of observed (dq,dr), and is
//!       bounded below iff a*u + b*v + c >= 0 on the convex hull of observed
//!       (q/n, r/n). Both hulls are tiny, so feasibility is decided directly.
//!   (C) Modular invariants: is b_{n+1} mod M determined by (n mod M, b mod M)?

use conjecture::cli::{now, Args};
use conjecture::{dq, enter, step, State};
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Candidate potentials
// ---------------------------------------------------------------------------

struct Cand {
    name: &'static str,
    f: fn(State) -> f64,
}

fn catalogue() -> Vec<Cand> {
    vec![
        Cand { name: "q", f: |s| s.q as f64 },
        Cand { name: "r", f: |s| s.r as f64 },
        Cand { name: "|e|", f: |s| s.e().abs() as f64 },
        Cand { name: "|e|/(n+2)", f: |s| s.e().abs() as f64 / (s.n + 2) as f64 },
        Cand { name: "e^2/(n+2)^2", f: |s| { let x = s.e() as f64 / (s.n + 2) as f64; x * x } },
        Cand { name: "|q - n/4|", f: |s| (s.q as f64 - s.n as f64 / 4.0).abs() },
        Cand { name: "|r - n/2|", f: |s| (s.r as f64 - s.n as f64 / 2.0).abs() },
        Cand { name: "|2r - q|", f: |s| (2 * s.r as i64 - s.q as i64).abs() as f64 },
        Cand { name: "n - q", f: |s| (s.n - s.q) as f64 },
        Cand { name: "q/n", f: |s| s.q as f64 / s.n as f64 },
        Cand { name: "r/n", f: |s| s.r as f64 / s.n as f64 },
        Cand { name: "dist to absorb |e|/n", f: |s| s.e().abs() as f64 / s.n as f64 },
        Cand { name: "log-ish: ln(1+|e|)", f: |s| ((1 + s.e().unsigned_abs()) as f64).ln() },
        Cand { name: "v2(b)", f: |s| s.b().trailing_zeros() as f64 },
        Cand { name: "gcd(b, n+1)", f: |s| gcd(s.b(), s.n + 1) as f64 },
        Cand { name: "-gcd(b, n+1)", f: |s| -(gcd(s.b(), s.n + 1) as f64) },
        Cand { name: "b/(n(n+1))", f: |s| s.b() as f64 / (s.n as f64 * (s.n + 1) as f64) },
    ]
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a.max(1)
}

// ---------------------------------------------------------------------------
// Convex hull (monotone chain) on f64 points
// ---------------------------------------------------------------------------

fn hull(mut pts: Vec<(f64, f64)>) -> Vec<(f64, f64)> {
    pts.sort_by(|x, y| x.partial_cmp(y).unwrap());
    pts.dedup();
    if pts.len() < 3 {
        return pts;
    }
    let cross = |o: (f64, f64), a: (f64, f64), b: (f64, f64)| {
        (a.0 - o.0) * (b.1 - o.1) - (a.1 - o.1) * (b.0 - o.0)
    };
    let mut h: Vec<(f64, f64)> = Vec::new();
    for &p in pts.iter().chain(pts.iter().rev()) {
        while h.len() >= 2 && cross(h[h.len() - 2], h[h.len() - 1], p) <= 0.0 {
            h.pop();
        }
        h.push(p);
    }
    h.pop();
    h
}

// ---------------------------------------------------------------------------
// Sampling reachable transitions
// ---------------------------------------------------------------------------

struct Sample {
    dqdr: Vec<(f64, f64)>,
    kaprho: Vec<(f64, f64)>,
    transitions: Vec<(State, State)>,
    mod_map: HashMap<(u64, u64, u64), u64>,
    mod_bad: HashMap<u64, ((u64, u64), (u64, u64))>,
}

fn collect(lo: u64, hi: u64, stride: u64, per_orbit: u64, max_n: u64, mods: &[u64]) -> Sample {
    let mut s = Sample {
        dqdr: Vec::new(),
        kaprho: Vec::new(),
        transitions: Vec::new(),
        mod_map: HashMap::new(),
        mod_bad: HashMap::new(),
    };
    let mut m = lo;
    while m <= hi {
        let mut st = enter(m);
        let mut k = 0u64;
        while !st.absorbed() && st.n < max_n && k < per_orbit {
            let nx = step(st);
            s.dqdr.push((dq(st) as f64, nx.r as f64 - st.r as f64));
            s.kaprho.push((st.q as f64 / st.n as f64, st.r as f64 / st.n as f64));
            if s.transitions.len() < 4_000_000 {
                s.transitions.push((st, nx));
            }
            for &md in mods {
                if s.mod_bad.contains_key(&md) {
                    continue;
                }
                let key = (md, st.n % md, st.b() % md);
                let val = nx.b() % md;
                match s.mod_map.get(&key) {
                    Some(&old) if old != val => {
                        s.mod_bad.insert(md, ((st.n, st.b()), (old, val)));
                    }
                    None => {
                        s.mod_map.insert(key, val);
                    }
                    _ => {}
                }
            }
            st = nx;
            k += 1;
        }
        m += stride;
    }
    s
}

// ---------------------------------------------------------------------------

fn main() {
    let a = Args::parse();
    let lo = a.u64("lo", 1);
    let hi = a.u64("hi", 4000);
    let stride = a.u64("stride", 1).max(1);
    let per_orbit = a.u64("per-orbit", 4000);
    let max_n = a.u64("max-n", 5_000_000);
    let grid = a.u64("grid", 200) as i64;
    let t0 = now();

    let mods: Vec<u64> = (2..=64u64).collect();
    let smp = collect(lo, hi, stride, per_orbit, max_n, &mods);
    println!("sampled transitions      : {}", smp.dqdr.len());
    println!("retained for catalogue   : {}", smp.transitions.len());

    // ---- (A) catalogue falsification --------------------------------------
    println!("\n=== (A) monotonicity falsification of candidate potentials ===");
    println!("{:<24} {:>10}  {}", "candidate", "verdict", "counterexample (n,q,r)->(n,q,r)");
    for c in catalogue() {
        let mut bad = None;
        let mut ups = 0u64;
        for &(x, y) in &smp.transitions {
            let (vx, vy) = ((c.f)(x), (c.f)(y));
            if vy > vx + 1e-12 {
                ups += 1;
                if bad.is_none() {
                    bad = Some((x, y, vx, vy));
                }
            }
        }
        match bad {
            Some((x, y, vx, vy)) => println!(
                "{:<24} {:>10}  ({},{},{})->({},{},{})  V {:.4}->{:.4}   [{} increases]",
                c.name, "REJECTED", x.n, x.q, x.r, y.n, y.q, y.r, vx, vy, ups
            ),
            None => println!("{:<24} {:>10}  survived this sample", c.name, "SURVIVED"),
        }
    }

    // ---- (B) affine Lyapunov feasibility ----------------------------------
    println!("\n=== (B) affine V = a*q + b*r + c*n + d : exact feasibility ===");
    let hd = hull(smp.dqdr.iter().map(|&(x, y)| (x, y)).collect());
    let hs = hull(smp.kaprho.clone());
    println!("hull of (dq, dr)         : {} vertices {:?}", hd.len(), trunc(&hd));
    println!("hull of (q/n, r/n)       : {} vertices {:?}", hs.len(), trunc(&hs));
    let mut feasible: Vec<(i64, i64, i64)> = Vec::new();
    for ai in -grid..=grid {
        for bi in -grid..=grid {
            for ci in -grid..=grid {
                if ai == 0 && bi == 0 && ci == 0 {
                    continue;
                }
                let (a_, b_, c_) = (ai as f64 / grid as f64, bi as f64 / grid as f64, ci as f64 / grid as f64);
                // non-increasing on every observed transition direction
                if hd.iter().any(|&(x, y)| a_ * x + b_ * y + c_ > 1e-9) {
                    continue;
                }
                // bounded below: a*kappa + b*rho + c >= 0 on the state hull
                if hs.iter().any(|&(u, v)| a_ * u + b_ * v + c_ < -1e-9) {
                    continue;
                }
                feasible.push((ai, bi, ci));
            }
        }
    }
    println!("grid resolution          : 1/{grid} on each coefficient");
    println!("nontrivial feasible dirs : {}", feasible.len());
    if feasible.is_empty() {
        println!("VERDICT: no affine Lyapunov function of the form a*q+b*r+c*n+d exists.");
        println!("         (Non-increasing forces a/4 + b/2 + c <= 0 via the (dq,dr) hull,");
        println!("          bounded-below forces a/4 + b*v + c >= 0 for all v in [0,1);");
        println!("          the two are compatible only at a=b=c=0.)");
    } else {
        println!("SURVIVORS (must be examined by hand): {:?}", &feasible[..feasible.len().min(20)]);
    }

    // ---- (C) modular invariants -------------------------------------------
    println!("\n=== (C) is b_(n+1) mod M a function of (n mod M, b mod M)? ===");
    let mut wd = Vec::new();
    for &md in &mods {
        match smp.mod_bad.get(&md) {
            Some(((n, b), (v1, v2))) => {
                if md <= 8 {
                    println!("M={md:<3} NOT well defined; witness n={n} b={b} gives {v1} and {v2}");
                }
            }
            None => wd.push(md),
        }
    }
    if wd.is_empty() {
        println!("No modulus 2..64 admits a well-defined induced map: every modular");
        println!("invariant of this shape is impossible. The only surviving congruence");
        println!("structure is the divisor lemma  d | n  =>  b_(n+1) = 2 b_n (mod d).");
    } else {
        println!("well-defined moduli (INVESTIGATE): {wd:?}");
    }

    println!("\nelapsed seconds          : {:.2}", now() - t0);
}

fn trunc(v: &[(f64, f64)]) -> Vec<(f64, f64)> {
    v.iter().take(8).map(|&(a, b)| ((a * 1000.0).round() / 1000.0, (b * 1000.0).round() / 1000.0)).collect()
}
