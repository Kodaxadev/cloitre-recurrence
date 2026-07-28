//! INDEPENDENT verifier. Shares no code with the search framework.
//!
//! Differences that make a shared bug unlikely:
//!   * raw b-recurrence  b <- b + (b mod n)  -- no (q,r) coordinates at all
//!   * u128 arithmetic   -- different width from the u64 search framework
//!   * absorption tested by the *definition* (increments constant for a stretch)
//!     as well as by the divisibility criterion, and the two must agree
//!   * no early-exit prologue: every index from 1 is examined
//!
//! Usage:
//!   verify --csv ../data/scan_200k.csv [--stride 1] [--threads 16] [--tail 64]
//!   verify --selftest

use std::fs;
use std::sync::atomic::{AtomicU64, Ordering};

#[derive(Clone, Copy, Debug)]
struct Row {
    m: u128,
    t: u128,
    c: u128,
    b_t: u128,
}

/// Recompute from the literal definition and return (first absorbing index,
/// value there), where "absorbing" is tested as: b == c*(n+1) with c < n.
/// Returns None if no absorbing index is found with n <= cap.
fn first_absorbing(m: u128, cap: u128) -> Option<(u128, u128)> {
    let mut b: u128 = m;
    let mut n: u128 = 1;
    loop {
        // absorbing test, straight from the definition of the fixed ray
        let np1 = n + 1;
        if b % np1 == 0 && b / np1 < n {
            return Some((n, b));
        }
        if n >= cap {
            return None;
        }
        b += b % n;
        n += 1;
    }
}

/// Independent confirmation that the increments really are constant: run
/// `tail` extra steps past t and check every difference equals c.
fn increments_constant(m: u128, t: u128, c: u128, tail: u128) -> bool {
    let mut b: u128 = m;
    let mut n: u128 = 1;
    while n < t {
        b += b % n;
        n += 1;
    }
    if b != c * (t + 1) {
        return false;
    }
    for _ in 0..tail {
        let nb = b + b % n;
        if nb - b != c {
            return false;
        }
        b = nb;
        n += 1;
    }
    true
}

fn parse_csv(path: &str) -> Vec<Row> {
    let txt = fs::read_to_string(path).unwrap_or_else(|e| panic!("read {path}: {e}"));
    let mut rows = Vec::new();
    for (i, line) in txt.lines().enumerate() {
        if i == 0 || line.trim().is_empty() {
            continue;
        }
        let f: Vec<&str> = line.split(',').collect();
        assert_eq!(f.len(), 4, "bad row {i}: {line}");
        if f[1] == "UNRESOLVED" {
            panic!("row {i} is UNRESOLVED: {line}");
        }
        rows.push(Row {
            m: f[0].parse().expect("m"),
            t: f[1].parse().expect("t"),
            c: f[2].parse().expect("c"),
            b_t: f[3].parse().expect("b_t"),
        });
    }
    rows
}

fn selftest() {
    // OEIS A073117: a(397) = 38606 = 398*97.
    assert_eq!(first_absorbing(1, 100_000), Some((397, 38606)));
    assert!(increments_constant(1, 397, 97, 200));
    // OEIS A117846 first 12 terms, b_1 = 2n-1.
    const A: [u128; 12] = [97, 1, 2, 2, 316, 2, 3, 3, 3, 4, 12, 4];
    for (i, &want) in A.iter().enumerate() {
        let m = 2 * (i as u128 + 1) - 1;
        let (t, b) = first_absorbing(m, 50_000_000).expect("must stabilize");
        assert_eq!(b / (t + 1), want, "A117846({}) m={m}", i + 1);
        assert!(increments_constant(m, t, want, 100));
    }
    // Pair merging: 2k-1 and 2k agree from index 3 on.
    for k in 1..5000u128 {
        let f = |mut b: u128| {
            for n in 1..3u128 {
                b += b % n;
            }
            b
        };
        assert_eq!(f(2 * k - 1), 2 * k);
        assert_eq!(f(2 * k), 2 * k);
    }
    println!("selftest: OK (A073117, A117846 x12, pair merging)");
}

fn main() {
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let get = |k: &str, d: &str| -> String {
        argv.iter()
            .position(|a| a == &format!("--{k}"))
            .and_then(|i| argv.get(i + 1))
            .cloned()
            .unwrap_or_else(|| d.to_string())
    };
    if argv.iter().any(|a| a == "--selftest") {
        selftest();
        return;
    }

    let csv = get("csv", "../data/scan_200k.csv");
    let stride: usize = get("stride", "1").parse().unwrap();
    let tail: u128 = get("tail", "64").parse().unwrap();
    let threads: usize = get("threads", "16").parse().unwrap();

    selftest();
    let rows = parse_csv(&csv);
    println!("verifying {} rows from {csv} (stride {stride}, tail {tail})", rows.len());

    let checked = AtomicU64::new(0);
    let bad = AtomicU64::new(0);
    let sel: Vec<Row> = rows.iter().copied().step_by(stride).collect();
    let total = sel.len();
    let chunk = total.div_ceil(threads.max(1));

    std::thread::scope(|s| {
        for part in sel.chunks(chunk) {
            let checked = &checked;
            let bad = &bad;
            s.spawn(move || {
                for row in part {
                    let mut ok = true;
                    // 1. claimed value is consistent with the claimed pair
                    if row.b_t != row.c * (row.t + 1) {
                        eprintln!("m={}: b_t != c*(t+1)", row.m);
                        ok = false;
                    }
                    // 2. c < t is required for absorption
                    if row.c >= row.t {
                        eprintln!("m={}: c >= t", row.m);
                        ok = false;
                    }
                    // 3. independent recomputation of the FIRST absorbing index
                    match first_absorbing(row.m, row.t + 1) {
                        Some((t2, b2)) => {
                            if t2 != row.t || b2 != row.b_t {
                                eprintln!("m={}: recomputed (t,b)=({t2},{b2}) vs ({},{})", row.m, row.t, row.b_t);
                                ok = false;
                            }
                        }
                        None => {
                            eprintln!("m={}: no absorbing index found up to t", row.m);
                            ok = false;
                        }
                    }
                    // 4. increments really are constant past t
                    if !increments_constant(row.m, row.t, row.c, tail) {
                        eprintln!("m={}: increments not constant past t", row.m);
                        ok = false;
                    }
                    if !ok {
                        bad.fetch_add(1, Ordering::Relaxed);
                    }
                    let d = checked.fetch_add(1, Ordering::Relaxed) + 1;
                    if d % 20_000 == 0 {
                        eprintln!("[verify] {d}/{total} rows");
                    }
                }
            });
        }
    });

    let c = checked.load(Ordering::Relaxed);
    let b = bad.load(Ordering::Relaxed);
    println!("rows checked : {c}");
    println!("rows FAILED  : {b}");
    if b == 0 {
        println!("VERDICT: every checked row independently confirmed.");
    } else {
        println!("VERDICT: MISMATCH -- the search framework result is not trustworthy.");
        std::process::exit(1);
    }
}
