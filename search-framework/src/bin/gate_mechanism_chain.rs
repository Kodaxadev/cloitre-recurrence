//! Classify consecutive upper-nonunique safe-block gates.
//!
//! A gate is `pure upper` when its canonical translate is zero but its
//! upper-candidate mechanism is active. This tool searches for long runs of
//! that exact mechanism; it is exploratory and does not certify a theorem.

use conjecture::cli::{now, Args};
use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy, Debug)]
struct PositiveBlock {
    start: SafeState,
    returned: SafeState,
    length: u32,
}

#[allow(dead_code)]
#[derive(Clone, Copy, Debug)]
struct Gate {
    n: u64,
    quotient: u64,
    residue: u64,
    k: u32,
    zeros: u32,
    parent_defect: u64,
    child_defect: u64,
    translate: u128,
    spacing: u128,
}

#[derive(Debug)]
struct Trace {
    steps: u64,
    max_pure_upper_run: usize,
    best_run: Vec<Gate>,
}

fn accelerate_zero(state: SafeState) -> Option<(u32, Option<SafeState>, u64)> {
    let mut current = match safe_step(state) {
        SafeOutcome::Continue {
            state,
            digit: SafeDigit::Zero,
        } => state,
        _ => return None,
    };
    let mut wraps = 0;
    let mut steps = 1;
    loop {
        match safe_step(current) {
            SafeOutcome::Continue {
                digit: SafeDigit::Wrap,
                state,
            } => {
                wraps += 1;
                steps += 1;
                current = state;
            }
            SafeOutcome::Continue {
                digit: SafeDigit::Zero,
                ..
            } => return Some((wraps, Some(current), steps)),
            SafeOutcome::Terminated { .. } => return Some((wraps, None, steps)),
        }
    }
}

fn gate(parent: PositiveBlock, child: SafeState, zeros: u32) -> Gate {
    let n = parent.start.n();
    let parent_defect = n - parent.start.wraps - 2 * parent.start.e;
    let child_defect = child.n() - child.wraps - 2 * child.e;
    let exponent = parent.length + zeros + 3;
    let spacing = 1u128.checked_shl(exponent).unwrap_or(u128::MAX);
    let x = (1u128 << (zeros + 2)) * u128::from(parent.returned.e)
        - u128::from(parent.returned.n() + u64::from(zeros) + 3);
    let translate = (x - 1) / spacing;
    Gate {
        n,
        quotient: parent.start.wraps,
        residue: parent.start.e,
        k: parent.length,
        zeros,
        parent_defect,
        child_defect,
        translate,
        spacing,
    }
}

fn is_pure_upper(gate: Gate) -> bool {
    gate.translate == 0
        && gate.parent_defect >= 2
        && 2 * u128::from(gate.child_defect) >= gate.spacing
}

fn trace(start: SafeState, max_steps: u64) -> Trace {
    let mut state = start;
    let mut steps = 0;
    let mut previous: Option<PositiveBlock> = None;
    let mut zero_only = 0u32;
    let mut current_run = Vec::new();
    let mut best_run = Vec::new();

    while steps < max_steps {
        let block_start = state;
        let Some((k, next_zero, used)) = accelerate_zero(state) else {
            match safe_step(state) {
                SafeOutcome::Continue { state: next, .. } => {
                    state = next;
                    steps += 1;
                    continue;
                }
                SafeOutcome::Terminated { .. } => break,
            }
        };
        steps += used;

        if k > 0 {
            if let Some(parent) = previous {
                let current = gate(parent, block_start, zero_only);
                if is_pure_upper(current) {
                    current_run.push(current);
                    if current_run.len() > best_run.len() {
                        best_run = current_run.clone();
                    }
                } else {
                    current_run.clear();
                }
            }
            zero_only = 0;
        } else if previous.is_some() {
            zero_only += 1;
        }

        let Some(next) = next_zero else {
            break;
        };
        if k > 0 {
            previous = Some(PositiveBlock {
                start: block_start,
                returned: next,
                length: k,
            });
        }
        state = next;
    }

    Trace {
        steps,
        max_pure_upper_run: best_run.len(),
        best_run,
    }
}

fn next_random(seed: &mut u64) -> u64 {
    *seed = seed
        .wrapping_mul(6_364_136_223_846_793_005)
        .wrapping_add(1_442_695_040_888_963_407);
    *seed
}

fn main() {
    let args = Args::parse();
    let max_n = args.u64("max-n", 700);
    let max_steps = args.u64("max-steps", 1_000_000);
    let samples = args.u64("samples", 0);
    let all_quotients = args.flag("all-quotients");
    let started = now();
    let mut states_checked = 0u64;
    let mut longest = (0u64, 0u64, 0u64, 0u64);
    let mut best = (0usize, 0u64, 0u64, 0u64, Vec::new());

    let mut consider = |n: u64, quotient: u64, residue: u64| {
        let result = trace(
            SafeState {
                e: residue,
                w: n - quotient,
                wraps: quotient,
            },
            max_steps,
        );
        states_checked += 1;
        if result.steps > longest.0 {
            longest = (result.steps, n, quotient, residue);
        }
        if result.max_pure_upper_run > best.0 {
            best = (
                result.max_pure_upper_run,
                n,
                quotient,
                residue,
                result.best_run,
            );
            println!(
                "record pure-upper run {} at n={n}, q={quotient}, e={residue}: {:?}",
                best.0, best.4
            );
        }
    };

    if samples > 0 {
        let mut seed = args.u64("seed", 0x5afe_c0de_0731_17e5);
        for _ in 0..samples {
            let n = 6 + next_random(&mut seed) % (max_n - 5);
            let first_e = (n + 3) / 4 + 1;
            let max_quotient = n - 2 * first_e;
            let quotient = if all_quotients {
                next_random(&mut seed) % (max_quotient + 1)
            } else {
                0
            };
            let last_e = (n - quotient) / 2;
            let residue = first_e + next_random(&mut seed) % (last_e - first_e + 1);
            consider(n, quotient, residue);
        }
    } else {
        for n in 6..=max_n {
            let first_e = (n + 3) / 4 + 1;
            for residue in first_e..=n / 2 {
                let last_quotient = if all_quotients { n - 2 * residue } else { 0 };
                for quotient in 0..=last_quotient {
                    consider(n, quotient, residue);
                }
            }
        }
    }

    println!(
        "search domain               : {}",
        if samples > 0 {
            format!("{samples} deterministic samples with n<={max_n}")
        } else {
            format!("all n in 6..={max_n}")
        }
    );
    println!(
        "start-state scope           : {}",
        if all_quotients {
            "all valid positive-block zero epochs"
        } else {
            "quotient-zero safe states"
        }
    );
    println!("states checked              : {states_checked}");
    println!(
        "longest safe path           : {} at n={}, q={}, e={}",
        longest.0, longest.1, longest.2, longest.3
    );
    println!(
        "longest pure-upper chain    : {} at n={}, q={}, e={}",
        best.0, best.1, best.2, best.3
    );
    println!("record chain                : {:?}", best.4);
    println!("elapsed seconds             : {:.3}", now() - started);
}
