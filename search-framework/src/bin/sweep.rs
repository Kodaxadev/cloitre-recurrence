//! Compressed verification driver.
//!
//! Advances the SET of distinct reachable values for all starts in [lo,hi]
//! simultaneously. "Every m in [lo,hi] stabilizes by index N" is exactly
//! "the live set is empty at index N", so emptiness is a complete verification
//! of the conjecture on that range -- no per-start bookkeeping required.
//!
//! Reports the work profile so it can be compared against the per-start scan:
//! per-start work is sum over m of t(m); sweep work is sum over n of live(n).

use conjecture::cli::{now, Args};
use conjecture::sweep::Sweep;
use conjecture::Fnv;
use std::fs::File;
use std::io::{BufWriter, Write};

fn main() {
    let a = Args::parse();
    let lo = a.u64("lo", 1);
    let hi = a.u64("hi", 200_000);
    let max_n = a.u64("max-n", 50_000_000);
    let out_path = a.str("out", "");
    let every = a.u64("every", 1);

    let mut w = if out_path.is_empty() {
        None
    } else {
        let f = File::create(&out_path).expect("create out");
        let mut b = BufWriter::with_capacity(1 << 20, f);
        writeln!(b, "n,live_before,absorbed,merged,live_after").unwrap();
        Some(b)
    };

    let t0 = now();
    let mut s = Sweep::new(lo, hi);
    let mut work: u128 = 0;
    let mut merged_total: u64 = 0;
    let mut peak_live = s.live_count();
    let mut digest = Fnv::default();
    let mut last_absorb_n = 0u64;

    while !s.is_empty() && s.n < max_n {
        let st = s.step();
        work += st.live_before as u128;
        merged_total += st.merged as u64;
        peak_live = peak_live.max(st.live_before);
        if st.absorbed > 0 {
            last_absorb_n = st.n;
            digest.write_u64(st.n);
            digest.write_u64(st.absorbed as u64);
        }
        if let Some(b) = w.as_mut() {
            if st.n % every == 0 || st.absorbed > 0 || st.live_after == 0 {
                writeln!(b, "{},{},{},{},{}", st.n, st.live_before, st.absorbed, st.merged, st.live_after)
                    .unwrap();
            }
        }
        if st.n % 200_000 == 0 {
            eprintln!("[sweep] n={} live={} elapsed={:.1}s", st.n, st.live_after, now() - t0);
        }
    }
    if let Some(b) = w.as_mut() {
        b.flush().unwrap();
    }

    let starts = hi - lo + 1;
    println!("range                    : {lo}..={hi}  ({starts} starts)");
    println!("verified empty at index  : {}", if s.is_empty() { s.n.to_string() } else { "NOT EMPTY".into() });
    println!("last index with an absorb: {last_absorb_n}");
    println!("live remaining           : {}", s.live_count());
    if !s.is_empty() {
        let head: Vec<u64> = s.live().iter().copied().take(20).collect();
        println!("surviving values (<=20)  : {head:?}");
    }
    println!("peak distinct live       : {peak_live}");
    println!("total merges             : {merged_total}");
    println!("total absorbed           : {}", s.total_absorbed);
    println!("sweep work (sum of live) : {work}");
    println!("absorb-profile digest    : {:#018x}", digest.0);
    println!("elapsed seconds          : {:.2}", now() - t0);

    // Accounting identity: every start either merged into another orbit or was
    // absorbed. starts = merges + absorbed (+ survivors).
    let accounted = merged_total + s.total_absorbed + s.live_count() as u64;
    println!("accounting  merges+absorbed+live = {accounted}  (must equal {starts})");
    assert_eq!(accounted, starts, "accounting identity violated");
}
