//! Per-start scan: compute the stabilization index t(m) and increment c(m)
//! for every m in a range. Parallel, deterministic, checkpointed, resumable.
//!
//! Output CSV columns: m,t,c,b_t   (b_t = c*(t+1), stored for cross-checking)
//!
//! Determinism: the output is written strictly in increasing m order regardless
//! of thread count, and the FNV digest covers the numeric triples only, so runs
//! with different --threads / --block must produce identical digests.

use conjecture::cli::{now, Args};
use conjecture::{solve_fast, Fnv, Outcome};
use std::fs::{File, OpenOptions};
use std::io::{BufWriter, Write};
use std::path::Path;

fn main() {
    let a = Args::parse();
    let lo = a.u64("lo", 1);
    let hi = a.u64("hi", 200_000);
    let max_n = a.u64("max-n", 20_000_000);
    let threads = a.usize("threads", std::thread::available_parallelism().map(|v| v.get()).unwrap_or(4));
    let block = a.usize("block", 20_000);
    let out_path = a.str("out", "../data/scan.csv");
    let ckpt_path = a.str("checkpoint", "");

    // ---- resume -----------------------------------------------------------
    let mut start = lo;
    let mut append = false;
    if !ckpt_path.is_empty() {
        if let Ok(txt) = std::fs::read_to_string(&ckpt_path) {
            if let Some(done) = txt.trim().split(',').next().and_then(|s| s.parse::<u64>().ok()) {
                if done >= lo && done < hi {
                    start = done + 1;
                    append = true;
                    eprintln!("[scan] resuming from m={start} (checkpoint {ckpt_path})");
                } else if done >= hi {
                    eprintln!("[scan] checkpoint says range already complete");
                    return;
                }
            }
        }
    }

    let file = if append && Path::new(&out_path).exists() {
        OpenOptions::new().append(true).open(&out_path).expect("open out for append")
    } else {
        let f = File::create(&out_path).expect("create out");
        let mut w = BufWriter::new(&f);
        writeln!(w, "m,t,c,b_t").unwrap();
        w.flush().unwrap();
        drop(w);
        OpenOptions::new().append(true).open(&out_path).expect("reopen out")
    };
    let mut w = BufWriter::with_capacity(1 << 20, file);

    // ---- scan -------------------------------------------------------------
    let t0 = now();
    let mut digest = Fnv::default();
    let mut max_t = 0u64;
    let mut max_t_m = 0u64;
    let mut max_c = 0u64;
    let mut max_c_m = 0u64;
    let mut unresolved: Vec<u64> = Vec::new();
    let mut total_rows: u64 = 0;

    let mut bstart = start;
    while bstart <= hi {
        let bend = (bstart + block as u64 - 1).min(hi);
        let results = solve_block(bstart, bend, max_n, threads);

        for (i, out) in results.iter().enumerate() {
            let m = bstart + i as u64;
            match *out {
                Outcome::Stabilized { t, c } => {
                    let bt = c * (t + 1);
                    writeln!(w, "{m},{t},{c},{bt}").unwrap();
                    digest.write_u64(m);
                    digest.write_u64(t);
                    digest.write_u64(c);
                    total_rows += 1;
                    if t > max_t {
                        max_t = t;
                        max_t_m = m;
                    }
                    if c > max_c {
                        max_c = c;
                        max_c_m = m;
                    }
                }
                Outcome::Unresolved { state } => {
                    writeln!(w, "{m},UNRESOLVED,{},{}", state.q, state.b()).unwrap();
                    unresolved.push(m);
                }
            }
        }
        w.flush().unwrap();
        if !ckpt_path.is_empty() {
            write_checkpoint(&ckpt_path, bend, digest.0, max_t, max_t_m);
        }
        let el = now() - t0;
        eprintln!(
            "[scan] m<={bend} ({:.1}%)  elapsed {el:.1}s  max_t={max_t} at m={max_t_m}  unresolved={}",
            100.0 * (bend - start + 1) as f64 / (hi - start + 1).max(1) as f64,
            unresolved.len()
        );
        bstart = bend + 1;
    }
    w.flush().unwrap();

    println!("range              : {lo}..={hi}  (this run started at {start})");
    println!("max-n cap          : {max_n}");
    println!("rows written       : {total_rows}");
    println!("unresolved         : {}", unresolved.len());
    if !unresolved.is_empty() {
        println!("unresolved starts  : {:?}", &unresolved[..unresolved.len().min(50)]);
    }
    println!("longest t(m)       : t={max_t} at m={max_t_m}");
    println!("largest c(m)       : c={max_c} at m={max_c_m}");
    println!("fnv1a64 digest     : {:#018x}", digest.0);
    println!("elapsed seconds    : {:.2}", now() - t0);
}

fn write_checkpoint(path: &str, done: u64, digest: u64, max_t: u64, max_t_m: u64) {
    let tmp = format!("{path}.tmp");
    std::fs::write(&tmp, format!("{done},{digest:#018x},{max_t},{max_t_m}\n")).expect("write ckpt");
    let _ = std::fs::remove_file(path);
    std::fs::rename(&tmp, path).expect("rename ckpt");
}

/// Solve `lo..=hi` across `threads` workers; results returned in m order.
fn solve_block(lo: u64, hi: u64, max_n: u64, threads: usize) -> Vec<Outcome> {
    let len = (hi - lo + 1) as usize;
    let mut out: Vec<Outcome> = vec![Outcome::Stabilized { t: 0, c: 0 }; len];
    let nthreads = threads.max(1).min(len.max(1));
    let chunk = len.div_ceil(nthreads);

    std::thread::scope(|s| {
        for (ci, slice) in out.chunks_mut(chunk).enumerate() {
            let base = lo + (ci * chunk) as u64;
            s.spawn(move || {
                for (j, cell) in slice.iter_mut().enumerate() {
                    *cell = solve_fast(base + j as u64, max_n);
                }
            });
        }
    });
    out
}
