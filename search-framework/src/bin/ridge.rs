//! Exhaust positive no-down segments that begin immediately after a down-step.
//!
//! A down-step at `(n,q,r)` has `0 <= r < q/2`. Its image lies on the
//! post-down ridge used by Theorem 22. This probe measures how many up- and
//! zero-steps occur before the next down-step or absorption.

use conjecture::cli::{now, Args};
use conjecture::{dq, step, State};

#[derive(Clone, Copy, Debug)]
struct Record {
    down_start: State,
    end: State,
    steps: u64,
    ups: u64,
    zeros: u64,
    absorbed: bool,
    ended_down: bool,
}

fn run(down_start: State, max_steps: u64) -> Record {
    debug_assert_eq!(dq(down_start), -1);
    let mut state = step(down_start);
    let mut steps = 0;
    let mut ups = 0;
    let mut zeros = 0;
    while steps < max_steps && !state.absorbed() && dq(state) != -1 {
        match dq(state) {
            0 => zeros += 1,
            1 => ups += 1,
            digit => unreachable!("unexpected digit {digit}"),
        }
        state = step(state);
        steps += 1;
    }
    Record {
        down_start,
        end: state,
        steps,
        ups,
        zeros,
        absorbed: state.absorbed(),
        ended_down: !state.absorbed() && dq(state) == -1,
    }
}

fn lower_up_fraction(candidate: Record, best: Option<Record>) -> bool {
    match best {
        None => true,
        Some(current) => {
            candidate.ups * current.steps < current.ups * candidate.steps
                || (candidate.ups * current.steps == current.ups * candidate.steps
                    && candidate.steps > current.steps)
        }
    }
}

fn print_record(label: &str, record: Option<Record>) {
    let Some(record) = record else {
        println!("{label:<28}: none");
        return;
    };
    println!("{label:<28}:");
    println!("  start                    : {:?}", record.down_start);
    println!("  end                      : {:?}", record.end);
    println!(
        "  steps / up / zero        : {} / {} / {}",
        record.steps, record.ups, record.zeros
    );
    println!(
        "  absorbed / ended down    : {} / {}",
        record.absorbed, record.ended_down
    );
}

fn main() {
    let args = Args::parse();
    let n = args.u64("n", 10_000);
    let default_max_q = n / (u64::from(n.ilog2()) + 1);
    let max_q = args.u64("max-q", default_max_q).min(n);
    let max_r = args.u64("max-r", n);
    let min_steps = args.u64("min-steps", 50);
    let max_steps = args.u64("max-steps", n.saturating_mul(10));
    let started = now();

    let mut searched = 0u64;
    let mut unresolved = 0u64;
    let mut absorbed = 0u64;
    let mut longest: Option<Record> = None;
    let mut sparsest: Option<Record> = None;

    for q in 1..=max_q {
        let r_count = ((q + 1) / 2).min(max_r.saturating_add(1));
        for r in 0..r_count {
            let record = run(State { n, q, r }, max_steps);
            searched += 1;
            unresolved += u64::from(record.steps == max_steps);
            absorbed += u64::from(record.absorbed);
            if longest.is_none_or(|current| record.steps > current.steps) {
                longest = Some(record);
            }
            if record.steps >= min_steps && lower_up_fraction(record, sparsest) {
                sparsest = Some(record);
            }
        }
    }

    println!("down-step index             : {n}");
    println!("maximum starting q         : {max_q}");
    println!("maximum starting r         : {max_r}");
    println!("post-down states searched  : {searched}");
    println!("minimum reported length    : {min_steps}");
    println!("step limit                 : {max_steps}");
    println!("unresolved                 : {unresolved}");
    println!("absorbed                   : {absorbed}");
    print_record("longest", longest);
    print_record("sparsest qualifying", sparsest);
    if let Some(record) = sparsest {
        println!(
            "sparsest up fraction        : {}/{} = {:.9}",
            record.ups,
            record.steps,
            record.ups as f64 / record.steps as f64
        );
    }
    println!("elapsed seconds            : {:.3}", now() - started);
}
