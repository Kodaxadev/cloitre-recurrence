//! Compressed simultaneous verification: advance ALL start values in an
//! interval at once, keeping only the *set* of distinct reachable values.
//!
//! Rationale. The forward map at index n is
//!     f_n(b) = b + (b mod n) = 2b - n*floor(b/n),
//! i.e. affine with slope 2 on each block [kn, (k+1)n). It is NOT injective:
//! block k and block k+1 have overlapping images, so distinct orbits merge.
//! Every merge removes work permanently. Tracking the set therefore costs
//! strictly less than tracking the starts, and "every m <= M stabilizes by
//! index N" is exactly "the live set is empty at N".
//!
//! Key structural fact exploited here: images of block k lie in [kn, (k+2)n),
//! so only ADJACENT blocks can interleave. The image of a sorted list can be
//! re-sorted by a rolling two-way merge in O(L) instead of O(L log L).

use crate::absorbed_b;

#[derive(Clone, Copy, Debug, Default)]
pub struct StepStats {
    pub n: u64,
    /// Live distinct values before this step.
    pub live_before: usize,
    /// Values found absorbing at this index (removed).
    pub absorbed: usize,
    /// Distinct values lost to orbit merging during this step.
    pub merged: usize,
    /// Live distinct values after this step (at index n+1).
    pub live_after: usize,
}

pub struct Sweep {
    pub n: u64,
    live: Vec<u64>,
    out: Vec<u64>,
    img: Vec<u64>,
    carry: Vec<u64>,
    merged_buf: Vec<u64>,
    /// Total absorbed so far, indexed nowhere: just a running total.
    pub total_absorbed: u64,
}

impl Sweep {
    /// Start with every b_2 = m for m in `lo..=hi`. (b_2 = b_1 because
    /// b_1 mod 1 = 0, so index 2 is the natural entry point.)
    pub fn new(lo: u64, hi: u64) -> Self {
        assert!(lo >= 1 && lo <= hi, "bad range");
        Sweep {
            n: 2,
            live: (lo..=hi).collect(),
            out: Vec::new(),
            img: Vec::new(),
            carry: Vec::new(),
            merged_buf: Vec::new(),
            total_absorbed: 0,
        }
    }

    pub fn live_count(&self) -> usize {
        self.live.len()
    }

    pub fn live(&self) -> &[u64] {
        &self.live
    }

    pub fn is_empty(&self) -> bool {
        self.live.is_empty()
    }

    /// Advance the whole set from index n to index n+1.
    pub fn step(&mut self) -> StepStats {
        let n = self.n;
        let live_before = self.live.len();

        // 1. Remove absorbing values. b is absorbing at n iff (n+1)|b and
        //    b/(n+1) < n. Removal is safe: absorbing states never leave.
        let before = self.live.len();
        self.live.retain(|&b| !absorbed_b(n, b));
        let absorbed = before - self.live.len();
        self.total_absorbed += absorbed as u64;

        // 2. Apply f_n block by block and re-sort by rolling two-way merge.
        self.out.clear();
        self.carry.clear();
        let mut i = 0usize;
        while i < self.live.len() {
            let k = self.live[i] / n;
            let boundary = (k + 1) * n;

            self.img.clear();
            while i < self.live.len() && self.live[i] / n == k {
                // f_n(b) = 2b - k*n, strictly increasing across the block.
                self.img.push(2 * self.live[i] - k * n);
                i += 1;
            }

            // merge carry (sorted) with img (sorted) into merged_buf
            merge_sorted(&self.carry, &self.img, &mut self.merged_buf);

            // Everything < boundary is final: later blocks have images >= boundary.
            let split = self.merged_buf.partition_point(|&v| v < boundary);
            push_dedup(&mut self.out, &self.merged_buf[..split]);
            self.carry.clear();
            self.carry.extend_from_slice(&self.merged_buf[split..]);
        }
        push_dedup(&mut self.out, &self.carry);

        let live_after = self.out.len();
        let merged = self.live.len() - live_after;
        std::mem::swap(&mut self.live, &mut self.out);
        self.n = n + 1;

        StepStats { n, live_before, absorbed, merged, live_after }
    }
}

/// Standard two-way merge of sorted slices into `dst` (cleared first).
fn merge_sorted(a: &[u64], b: &[u64], dst: &mut Vec<u64>) {
    dst.clear();
    dst.reserve(a.len() + b.len());
    let (mut i, mut j) = (0usize, 0usize);
    while i < a.len() && j < b.len() {
        if a[i] <= b[j] {
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

/// Append `src` (sorted) to `dst` (sorted), dropping values equal to the
/// current tail of `dst` or to their predecessor in `src`.
fn push_dedup(dst: &mut Vec<u64>, src: &[u64]) {
    for &v in src {
        if dst.last() != Some(&v) {
            dst.push(v);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    /// Brute-force reference: keep the set explicitly with a BTreeSet.
    fn reference(lo: u64, hi: u64, steps: u64) -> Vec<(u64, usize, usize)> {
        let mut set: BTreeSet<u64> = (lo..=hi).collect();
        let mut n = 2u64;
        let mut out = Vec::new();
        for _ in 0..steps {
            let before = set.len();
            set.retain(|&b| !absorbed_b(n, b));
            let absorbed = before - set.len();
            let next: BTreeSet<u64> = set.iter().map(|&b| b + b % n).collect();
            out.push((n, before, absorbed));
            set = next;
            n += 1;
        }
        out
    }

    #[test]
    fn sweep_matches_bruteforce_set() {
        for (lo, hi) in [(1u64, 60u64), (1, 500), (37, 900), (1000, 1600)] {
            let want = reference(lo, hi, 120);
            let mut s = Sweep::new(lo, hi);
            for w in want {
                let got = s.step();
                assert_eq!((got.n, got.live_before, got.absorbed), w, "range {lo}..{hi}");
            }
        }
    }

    #[test]
    fn sweep_output_is_sorted_and_deduped() {
        let mut s = Sweep::new(1, 4000);
        for _ in 0..400 {
            s.step();
            assert!(s.live().windows(2).all(|w| w[0] < w[1]), "not strictly increasing at n={}", s.n);
        }
    }

    /// The set-based sweep and per-start solving must agree on the total number
    /// of starts that stabilize by a given index.
    #[test]
    fn sweep_agrees_with_per_start_counts() {
        use crate::{solve, Outcome};
        let hi = 3000u64;
        let cutoff = 900u64;
        let mut s = Sweep::new(1, hi);
        while s.n < cutoff {
            s.step();
        }
        let still_live_starts = (1..=hi)
            .filter(|&m| match solve(m, cutoff) {
                Outcome::Stabilized { t, .. } => t >= cutoff,
                Outcome::Unresolved { .. } => true,
            })
            .count();
        // Distinct live values <= live starts (merging can only reduce).
        assert!(s.live_count() <= still_live_starts);
        assert!(s.live_count() > 0);
    }
}
