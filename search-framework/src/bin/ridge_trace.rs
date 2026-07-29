//! Measure mixed-ridge terminal runs on one literal recurrence orbit.
//!
//! This is an exploratory falsification tool for the bounded-terminal-run
//! branch left by Theorem 75. It starts from `b_1=m` via `enter`, so every
//! reported ridge is globally reachable. Finite measurements are not proofs.

use conjecture::cli::{now, Args};
use conjecture::{dq, enter, step, State};

#[derive(Clone, Copy, Debug)]
struct Ridge {
    start_n: u64,
    end_n: u64,
    prefix: u64,
    suffix_zeros: u64,
    initial_run: u64,
    max_up_run: u32,
    terminal_run: u32,
    value: u64,
    normalized: u128,
    mixed: bool,
}

#[derive(Clone, Copy, Debug)]
struct Builder {
    start_n: u64,
    steps: u64,
    initial_run: u64,
    initial_open: bool,
    current_up_run: u32,
    max_up_run: u32,
    last_up_prefix: u64,
    last_terminal_run: u32,
    last_value: u64,
    pending_zero: bool,
    positive_zero_seen: bool,
}

impl Builder {
    fn new(start_n: u64) -> Self {
        Self {
            start_n,
            steps: 0,
            initial_run: 0,
            initial_open: true,
            current_up_run: 0,
            max_up_run: 0,
            last_up_prefix: 0,
            last_terminal_run: 0,
            last_value: 0,
            pending_zero: false,
            positive_zero_seen: false,
        }
    }

    fn observe(&mut self, state: State, digit: i8, next: State) {
        debug_assert!(digit == 0 || digit == 1);
        if digit == 1 {
            self.positive_zero_seen |= self.pending_zero;
            self.pending_zero = false;
            if self.initial_open {
                self.initial_run += 1;
            }
            self.current_up_run += 1;
            self.max_up_run = self.max_up_run.max(self.current_up_run);
            self.last_up_prefix = self.steps + 1;
            self.last_terminal_run = self.current_up_run;
            if next.e() < 0 {
                self.last_value = next.e().unsigned_abs();
            }
        } else {
            self.pending_zero = true;
            self.initial_open = false;
            self.current_up_run = 0;
        }
        self.steps += 1;
        debug_assert_eq!(next.n, state.n + 1);
    }

    fn finish(self, end_n: u64) -> Option<Ridge> {
        if self.last_up_prefix == 0 || self.last_value == 0 {
            return None;
        }
        let prefix = self.last_up_prefix;
        let terminal_run = self.last_terminal_run;
        let suffix_zeros = self.steps - prefix;
        let total = u128::from(self.start_n) + u128::from(prefix) + 3 + u128::from(self.last_value);
        assert_eq!(total % (1u128 << terminal_run), 0);
        let normalized = total >> terminal_run;
        if self.positive_zero_seen {
            assert_eq!(
                normalized & 1,
                u128::from((self.start_n + prefix + 1 - u64::from(terminal_run)) & 1)
            );
        }
        Some(Ridge {
            start_n: self.start_n,
            end_n,
            prefix,
            suffix_zeros,
            initial_run: self.initial_run,
            max_up_run: self.max_up_run,
            terminal_run,
            value: self.last_value,
            normalized,
            mixed: self.positive_zero_seen,
        })
    }
}

#[derive(Debug)]
struct Stats {
    orbits: u64,
    absorbed: u64,
    ridges: u64,
    mixed: u64,
    max_initial_run: u64,
    max_up_run: u32,
    max_terminal_run: u32,
    low_bound: u32,
    low_chain: u64,
    longest_low_chain: u64,
    longest_low_start: u64,
    longest_low_end: u64,
    current_low_start: u64,
    histogram: [u64; 33],
    max_terminal_witness: Option<(u64, Ridge)>,
    longest_prefix: Option<Ridge>,
    largest_normalized: Option<Ridge>,
}

impl Stats {
    fn new(low_bound: u32) -> Self {
        Self {
            orbits: 0,
            absorbed: 0,
            ridges: 0,
            mixed: 0,
            max_initial_run: 0,
            max_up_run: 0,
            max_terminal_run: 0,
            low_bound,
            low_chain: 0,
            longest_low_chain: 0,
            longest_low_start: 0,
            longest_low_end: 0,
            current_low_start: 0,
            histogram: [0; 33],
            max_terminal_witness: None,
            longest_prefix: None,
            largest_normalized: None,
        }
    }

    fn start_orbit(&mut self) {
        self.orbits += 1;
        self.low_chain = 0;
    }

    fn observe(&mut self, m: u64, ridge: Ridge) {
        self.ridges += 1;
        self.mixed += u64::from(ridge.mixed);
        self.max_initial_run = self.max_initial_run.max(ridge.initial_run);
        self.max_up_run = self.max_up_run.max(ridge.max_up_run);
        if ridge.terminal_run > self.max_terminal_run {
            self.max_terminal_run = ridge.terminal_run;
            self.max_terminal_witness = Some((m, ridge));
        }
        let bucket = usize::try_from(ridge.terminal_run.min(32)).unwrap();
        self.histogram[bucket] += 1;
        if self
            .longest_prefix
            .is_none_or(|old| ridge.prefix > old.prefix)
        {
            self.longest_prefix = Some(ridge);
        }
        if self
            .largest_normalized
            .is_none_or(|old| ridge.normalized > old.normalized)
        {
            self.largest_normalized = Some(ridge);
        }

        if ridge.terminal_run <= self.low_bound {
            if self.low_chain == 0 {
                self.current_low_start = ridge.start_n;
            }
            self.low_chain += 1;
            if self.low_chain > self.longest_low_chain {
                self.longest_low_chain = self.low_chain;
                self.longest_low_start = self.current_low_start;
                self.longest_low_end = ridge.end_n;
            }
        } else {
            self.low_chain = 0;
        }
    }
}

fn run_orbit(m: u64, max_n: u64, stats: &mut Stats) -> State {
    let mut state = enter(m);
    let mut builder: Option<Builder> = None;
    stats.start_orbit();

    while !state.absorbed() && state.n < max_n {
        let digit = dq(state);
        if digit == -1 {
            if let Some(ridge) = builder.take().and_then(|item| item.finish(state.n)) {
                stats.observe(m, ridge);
            }
            state = step(state);
            builder = Some(Builder::new(state.n));
            continue;
        }

        let next = step(state);
        if let Some(item) = builder.as_mut() {
            item.observe(state, digit, next);
        }
        state = next;
    }
    stats.absorbed += u64::from(state.absorbed());
    state
}

fn print_ridge(label: &str, item: Option<Ridge>) {
    let Some(ridge) = item else {
        println!("{label:<27}: none");
        return;
    };
    println!(
        "{label:<27}: n={}..{} P={} z={} K0={} Kmax={} R={} v={} M={} mixed={}",
        ridge.start_n,
        ridge.end_n,
        ridge.prefix,
        ridge.suffix_zeros,
        ridge.initial_run,
        ridge.max_up_run,
        ridge.terminal_run,
        ridge.value,
        ridge.normalized,
        ridge.mixed
    );
}

fn main() {
    let args = Args::parse();
    let max_n = args.u64("max-n", u64::MAX);
    let low_bound = args.u64("terminal-bound", 2).min(31) as u32;
    let started = now();
    let mut stats = Stats::new(low_bound);
    let state;

    if args.0.contains_key("lo") || args.0.contains_key("hi") {
        let lo = args.u64("lo", 1);
        let hi = args.u64("hi", lo);
        assert!(lo <= hi);
        let mut last = None;
        for m in lo..=hi {
            last = Some(run_orbit(m, max_n, &mut stats));
        }
        state = last.expect("nonempty start range");
        println!("start range                : {lo}..={hi}");
        println!("last m / ending index      : {hi} / {}", state.n);
    } else {
        let m = args.u64("m", 1_320_111);
        state = run_orbit(m, max_n, &mut stats);
        println!("start m                    : {m}");
        println!("ending index               : {}", state.n);
    }
    println!(
        "orbits / absorbed          : {} / {}",
        stats.orbits, stats.absorbed
    );
    println!("completed ridges           : {}", stats.ridges);
    println!("mixed ridges               : {}", stats.mixed);
    println!("max initial up-run         : {}", stats.max_initial_run);
    println!("max internal up-run        : {}", stats.max_up_run);
    println!("max terminal up-run        : {}", stats.max_terminal_run);
    println!(
        "longest terminal <= {} chain: {} (n={}..{})",
        stats.low_bound, stats.longest_low_chain, stats.longest_low_start, stats.longest_low_end
    );
    println!("terminal-run histogram (32 means >=32):");
    for (run, &count) in stats.histogram.iter().enumerate().skip(1) {
        if count > 0 {
            println!("  {run:>2}: {count}");
        }
    }
    if let Some((m, ridge)) = stats.max_terminal_witness {
        println!("max-terminal witness m     : {m}");
        print_ridge("max-terminal ridge", Some(ridge));
    }
    print_ridge("longest positive prefix", stats.longest_prefix);
    print_ridge("largest normalized state", stats.largest_normalized);
    println!("elapsed seconds            : {:.3}", now() - started);
}
