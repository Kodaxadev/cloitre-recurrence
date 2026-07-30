//! Test for the pure-upper run ceiling (K17).
//!
//! The block decomposition and the pure-upper test are re-derived here rather
//! than shared with the binary, so that a change to one has to be reflected in
//! the other to keep this passing.

use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy)]
struct Block {
    start: SafeState,
    wraps: u64,
    next_zero: Option<SafeState>,
}

fn zero_blocks(start: SafeState, limit: usize) -> Vec<Block> {
    let mut out = Vec::new();
    let mut current = start;
    for _ in 0..limit {
        let after_zero = match safe_step(current) {
            SafeOutcome::Continue {
                state,
                digit: SafeDigit::Zero,
            } => state,
            SafeOutcome::Continue { state, .. } => {
                current = state;
                continue;
            }
            SafeOutcome::Terminated { .. } => return out,
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
            None => return out,
        }
    }
    out
}

fn defect(state: SafeState) -> i128 {
    i128::from(state.n()) - i128::from(state.wraps) - 2 * i128::from(state.e)
}

fn pure_upper(parent: &Block, child: &Block, gap: u64) -> bool {
    let Some(returned) = parent.next_zero else {
        return false;
    };
    if parent.wraps == 0 || child.wraps == 0 {
        return false;
    }
    let exponent = parent.wraps + gap + 3;
    if exponent >= 62 || gap + 2 >= 62 {
        return false;
    }
    if defect(parent.start) < 2 {
        return false;
    }
    let spacing = 1i128 << exponent;
    let excess = (i128::from(returned.e) << (gap + 2))
        - i128::from(returned.n())
        - i128::from(gap)
        - 3;
    if excess < 1 || excess > spacing {
        return false;
    }
    2 * defect(child.start) >= spacing
}

fn longest_run(start: SafeState) -> u32 {
    let blocks = zero_blocks(start, 4096);
    let spots: Vec<usize> = blocks
        .iter()
        .enumerate()
        .filter(|(_, block)| block.wraps > 0 && block.next_zero.is_some())
        .map(|(index, _)| index)
        .collect();
    let mut best = 0u32;
    let mut run = 0u32;
    for window in spots.windows(2) {
        let gap = (window[1] - window[0] - 1) as u64;
        if pure_upper(&blocks[window[0]], &blocks[window[1]], gap) {
            run += 1;
            best = best.max(run);
        } else {
            run = 0;
        }
    }
    best
}

#[test]
fn k14_witness_has_six_pure_upper_gates() {
    // R8: the "transient of length at most five" claim is false.
    assert_eq!(longest_run(SafeState { e: 482, w: 966, wraps: 5 }), 6);
    // Lemma 116 normalization keeps the run.
    assert_eq!(longest_run(SafeState { e: 482, w: 971, wraps: 0 }), 6);
}

#[test]
fn pure_upper_run_ceiling_is_six() {
    let mut best = 0u32;
    let mut at = (0u64, 0u64);
    for n in 6u64..=1500 {
        for e in 1..n {
            let start = SafeState { e, w: n, wraps: 0 };
            if !start.check() {
                continue;
            }
            let run = longest_run(start);
            if run > best {
                best = run;
                at = (n, e);
            }
        }
    }
    assert_eq!(best, 6, "pure-upper run ceiling changed: {best} at {at:?}");
    assert_eq!(at, (960, 199));
}
