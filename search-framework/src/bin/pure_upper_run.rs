//! Longest run of consecutive pure-upper gates on a safe-map path.
//!
//! Theorem 133 forces the outgoing gap of a pure-upper gate at every block
//! length, so the mechanism has no gap-word freedom and the only question left
//! is how long a run of such gates can be. This sweeps every normalized safe
//! state up to an index bound and reports the record run.
//!
//! Lemma 116 lets the sweep fix the initial wrap count at zero: lowering it
//! preserves the digit word and raises both gate defects, and the canonical
//! translate depends only on indices and residues, so a pure-upper run can
//! only lengthen. `U = 0` therefore decides every wrap count at once.

use std::env;
use std::thread;

use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

/// A maximal zero-epoch block: its start, its wrap count, and its return state.
#[derive(Clone, Copy)]
struct Block {
    start: SafeState,
    wraps: u64,
    next_zero: Option<SafeState>,
}

/// Split a safe path into zero-epoch blocks, up to `limit` blocks.
fn zero_blocks(start: SafeState, limit: usize, out: &mut Vec<Block>) {
    out.clear();
    let mut current = start;
    for _ in 0..limit {
        // A block begins with one zero digit.
        let after_zero = match safe_step(current) {
            SafeOutcome::Continue {
                state,
                digit: SafeDigit::Zero,
            } => state,
            // Not at a zero epoch: advance and try again, or stop.
            SafeOutcome::Continue { state, .. } => {
                current = state;
                continue;
            }
            SafeOutcome::Terminated { .. } => return,
        };
        let mut walker = after_zero;
        let mut wraps = 0u64;
        let next_zero = loop {
            match safe_step(walker) {
                SafeOutcome::Continue {
                    digit: SafeDigit::Zero,
                    ..
                } => break Some(walker),
                SafeOutcome::Continue { state, .. } => {
                    wraps += 1;
                    walker = state;
                }
                SafeOutcome::Terminated { .. } => break None,
            }
        };
        out.push(Block {
            start: current,
            wraps,
            next_zero,
        });
        match next_zero {
            Some(state) => current = state,
            None => return,
        }
    }
}

/// Is the gate from `parent` to the positive block `gap` zero-blocks later
/// pure-upper? Uses `d >= 2`, `1 <= x <= H` and `2 d' >= H` with
/// `H = 2^(k + r + 3)`.
fn pure_upper(parent: &Block, child: &Block, gap: u64) -> bool {
    let Some(returned) = parent.next_zero else {
        return false;
    };
    let k = parent.wraps;
    if k == 0 || child.wraps == 0 {
        return false;
    }
    let exponent = k + gap + 3;
    if exponent >= 62 {
        return false;
    }
    let spacing = 1i128 << exponent;
    let parent_defect =
        i128::from(parent.start.n()) - i128::from(parent.start.wraps) - 2 * i128::from(parent.start.e);
    if parent_defect < 2 {
        return false;
    }
    let shift = gap + 2;
    if shift >= 62 {
        return false;
    }
    let excess = (i128::from(returned.e) << shift)
        - i128::from(returned.n())
        - i128::from(gap)
        - 3;
    if excess < 1 || excess > spacing {
        return false;
    }
    let child_defect =
        i128::from(child.start.n()) - i128::from(child.start.wraps) - 2 * i128::from(child.start.e);
    2 * child_defect >= spacing
}

/// Longest run of consecutive pure-upper gates from one starting state.
fn longest_run(start: SafeState, blocks: &mut Vec<Block>, spots: &mut Vec<usize>) -> u32 {
    zero_blocks(start, 4096, blocks);
    spots.clear();
    for (index, block) in blocks.iter().enumerate() {
        if block.wraps > 0 && block.next_zero.is_some() {
            spots.push(index);
        }
    }
    let mut best = 0u32;
    let mut run = 0u32;
    for window in spots.windows(2) {
        let (left, right) = (window[0], window[1]);
        let gap = (right - left - 1) as u64;
        if pure_upper(&blocks[left], &blocks[right], gap) {
            run += 1;
            best = best.max(run);
        } else {
            run = 0;
        }
    }
    best
}

struct Record {
    best: u32,
    at: (u64, u64),
}

fn sweep_range(lo: u64, hi: u64) -> Record {
    let mut record = Record {
        best: 0,
        at: (0, 0),
    };
    let mut blocks = Vec::with_capacity(4096);
    let mut spots = Vec::with_capacity(4096);
    for n in lo..=hi {
        for e in 1..n {
            let start = SafeState { e, w: n, wraps: 0 };
            if !start.check() {
                continue;
            }
            let run = longest_run(start, &mut blocks, &mut spots);
            if run > record.best {
                record.best = run;
                record.at = (n, e);
            }
        }
    }
    record
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let bound: u64 = args
        .get(1)
        .and_then(|value| value.parse().ok())
        .unwrap_or(2000);
    let threads: usize = args
        .get(2)
        .and_then(|value| value.parse().ok())
        .unwrap_or(8);

    let lo = 6u64;
    let span = (bound - lo + 1).div_ceil(threads as u64);
    let mut best = Record {
        best: 0,
        at: (0, 0),
    };
    thread::scope(|scope| {
        let mut handles = Vec::new();
        for index in 0..threads {
            let start = lo + span * index as u64;
            let end = (start + span - 1).min(bound);
            if start > end {
                continue;
            }
            handles.push(scope.spawn(move || sweep_range(start, end)));
        }
        for handle in handles {
            let part = handle.join().expect("sweep thread panicked");
            if part.best > best.best {
                best = part;
            }
        }
    });

    println!("bound n <= {bound}, normalized wrap count zero");
    println!(
        "longest consecutive pure-upper run: {} at (n, e) = {:?}",
        best.best, best.at
    );
}
