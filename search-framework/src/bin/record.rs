//! Complete orbit census over a start range, via the witness-tracking sweep.
//!
//! Emits one row per DISTINCT orbit: t (absorbing index), c (eventual
//! increment), and the smallest start m reaching it. Because merges are
//! accounted for exactly, `#records + #merges == #starts` is checked, so the
//! census provably covers every start in the range.

use conjecture::cli::{now, Args};
use conjecture::witness::{Record, WitnessSweep};
use conjecture::Fnv;
use std::fs::File;
use std::io::{BufWriter, Write};

fn main() {
    let a = Args::parse();
    let lo = a.u64("lo", 1);
    let hi = a.u64("hi", 1_000_000);
    let max_n = a.u64("max-n", 2_000_000_000);
    let out_path = a.str("out", "");

    let t0 = now();
    let mut s = WitnessSweep::new(lo, hi);
    let mut found: Vec<Record> = Vec::new();
    while !s.is_empty() && s.n < max_n {
        s.step(&mut found);
        if s.n % 5_000_000 == 0 {
            eprintln!("[record] n={} live={} records={} elapsed={:.1}s", s.n, s.live_count(), found.len(), now() - t0);
        }
    }

    // Deterministic order: by absorbing index, then by witness.
    found.sort_unstable_by_key(|r| (r.t, r.witness));

    let mut digest = Fnv::default();
    for r in &found {
        digest.write_u64(r.t);
        digest.write_u64(r.c);
        digest.write_u64(r.witness);
    }

    if !out_path.is_empty() {
        let f = File::create(&out_path).expect("create out");
        let mut w = BufWriter::with_capacity(1 << 20, f);
        writeln!(w, "t,c,witness_m,b_t").unwrap();
        for r in &found {
            writeln!(w, "{},{},{},{}", r.t, r.c, r.witness, r.c * (r.t + 1)).unwrap();
        }
        w.flush().unwrap();
    }

    let starts = hi - lo + 1;
    let acc = found.len() as u64 + s.total_merges + s.live_count() as u64;
    println!("range                    : {lo}..={hi}  ({starts} starts)");
    println!("distinct orbits (records): {}", found.len());
    println!("merges                   : {}", s.total_merges);
    println!("live remaining           : {}", s.live_count());
    println!("accounting records+merges+live = {acc}  (must equal {starts})");
    assert_eq!(acc, starts, "census does not cover the range");
    println!("compression factor       : {:.1}x fewer orbits than starts", starts as f64 / found.len().max(1) as f64);

    if let Some(top) = found.iter().max_by_key(|r| r.t) {
        println!("\nLONGEST stabilization:");
        println!("  t (absorbing index)    : {}", top.t);
        println!("  c (eventual increment) : {}", top.c);
        println!("  smallest start m       : {}", top.witness);
        println!("  b_t = c*(t+1)          : {}", top.c * (top.t + 1));
        println!("  c/t                    : {:.6}   (n^2/4 law predicts 0.25)", top.c as f64 / top.t as f64);
    }
    println!("\ntop 15 by absorbing index:");
    let mut byt = found.clone();
    byt.sort_unstable_by_key(|r| std::cmp::Reverse(r.t));
    println!("{:>14}  {:>13}  {:>12}", "t", "c", "witness m");
    for r in byt.iter().take(15) {
        println!("{:>14}  {:>13}  {:>12}", r.t, r.c, r.witness);
    }
    println!("\ncensus digest            : {:#018x}", digest.0);
    println!("elapsed seconds          : {:.2}", now() - t0);
}
