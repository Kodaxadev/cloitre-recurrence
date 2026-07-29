//! Exhaustive sweep of the deterministic all-unit pure-upper subsystem.
//!
//! Lemma 128 makes the outgoing exponent of a pure-upper unit gate unique, so
//! the subsystem is a deterministic map on `(n, U, f)`. The `(n, f)` part of
//! the trajectory does not depend on `U` at all, and both `U`-dependent
//! validity tests are relaxed when `U` decreases. So `U = 0` gives a uniform
//! upper bound for the chain length of every state sharing its `(n, f)`.
//!
//! The canonical-translate condition `g <= 2^{h+2}` confines `f` to about four
//! consecutive integers once `(n, h)` is fixed, so the whole set of states with
//! at least one outgoing gate is enumerated in `O(N log N)` rather than
//! `O(N^2)`. Every such state is then iterated forward to exhaustion.

use std::env;
use std::thread;

/// Least `h >= 2` with `2^h f >= n + h + 4`. Monotone in `h`.
#[inline]
fn minimal_exponent(n: u64, f: u64) -> u32 {
    let mut h: u32 = 2;
    while (f << h) < n + h as u64 + 4 {
        h += 1;
    }
    h
}

/// One step of the deterministic subsystem at wrap count zero.
#[inline]
fn step_normalized(n: u64, f: u64) -> Option<(u64, u64)> {
    // Parent defect test d >= 2, i.e. D - 3 - f >= 4 with D = n.
    if n < f + 7 {
        return None;
    }
    let h = minimal_exponent(n, f);
    if h + 2 >= 63 {
        return None;
    }
    let spacing = 1u64 << (h + 2);
    let g = (f << h) - n - h as u64 - 3;
    // Canonical translate j = 0.
    if g < 1 || g > spacing {
        return None;
    }
    // Child defect test 2 d' >= spacing, with D' = n + h - 2.
    if n + h as u64 - 2 < 3 + g + spacing {
        return None;
    }
    Some((n + h as u64, g))
}

/// Length of the normalized chain from `(n, f)`.
#[inline]
fn chain_length(mut n: u64, mut f: u64, cap: u32) -> u32 {
    let mut length = 0u32;
    while length < cap {
        match step_normalized(n, f) {
            Some((next_n, next_f)) => {
                n = next_n;
                f = next_f;
                length += 1;
            }
            None => break,
        }
    }
    length
}

const MAX_TRACK: usize = 48;

#[derive(Clone, Copy)]
struct Tally {
    /// `first[l]` is the least start index realizing chain length exactly `l`,
    /// and `witness[l]` its returned residue.
    first: [u64; MAX_TRACK],
    witness: [u64; MAX_TRACK],
    candidates: u64,
    live: u64,
}

impl Tally {
    fn new() -> Self {
        Tally {
            first: [u64::MAX; MAX_TRACK],
            witness: [0; MAX_TRACK],
            candidates: 0,
            live: 0,
        }
    }

    fn offer(&mut self, length: usize, n: u64, f: u64) {
        if length < MAX_TRACK && self.first[length] > n {
            self.first[length] = n;
            self.witness[length] = f;
        }
    }

    fn merge(&mut self, other: &Tally) {
        for index in 0..MAX_TRACK {
            if other.first[index] < self.first[index] {
                self.first[index] = other.first[index];
                self.witness[index] = other.witness[index];
            }
        }
        self.candidates += other.candidates;
        self.live += other.live;
    }
}

fn sweep_range(lo: u64, hi: u64, cap: u32) -> Tally {
    let mut tally = Tally::new();
    for n in lo..=hi {
        let mut h: u32 = 2;
        while h + 2 < 63 && (1u64 << (h + 2)) <= n + h as u64 {
            let spacing = 1u64 << (h + 2);
            let power = 1u64 << h;
            // g = f * 2^h - n - h - 3 must lie in [1, spacing].
            let f_lo = (n + h as u64 + 4).div_ceil(power);
            let f_hi = (n + h as u64 + 3 + spacing) / power;
            let mut f = f_lo;
            while f <= f_hi {
                if (n + 3 + f) % 4 == 0 {
                    tally.candidates += 1;
                    // A full step also re-derives h, so an f that survives is
                    // exactly a state whose unique gate is this h.
                    if step_normalized(n, f).is_some() {
                        tally.live += 1;
                        let length = chain_length(n, f, cap);
                        tally.offer(length as usize, n, f);
                    }
                }
                f += 1;
            }
            h += 1;
        }
    }
    tally
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let bound: u64 = args
        .get(1)
        .and_then(|value| value.parse().ok())
        .unwrap_or(100_000);
    let threads: usize = args
        .get(2)
        .and_then(|value| value.parse().ok())
        .unwrap_or(8);
    let cap: u32 = 40;

    let lo = 8u64;
    let span = (bound - lo + 1).div_ceil(threads as u64);
    let mut total = Tally::new();
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for index in 0..threads {
            let start = lo + span * index as u64;
            let end = (start + span - 1).min(bound);
            if start > end {
                continue;
            }
            handles.push(scope.spawn(move || sweep_range(start, end, cap)));
        }
        for handle in handles {
            let part = handle.join().expect("sweep thread panicked");
            total.merge(&part);
        }
    });

    println!("bound n <= {bound}");
    println!("candidate (n, h, f) triples: {}", total.candidates);
    println!("states with a valid gate: {}", total.live);
    println!("length  least start n  residue f");
    for length in 1..MAX_TRACK {
        if total.first[length] != u64::MAX {
            println!(
                "{length:6}  {:13}  {}",
                total.first[length], total.witness[length]
            );
        }
    }
}
