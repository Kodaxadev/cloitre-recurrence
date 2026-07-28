//! Sweep with witness tracking: same compressed set dynamics as `sweep`, but
//! every live value carries the SMALLEST start m that reaches it.
//!
//! This turns the compressed sweep into a complete census: each absorbing event
//! yields a triple (t, c, m) describing one distinct orbit, and the union of
//! those events accounts for every start in the range. The cost is one extra
//! u64 per live value.

use crate::absorbed_b;

/// One distinct orbit reaching its absorbing state.
#[derive(Clone, Copy, Debug)]
pub struct Record {
    /// Absorbing index t.
    pub t: u64,
    /// Eventual increment c = b_t/(t+1).
    pub c: u64,
    /// Smallest start value m whose orbit passes through this state.
    pub witness: u64,
}

pub struct WitnessSweep {
    pub n: u64,
    live: Vec<(u64, u64)>, // (value, witness), sorted strictly by value
    out: Vec<(u64, u64)>,
    img: Vec<(u64, u64)>,
    carry: Vec<(u64, u64)>,
    merged: Vec<(u64, u64)>,
    pub total_merges: u64,
}

impl WitnessSweep {
    pub fn new(lo: u64, hi: u64) -> Self {
        assert!(lo >= 1 && lo <= hi, "bad range");
        WitnessSweep {
            n: 2,
            live: (lo..=hi).map(|m| (m, m)).collect(),
            out: Vec::new(),
            img: Vec::new(),
            carry: Vec::new(),
            merged: Vec::new(),
            total_merges: 0,
        }
    }

    pub fn live_count(&self) -> usize {
        self.live.len()
    }

    pub fn is_empty(&self) -> bool {
        self.live.is_empty()
    }

    /// Advance one index. Absorbing values are removed and returned as records.
    pub fn step(&mut self, found: &mut Vec<Record>) {
        let n = self.n;

        // 1. harvest absorbing values
        self.live.retain(|&(b, w)| {
            if absorbed_b(n, b) {
                found.push(Record { t: n, c: b / (n + 1), witness: w });
                false
            } else {
                true
            }
        });

        // 2. apply f_n block by block; images of block k lie in [kn,(k+2)n) so
        //    only adjacent blocks interleave and a rolling 2-way merge suffices.
        self.out.clear();
        self.carry.clear();
        let mut i = 0usize;
        while i < self.live.len() {
            let k = self.live[i].0 / n;
            let boundary = (k + 1) * n;
            self.img.clear();
            while i < self.live.len() && self.live[i].0 / n == k {
                let (b, w) = self.live[i];
                self.img.push((2 * b - k * n, w));
                i += 1;
            }
            merge_pairs(&self.carry, &self.img, &mut self.merged);
            let split = self.merged.partition_point(|&(v, _)| v < boundary);
            let before = self.out.len();
            push_dedup_min(&mut self.out, &self.merged[..split]);
            self.total_merges += (split - (self.out.len() - before)) as u64;
            self.carry.clear();
            self.carry.extend_from_slice(&self.merged[split..]);
        }
        let before = self.out.len();
        let ncarry = self.carry.len();
        push_dedup_min(&mut self.out, &self.carry);
        self.total_merges += (ncarry - (self.out.len() - before)) as u64;

        std::mem::swap(&mut self.live, &mut self.out);
        self.n = n + 1;
    }
}

fn merge_pairs(a: &[(u64, u64)], b: &[(u64, u64)], dst: &mut Vec<(u64, u64)>) {
    dst.clear();
    dst.reserve(a.len() + b.len());
    let (mut i, mut j) = (0usize, 0usize);
    while i < a.len() && j < b.len() {
        if a[i].0 <= b[j].0 {
            dst.push(a[i]);
            i += 1;
        } else {
            dst.push(b[j]);
            j += 1;
        }
    }
    dst.extend_from_slice(&a[i..]);
    dst.extend_from_slice(&b[j..]);
}

/// Append sorted `src` to sorted `dst`, collapsing equal values and keeping the
/// smallest witness. Deterministic regardless of merge order.
fn push_dedup_min(dst: &mut Vec<(u64, u64)>, src: &[(u64, u64)]) {
    for &(v, w) in src {
        match dst.last_mut() {
            Some(last) if last.0 == v => {
                if w < last.1 {
                    last.1 = w;
                }
            }
            _ => dst.push((v, w)),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{solve, Outcome};

    /// Every record must agree with the per-start solver, and the witnesses
    /// must cover every start exactly once after accounting for merges.
    #[test]
    fn records_agree_with_per_start_solver() {
        let (lo, hi) = (1u64, 6000u64);
        let mut s = WitnessSweep::new(lo, hi);
        let mut found = Vec::new();
        while !s.is_empty() && s.n < 5_000_000 {
            s.step(&mut found);
        }
        assert!(s.is_empty(), "sweep did not terminate");
        for rec in &found {
            match solve(rec.witness, 5_000_000) {
                Outcome::Stabilized { t, c } => {
                    assert_eq!((t, c), (rec.t, rec.c), "witness m={}", rec.witness);
                }
                _ => panic!("witness {} unresolved", rec.witness),
            }
        }
        // Witnesses are distinct, and the record set covers the whole range.
        let mut ws: Vec<u64> = found.iter().map(|r| r.witness).collect();
        ws.sort_unstable();
        let n = ws.len();
        ws.dedup();
        assert_eq!(n, ws.len(), "duplicate witnesses");
        let acc = found.len() as u64 + s.total_merges;
        assert_eq!(acc, hi - lo + 1, "records + merges must equal starts");
    }

    /// The maximum t over records must equal the maximum t over all starts.
    #[test]
    fn record_maximum_is_the_true_maximum() {
        let (lo, hi) = (1u64, 4000u64);
        let mut s = WitnessSweep::new(lo, hi);
        let mut found = Vec::new();
        while !s.is_empty() {
            s.step(&mut found);
        }
        let sweep_max = found.iter().map(|r| r.t).max().unwrap();
        let brute = (lo..=hi)
            .map(|m| match solve(m, 5_000_000) {
                Outcome::Stabilized { t, .. } => t,
                _ => panic!("unresolved"),
            })
            .max()
            .unwrap();
        assert_eq!(sweep_max, brute);
    }
}
