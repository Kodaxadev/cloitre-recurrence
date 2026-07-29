//! Search safe paths for consecutive exact unique gates.
//!
//! This is an exploratory falsification tool for the possible claim that
//! unique gates have uniformly bounded chain length.

use conjecture::cli::{now, Args};
use conjecture::monotone::{safe_step, SafeDigit, SafeOutcome, SafeState};

#[derive(Clone, Copy, Debug)]
struct PositiveReturn {
    m: u64,
    wraps: u64,
    residue: u64,
    k: u32,
}

#[allow(dead_code)]
#[derive(Clone, Copy, Debug)]
struct Gate {
    k: u32,
    zeros: u32,
    m: u64,
    wraps: u64,
    residue: u64,
    candidates: u64,
}

#[derive(Debug)]
struct Trace {
    steps: u64,
    max_unique_run: usize,
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

fn gate_count(m: u64, wraps: u64, k: u32, r: u32) -> u64 {
    let m = i128::from(m);
    let wraps = i128::from(wraps);
    let k_u64 = u64::from(k);
    let parent_n = m - i128::from(k_u64) - 1;
    let parent_wraps = wraps - i128::from(k_u64);
    let scale = 1i128 << k;
    let modulus = 1i128 << (k + 1);
    let target = (m + 3 - scale * parent_n).rem_euclid(modulus);
    let r_i = i128::from(r);
    let width = m - wraps;

    let child_lower = (m + r_i + 3) / (1i128 << (r + 2)) + 1;
    let parent_lower = m + 3 - scale * (parent_n + 2);
    let lower = 1.max(child_lower).max(parent_lower);

    let child_upper = (width + r_i) / (1i128 << (r + 1));
    let parent_upper = m + 3 - scale * (parent_wraps + 4);
    let upper = (width - 1).min(child_upper).min(parent_upper);
    if lower > upper {
        return 0;
    }

    let first = lower + (target - lower).rem_euclid(modulus);
    if first > upper {
        0
    } else {
        u64::try_from(1 + (upper - first) / modulus).unwrap()
    }
}

fn trace(start: SafeState, max_steps: u64) -> Trace {
    let mut state = start;
    let mut steps = 0;
    let mut previous: Option<PositiveReturn> = None;
    let mut zero_only = 0u32;
    let mut current_run = Vec::new();
    let mut best_run = Vec::new();

    while steps < max_steps {
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
                let candidates = gate_count(parent.m, parent.wraps, parent.k, zero_only);
                assert!(candidates > 0);
                let gate = Gate {
                    k: parent.k,
                    zeros: zero_only,
                    m: parent.m,
                    wraps: parent.wraps,
                    residue: parent.residue,
                    candidates,
                };
                if candidates == 1 {
                    current_run.push(gate);
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
            previous = Some(PositiveReturn {
                m: next.n(),
                wraps: next.wraps,
                residue: next.e,
                k,
            });
        }
        state = next;
    }

    Trace {
        steps,
        max_unique_run: best_run.len(),
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
    let n = args.u64("n", 10_000);
    let min_n = args.u64("min-n", n);
    let max_n = args.u64("max-n", n);
    let max_steps = args.u64("max-steps", 1_000_000);
    let samples = args.u64("samples", 0);
    let quotient_backoff = args.u64("quotient-backoff", u64::MAX);
    let all_quotients = args.flag("all-quotients");
    if samples > 0 {
        assert!(6 <= max_n);
    } else {
        assert!(2 <= min_n && min_n <= max_n);
    }
    let started = now();
    let mut best = (0usize, 0u64, 0u64, 0u64, Vec::new());
    let mut longest = (0u64, 0u64, 0u64, 0u64);
    let mut states_checked = 0u64;

    let mut consider = |checkpoint: u64, quotient: u64, e: u64| {
        let result = trace(
            SafeState {
                e,
                w: checkpoint - quotient,
                wraps: quotient,
            },
            max_steps,
        );
        states_checked += 1;
        if result.steps > longest.0 {
            longest = (result.steps, checkpoint, quotient, e);
        }
        if result.max_unique_run > best.0 {
            best = (
                result.max_unique_run,
                checkpoint,
                quotient,
                e,
                result.best_run,
            );
            println!(
                "record unique run {} at n={checkpoint}, q={quotient}, e={e}: {:?}",
                best.0, best.4
            );
        }
    };

    if samples > 0 {
        let mut seed = args.u64("seed", 0x5afe_c0de_0731_17e5);
        for _ in 0..samples {
            let checkpoint = 6 + next_random(&mut seed) % (max_n - 5);
            let first_e = (checkpoint + 3) / 4 + 1;
            let max_quotient = checkpoint - 2 * first_e;
            let min_quotient = max_quotient.saturating_sub(quotient_backoff);
            let quotient =
                min_quotient + next_random(&mut seed) % (max_quotient - min_quotient + 1);
            let last_e = (checkpoint - quotient) / 2;
            let e = first_e + next_random(&mut seed) % (last_e - first_e + 1);
            consider(checkpoint, quotient, e);
        }
    } else {
        for checkpoint in min_n..=max_n {
            if all_quotients {
                for quotient in 0..=checkpoint - 2 {
                    let width = checkpoint - quotient;
                    let first_e = (checkpoint + 3) / 4 + 1;
                    let last_e = width / 2;
                    for e in first_e..=last_e {
                        consider(checkpoint, quotient, e);
                    }
                }
            } else {
                for e in 1..checkpoint {
                    consider(checkpoint, 0, e);
                }
            }
        }
    }

    println!(
        "search domain               : {}",
        if samples > 0 {
            format!("{samples} deterministic samples with n<={max_n}")
        } else {
            format!("checkpoint range {min_n}..={max_n}")
        }
    );
    println!(
        "start-state scope           : {}",
        if samples > 0 || all_quotients {
            "all valid positive-block zero epochs"
        } else {
            "all quotient-zero safe states"
        }
    );
    println!("states checked              : {states_checked}");
    println!(
        "longest safe path           : {} at n={}, q={}, e={}",
        longest.0, longest.1, longest.2, longest.3
    );
    println!(
        "longest unique-gate chain   : {} at n={}, q={}, e={}",
        best.0, best.1, best.2, best.3
    );
    println!("record chain                : {:?}", best.4);
    println!("elapsed seconds             : {:.3}", now() - started);
}
