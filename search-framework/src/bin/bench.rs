//! Head-to-head timing of the three ways to iterate the recurrence, over an
//! identical workload. All three must return identical results; the binary
//! asserts that, so a faster-but-wrong variant cannot be reported as a win.

use conjecture::cli::{now, Args};
use conjecture::{enter, solve_fast, Outcome};

/// Baseline: the literal definition in u64, one division per step.
fn solve_bform(m: u64, max_n: u64) -> Outcome {
    let mut b = m;
    let mut n = 1u64;
    loop {
        let np1 = n + 1;
        if b % np1 == 0 && b / np1 < n {
            return Outcome::Stabilized { t: n, c: b / np1 };
        }
        if n >= max_n {
            let s = enter(m);
            return Outcome::Unresolved { state: s };
        }
        b += b % n;
        n += 1;
    }
}

/// Same, but with the absorption test done only via a single modulo.
fn solve_bform_lean(m: u64, max_n: u64) -> Outcome {
    let mut b = m;
    let mut n = 1u64;
    loop {
        let r = b % n;
        if n > 1 && r == b / n {
            return Outcome::Stabilized { t: n, c: r };
        }
        if n >= max_n {
            return Outcome::Unresolved { state: enter(m) };
        }
        b += r;
        n += 1;
    }
}

fn main() {
    let a = Args::parse();
    let lo = a.u64("lo", 1);
    let hi = a.u64("hi", 20_000);
    let max_n = a.u64("max-n", 50_000_000);

    let variants: [(&str, fn(u64, u64) -> Outcome); 3] = [
        ("b-form, 2 divisions/step", solve_bform),
        ("b-form, 1 division/step", solve_bform_lean),
        ("(q,r)-form, DIVISION-FREE", solve_fast),
    ];

    let mut steps_total: u128 = 0;
    let mut reference: Vec<Outcome> = Vec::new();
    let mut timings = Vec::new();

    for (name, f) in variants {
        let t0 = now();
        let mut out = Vec::with_capacity((hi - lo + 1) as usize);
        for m in lo..=hi {
            out.push(f(m, max_n));
        }
        let el = now() - t0;
        if reference.is_empty() {
            steps_total = out
                .iter()
                .map(|o| match o {
                    Outcome::Stabilized { t, .. } => *t as u128,
                    _ => 0,
                })
                .sum();
            reference = out;
        } else {
            assert_eq!(out, reference, "variant '{name}' disagrees with the baseline");
        }
        timings.push((name, el));
    }

    println!("workload: starts {lo}..={hi}, total iterations {steps_total}");
    println!("{:<30} {:>10} {:>14} {:>10}", "variant", "seconds", "ns/step", "speedup");
    let base = timings[0].1;
    for (name, el) in &timings {
        println!(
            "{:<30} {:>10.3} {:>14.3} {:>9.2}x",
            name,
            el,
            el * 1e9 / steps_total as f64,
            base / el
        );
    }
    println!("\nall variants produced identical results ({} orbits)", reference.len());
}
