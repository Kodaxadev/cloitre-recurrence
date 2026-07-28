//! Quotient-change epoch analysis (Priority 5).
//!
//! Instead of looking at every iterate, look at the sequence dq_n = q_{n+1}-q_n
//! in {-1,0,+1}. In the rescaled coordinates kappa = q/n and eps = e/n = (r-q)/n
//! the exact recurrence e_{n+1} = 2 e_n - dq_n (n+2) becomes the shift map
//!     eps' = 2 eps - dq,      dq chosen to keep eps' in [-kappa, 1-kappa),
//! i.e. dq_n is literally the n-th DIGIT of the binary expansion of eps in the
//! digit set {-1,0,+1}. If eps equidistributes on that unit interval then
//!     P(dq=-1) = kappa/2,  P(dq=0) = 1/2,  P(dq=+1) = (1-kappa)/2,
//! so E[dq] = (1-2kappa)/2 and the fixed point of kappa' = E[dq] is kappa = 1/4.
//! This binary measures all of those predictions.

use conjecture::cli::{now, Args};
use conjecture::{dq, enter, step, State};
use std::fs::File;
use std::io::{BufWriter, Write};

const RBINS: usize = 20;

#[derive(Default, Clone)]
struct Acc {
    steps: u64,
    dq_count: [u64; 3], // index 0 => -1, 1 => 0, 2 => +1
    pair: [[u64; 3]; 3],
    kappa_sum: f64,
    eps_sum: f64,
    rho_sum: f64,
    rho_hist: [u64; RBINS],
    gap_sum: u64,
    gaps: u64,
    max_gap: u64,
}

impl Acc {
    fn observe(&mut self, s: State, d: i8, prev: Option<i8>) {
        self.steps += 1;
        let di = (d + 1) as usize;
        self.dq_count[di] += 1;
        if let Some(p) = prev {
            self.pair[(p + 1) as usize][di] += 1;
        }
        let n = s.n as f64;
        self.kappa_sum += s.q as f64 / n;
        self.eps_sum += s.e() as f64 / n;
        let rho = s.r as f64 / n;
        self.rho_sum += rho;
        let b = ((rho * RBINS as f64) as usize).min(RBINS - 1);
        self.rho_hist[b] += 1;
    }
    fn merge(&mut self, o: &Acc) {
        self.steps += o.steps;
        for i in 0..3 {
            self.dq_count[i] += o.dq_count[i];
            for j in 0..3 {
                self.pair[i][j] += o.pair[i][j];
            }
        }
        self.kappa_sum += o.kappa_sum;
        self.eps_sum += o.eps_sum;
        self.rho_sum += o.rho_sum;
        for i in 0..RBINS {
            self.rho_hist[i] += o.rho_hist[i];
        }
        self.gap_sum += o.gap_sum;
        self.gaps += o.gaps;
        self.max_gap = self.max_gap.max(o.max_gap);
    }
    fn report(&self, label: &str) {
        if self.steps == 0 {
            println!("[{label}] no steps");
            return;
        }
        let t = self.steps as f64;
        let (pm, p0, pp) =
            (self.dq_count[0] as f64 / t, self.dq_count[1] as f64 / t, self.dq_count[2] as f64 / t);
        let kappa = self.kappa_sum / t;
        println!("[{label}] steps                 : {}", self.steps);
        println!("[{label}] mean kappa = q/n      : {kappa:.6}   (heuristic 0.25)");
        println!("[{label}] mean rho   = r/n      : {:.6}   (heuristic 0.5)", self.rho_sum / t);
        println!("[{label}] mean eps   = (r-q)/n  : {:.6}   (heuristic 0.25)", self.eps_sum / t);
        println!("[{label}] P(dq=-1)              : {pm:.6}   (heuristic kappa/2 = {:.6})", kappa / 2.0);
        println!("[{label}] P(dq= 0)              : {p0:.6}   (heuristic 0.5)");
        println!(
            "[{label}] P(dq=+1)              : {pp:.6}   (heuristic (1-kappa)/2 = {:.6})",
            (1.0 - kappa) / 2.0
        );
        println!("[{label}] E[dq]                 : {:.6}   (heuristic (1-2k)/2 = {:.6})", pp - pm, (1.0 - 2.0 * kappa) / 2.0);
        // chi-square against uniform for rho
        let exp = t / RBINS as f64;
        let chi2: f64 =
            self.rho_hist.iter().map(|&o| { let d = o as f64 - exp; d * d / exp }).sum();
        println!("[{label}] chi2(rho, {RBINS} bins)    : {chi2:.2}   (df={}, uniform if ~{})", RBINS - 1, RBINS - 1);
        println!("[{label}] rho histogram         : {:?}", self.rho_hist);
        if self.gaps > 0 {
            println!(
                "[{label}] mean gap between dq!=0: {:.4}  max gap {}",
                self.gap_sum as f64 / self.gaps as f64,
                self.max_gap
            );
        }
        println!("[{label}] transition matrix (rows=prev dq -1/0/+1, cols=next):");
        for i in 0..3 {
            let row: u64 = self.pair[i].iter().sum();
            if row > 0 {
                println!(
                    "[{label}]   {:>2} -> [{:.5} {:.5} {:.5}]",
                    i as i32 - 1,
                    self.pair[i][0] as f64 / row as f64,
                    self.pair[i][1] as f64 / row as f64,
                    self.pair[i][2] as f64 / row as f64
                );
            }
        }
    }
}

fn run_orbit(m: u64, max_n: u64, acc: &mut Acc, mut bins: Option<&mut BufWriter<File>>) {
    let mut s = enter(m);
    let mut prev: Option<i8> = None;
    let mut last_change = s.n;
    let mut bin_edge = s.n * 2;
    let mut local = Acc::default();
    while !s.absorbed() && s.n < max_n {
        let d = dq(s);
        acc.observe(s, d, prev);
        local.observe(s, d, prev);
        if d != 0 {
            let gap = s.n - last_change;
            acc.gap_sum += gap;
            acc.gaps += 1;
            acc.max_gap = acc.max_gap.max(gap);
            last_change = s.n;
        }
        if let Some(bw) = bins.as_deref_mut() {
            if s.n >= bin_edge {
                emit_bin(bw, m, s.n, &local);
                local = Acc::default();
                bin_edge = s.n * 2;
            }
        }
        prev = Some(d);
        s = step(s);
    }
    if let Some(bw) = bins.as_deref_mut() {
        if local.steps > 0 {
            emit_bin(bw, m, s.n, &local);
        }
    }
}

fn emit_bin(bw: &mut BufWriter<File>, m: u64, n: u64, a: &Acc) {
    let t = a.steps as f64;
    writeln!(
        bw,
        "{m},{n},{},{:.8},{:.8},{:.8},{:.8},{:.8}",
        a.steps,
        a.kappa_sum / t,
        a.rho_sum / t,
        a.dq_count[0] as f64 / t,
        a.dq_count[1] as f64 / t,
        a.dq_count[2] as f64 / t
    )
    .unwrap();
}

fn main() {
    let a = Args::parse();
    let max_n = a.u64("max-n", 50_000_000);
    let out_path = a.str("out", "");
    let t0 = now();

    let mut bins = if out_path.is_empty() {
        None
    } else {
        let f = File::create(&out_path).expect("create out");
        let mut b = BufWriter::new(f);
        writeln!(b, "m,n_end,steps,mean_kappa,mean_rho,p_down,p_flat,p_up").unwrap();
        Some(b)
    };

    let mut acc = Acc::default();
    if a.0.contains_key("m") {
        let m = a.u64("m", 1);
        run_orbit(m, max_n, &mut acc, bins.as_mut());
        acc.report(&format!("m={m}"));
    } else {
        let lo = a.u64("lo", 1);
        let hi = a.u64("hi", 20_000);
        let stride = a.u64("stride", 1).max(1);
        let mut count = 0u64;
        let mut m = lo;
        while m <= hi {
            let mut one = Acc::default();
            run_orbit(m, max_n, &mut one, None);
            acc.merge(&one);
            count += 1;
            m += stride;
        }
        acc.report(&format!("ensemble {lo}..{hi} step {stride} ({count} orbits)"));
    }
    if let Some(b) = bins.as_mut() {
        b.flush().unwrap();
    }
    println!("elapsed seconds          : {:.2}", now() - t0);
}
