//! Exhaustively probe how long an arbitrary state can avoid a down-step.
//!
//! A nonabsorbed tail with no down-steps must have e > 0 and digits in
//! {0,+1}. This tool searches every such state at one index and records the
//! longest monotone-quotient segment before a down-step or absorption.

use conjecture::cli::{now, Args};
use conjecture::{dq, step, State};

#[derive(Clone, Copy, Debug)]
struct Record {
    start: State,
    end: State,
    steps: u64,
    ups: u64,
    zeros: u64,
    absorbed: bool,
}

fn run(start: State, max_steps: u64) -> Record {
    let mut state = start;
    let mut steps = 0;
    let mut ups = 0;
    let mut zeros = 0;
    while steps < max_steps && !state.absorbed() {
        match dq(state) {
            -1 => break,
            0 => zeros += 1,
            1 => ups += 1,
            digit => unreachable!("unexpected digit {digit}"),
        }
        state = step(state);
        steps += 1;
    }
    Record {
        start,
        end: state,
        steps,
        ups,
        zeros,
        absorbed: state.absorbed(),
    }
}

fn better(left: Record, right: Record) -> Record {
    if right.steps > left.steps
        || (right.steps == left.steps && right.ups < left.ups)
    {
        right
    } else {
        left
    }
}

fn main() {
    let args = Args::parse();
    let n = args.u64("n", 100);
    let factor = args.u64("factor", 100);
    let max_q = args.u64("max-q", n - 1).min(n - 1);
    let max_steps = n.checked_mul(factor).expect("step limit overflow");
    let started = now();
    let mut longest = Record {
        start: State { n, q: 0, r: 1 },
        end: State { n, q: 0, r: 1 },
        steps: 0,
        ups: 0,
        zeros: 0,
        absorbed: false,
    };
    let mut unresolved = 0u64;
    let mut searched = 0u64;
    for q in 0..=max_q {
        for r in q + 1..n {
            let record = run(State { n, q, r }, max_steps);
            searched += 1;
            if record.steps == max_steps {
                unresolved += 1;
            }
            longest = better(longest, record);
        }
    }
    println!("index                      : {n}");
    println!("states searched            : {searched}");
    println!("maximum starting q         : {max_q}");
    println!("step limit                 : {max_steps}");
    println!("unresolved                 : {unresolved}");
    println!("longest start              : {:?}", longest.start);
    println!("longest end                : {:?}", longest.end);
    println!("longest steps              : {}", longest.steps);
    println!("longest up / zero          : {} / {}", longest.ups, longest.zeros);
    println!("longest absorbed           : {}", longest.absorbed);
    println!(
        "end q/n                    : {:.9}",
        longest.end.q as f64 / longest.end.n as f64
    );
    println!("elapsed seconds            : {:.3}", now() - started);
}
