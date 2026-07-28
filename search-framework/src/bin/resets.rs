//! Measure quotient-change reset geometry on one exact orbit.
//!
//! This targets the logarithmic loss in Theorem 27: after a +1 event, how
//! often can e reset to a tiny positive value and begin another long zero-run
//! without an intervening -1 event?

use conjecture::cli::{now, Args};
use conjecture::{dq, enter, step, State};

#[derive(Default)]
struct Stats {
    steps: u64,
    events: u64,
    ups: u64,
    downs: u64,
    zero_resets: u64,
    positive_resets: u64,
    negative_resets: u64,
    max_zero_run: u64,
    max_up_event_streak: u64,
    up_event_streak: u64,
    min_positive_reset: u64,
    min_negative_reset: u64,
    small: Vec<(u64, u64, u64, i64, u64)>, // n,q,r,e_after,zero_run
}

fn main() {
    let args = Args::parse();
    let m = args.u64("m", 1);
    let max_n = args.u64("max-n", u64::MAX);
    let started = now();
    let mut s = if args.0.contains_key("n") {
        let state = State {
            n: args.u64("n", 2),
            q: args.u64("q", 1),
            r: args.u64("r", 0),
        };
        assert!(state.check(), "invalid starting state: {state:?}");
        state
    } else {
        enter(m)
    };
    let mut stats = Stats {
        min_positive_reset: u64::MAX,
        min_negative_reset: u64::MAX,
        ..Stats::default()
    };
    let mut zero_run = 0u64;

    while !s.absorbed() && s.n < max_n {
        let digit = dq(s);
        stats.steps += 1;
        if digit == 0 {
            zero_run += 1;
            s = step(s);
            continue;
        }

        stats.events += 1;
        stats.max_zero_run = stats.max_zero_run.max(zero_run);
        let next = step(s);
        if digit == 1 {
            stats.ups += 1;
            stats.up_event_streak += 1;
            stats.max_up_event_streak = stats.max_up_event_streak.max(stats.up_event_streak);
            let reset = next.e();
            match reset.cmp(&0) {
                std::cmp::Ordering::Less => {
                    stats.negative_resets += 1;
                    stats.min_negative_reset =
                        stats.min_negative_reset.min(reset.unsigned_abs());
                }
                std::cmp::Ordering::Equal => stats.zero_resets += 1,
                std::cmp::Ordering::Greater => {
                    stats.positive_resets += 1;
                    stats.min_positive_reset = stats.min_positive_reset.min(reset as u64);
                }
            }
            if reset.unsigned_abs() <= 16 {
                stats.small.push((s.n, s.q, s.r, reset, zero_run));
                stats.small.sort_unstable_by_key(|row| (row.3.unsigned_abs(), row.0));
                stats.small.truncate(20);
            }
        } else {
            stats.downs += 1;
            stats.up_event_streak = 0;
        }
        zero_run = 0;
        s = next;
    }

    println!("start m / state            : {m} / {:?}", if args.0.contains_key("n") { Some((args.u64("n", 2), args.u64("q", 1), args.u64("r", 0))) } else { None });
    println!("ending index               : {}", s.n);
    println!("absorbed                    : {}", s.absorbed());
    println!("steps                       : {}", stats.steps);
    println!("events                      : {}", stats.events);
    println!("up / down                   : {} / {}", stats.ups, stats.downs);
    println!(
        "up resets positive/negative/zero: {} / {} / {}",
        stats.positive_resets, stats.negative_resets, stats.zero_resets
    );
    println!("max zero-run               : {}", stats.max_zero_run);
    println!("max up-event streak        : {}", stats.max_up_event_streak);
    println!("min positive reset         : {}", stats.min_positive_reset);
    println!("min |negative reset|       : {}", stats.min_negative_reset);
    println!("smallest |e| after +1 (n,q,r,e_after,preceding_zero_run):");
    for row in &stats.small {
        println!("  {row:?}");
    }
    println!("elapsed seconds             : {:.2}", now() - started);
}
