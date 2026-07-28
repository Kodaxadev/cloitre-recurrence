//! Probe the auxiliary moving-modulus map x_(n+1) = 2*x_n mod (n+2).
//!
//! This is the exact dynamics of a hypothetical no-down tail before imposing
//! Lemma 40's growing danger interval.

use conjecture::cli::{now, Args};
use conjecture::monotone::{safe_step, SafeOutcome, SafeState};
use conjecture::Fnv;
use std::collections::{btree_map::Entry, BTreeMap};

#[allow(dead_code)]
#[derive(Clone, Copy, Debug)]
struct Record {
    start: u64,
    end_n: u64,
    end_x: u64,
    steps: u64,
    wraps: u64,
}

fn run(start_n: u64, start_x: u64, max_steps: u64) -> Record {
    let mut n = start_n;
    let mut x = start_x;
    let mut steps = 0;
    let mut wraps = 0;
    while x != 0 && steps < max_steps {
        let modulus = n + 2;
        let doubled = 2 * x;
        if doubled >= modulus {
            x = doubled - modulus;
            wraps += 1;
        } else {
            x = doubled;
        }
        n += 1;
        steps += 1;
    }
    Record {
        start: start_x,
        end_n: n,
        end_x: x,
        steps,
        wraps,
    }
}

fn sweep(start_n: u64, max_steps: u64) {
    let mut live: BTreeMap<u64, u64> =
        (1..start_n).map(|x| (x, x)).collect();
    let mut n = start_n;
    let mut steps = 0;
    let mut captured = 0u64;
    let mut merges = 0u64;
    let mut next_report = live.len().saturating_div(2);
    while !live.is_empty() && steps < max_steps {
        let before = live.len();
        let mut next: BTreeMap<u64, u64> = BTreeMap::new();
        let mut captured_now = 0u64;
        for (x, witness) in live {
            let modulus = n + 2;
            let doubled = 2 * x;
            let y = if doubled >= modulus {
                doubled - modulus
            } else {
                doubled
            };
            if y == 0 {
                captured_now += 1;
            } else {
                next.entry(y)
                    .and_modify(|old| *old = (*old).min(witness))
                    .or_insert(witness);
            }
        }
        captured += captured_now;
        merges += before as u64 - captured_now - next.len() as u64;
        live = next;
        n += 1;
        steps += 1;
        if live.len() <= next_report {
            let sample = live.iter().next().map(|(x, witness)| (*x, *witness));
            println!(
                "  n={n} steps={steps} live={} captured={captured} merges={merges} sample={sample:?}",
                live.len(),
            );
            next_report = live.len().saturating_div(2);
        }
    }
    println!("ending index               : {n}");
    println!("steps                       : {steps}");
    println!("live states                 : {}", live.len());
    println!("captured transitions        : {captured}");
    println!("merges                      : {merges}");
    for (x, witness) in live.iter().take(20) {
        println!("LIVE x={x} witness={witness}");
    }
}

fn safe_sweep(start_n: u64, max_steps: u64) {
    let mut live: BTreeMap<u64, (u64, u64)> =
        (1..start_n).map(|e| (e, (0, e))).collect();
    let mut n = start_n;
    let mut steps = 0;
    let mut rejected = 0u64;
    let mut captured = 0u64;
    let mut merges = 0u64;
    let starts = start_n - 1;
    let mut trajectory = Fnv::default();
    trajectory.write_u64(start_n);
    trajectory.write_u64(starts);
    let mut next_report = live.len().saturating_div(2);
    while !live.is_empty() && steps < max_steps {
        let mut next: BTreeMap<u64, (u64, u64)> = BTreeMap::new();
        for (e, (wraps, witness)) in live {
            let state = SafeState {
                e,
                w: n - wraps,
                wraps,
            };
            let (next_e, next_wraps) = match safe_step(state) {
                SafeOutcome::Continue { state, .. } => {
                    assert_eq!(state.n(), n + 1);
                    (state.e, state.wraps)
                }
                SafeOutcome::Terminated { capture: true } => {
                    captured += 1;
                    continue;
                }
                SafeOutcome::Terminated { capture: false } => {
                    rejected += 1;
                    continue;
                }
            };
            match next.entry(next_e) {
                Entry::Vacant(slot) => {
                    slot.insert((next_wraps, witness));
                }
                Entry::Occupied(mut slot) => {
                    merges += 1;
                    let old = slot.get_mut();
                    if next_wraps < old.0
                        || (next_wraps == old.0 && witness < old.1)
                    {
                        *old = (next_wraps, witness);
                    }
                }
            }
        }
        live = next;
        assert_eq!(
            starts,
            rejected + captured + merges + live.len() as u64,
            "safe-sweep covering identity failed"
        );
        let mut state_sum = 0u64;
        let mut state_xor = 0u64;
        let mut e_sum = 0u64;
        let mut wrap_sum = 0u64;
        for (&e, &(wraps, witness)) in &live {
            let fingerprint = mix_state(e, wraps, witness);
            state_sum = state_sum.wrapping_add(fingerprint);
            state_xor ^= fingerprint;
            e_sum = e_sum.wrapping_add(e);
            wrap_sum = wrap_sum.wrapping_add(wraps);
        }
        for value in [
            n,
            rejected,
            captured,
            merges,
            live.len() as u64,
            state_sum,
            state_xor,
            e_sum,
            wrap_sum,
        ] {
            trajectory.write_u64(value);
        }
        n += 1;
        steps += 1;
        if live.len() <= next_report {
            let sample = live
                .iter()
                .next()
                .map(|(e, (wraps, witness))| (*e, *wraps, *witness));
            println!(
                "  n={n} steps={steps} live={} rejected={rejected} captured={captured} sample={sample:?}",
                live.len()
            );
            next_report = live.len().saturating_div(2);
        }
    }
    println!("ending index               : {n}");
    println!("steps                       : {steps}");
    println!("live states                 : {}", live.len());
    println!("danger rejections           : {rejected}");
    println!("capture transitions         : {captured}");
    println!("dominated merges            : {merges}");
    println!("trajectory fnv1a64          : {:#018x}", trajectory.0);
    for (e, (wraps, witness)) in live.iter().take(20) {
        println!("LIVE e={e} wraps={wraps} witness={witness}");
    }
}

#[inline]
fn mix_state(e: u64, wraps: u64, witness: u64) -> u64 {
    let mut x = e ^ wraps.rotate_left(21) ^ witness.rotate_left(42);
    x = x.wrapping_add(0x9e37_79b9_7f4a_7c15);
    x = (x ^ (x >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
    x = (x ^ (x >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
    x ^ (x >> 31)
}

fn main() {
    let args = Args::parse();
    let n = args.u64("n", 100);
    let max_steps = args.u64("max-steps", 10_000_000);
    let started = now();
    if args.flag("safe-sweep") {
        safe_sweep(n, max_steps);
        println!("elapsed seconds            : {:.3}", now() - started);
        return;
    }
    if args.flag("sweep") {
        sweep(n, max_steps);
        println!("elapsed seconds            : {:.3}", now() - started);
        return;
    }
    if args.0.contains_key("x") {
        let x = args.u64("x", 1);
        assert!(x < n, "--x must be smaller than --n");
        println!("{:?}", run(n, x, max_steps));
        println!("elapsed seconds            : {:.3}", now() - started);
        return;
    }
    let mut longest = run(n, 1, max_steps);
    let mut survivors = Vec::new();
    for x in 1..n {
        let record = run(n, x, max_steps);
        if record.steps > longest.steps {
            longest = record;
        }
        if record.end_x != 0 {
            survivors.push(record);
        }
    }
    println!("start index                : {n}");
    println!("starts checked             : {}", n - 1);
    println!("step limit                 : {max_steps}");
    println!("survivors                  : {}", survivors.len());
    println!("longest                    : {longest:?}");
    for record in survivors.iter().take(20) {
        println!("SURVIVOR {record:?}");
    }
    println!("elapsed seconds            : {:.3}", now() - started);
}
