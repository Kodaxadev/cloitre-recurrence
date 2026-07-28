//! Exact search for asymptotically admissible periodic quotient-change words.
//!
//! Uses Lemma 28's finite-state slope representation:
//!   v_{j+1} = 2 v_j - p a_j,  -S <= v_j <= p-S.
//! Every closed word is checked against Theorem 25's exact phase-integrality
//! congruence. A passing word would define an integer affine phase candidate;
//! it would still need exact boundary and reachability checks.

use std::env;
use std::collections::BTreeMap;

#[derive(Default)]
struct PeriodResult {
    cycles: u64,
    passing: Vec<Vec<i8>>,
    obstructions: BTreeMap<u128, u64>,
    witness_periods: BTreeMap<u32, u64>,
    denominator_witnesses: u64,
}

struct Search {
    p: i64,
    target_sum: i64,
    start: i64,
    word: Vec<i8>,
    result: PeriodResult,
}

impl Search {
    fn visit(&mut self, position: i64, current: i64, running_sum: i64) {
        if current < -self.target_sum || current > self.p - self.target_sum {
            return;
        }
        if position == self.p {
            if current == self.start
                && running_sum == self.target_sum
                && self.word.iter().any(|&a| a != 0)
            {
                self.result.cycles += 1;
                let (obstruction, witness_period, denominator_witness) =
                    phase_obstruction(&self.word);
                *self.result.obstructions.entry(obstruction).or_default() += 1;
                *self.result.witness_periods.entry(witness_period).or_default() += 1;
                self.result.denominator_witnesses += denominator_witness as u64;
                if obstruction == 1 {
                    self.result.passing.push(self.word.clone());
                }
            }
            return;
        }

        let decision = self.target_sum + 2 * current;
        let digits: &[i8] = if decision < 0 {
            &[-1]
        } else if decision == 0 {
            &[-1, 0]
        } else if decision < self.p {
            &[0]
        } else if decision == self.p {
            &[0, 1]
        } else {
            &[1]
        };

        let remaining = self.p - position - 1;
        for &digit in digits {
            let next_sum = running_sum + digit as i64;
            if self.target_sum < next_sum - remaining
                || self.target_sum > next_sum + remaining
            {
                continue;
            }
            self.word.push(digit);
            self.visit(
                position + 1,
                2 * current - digit as i64 * self.p,
                next_sum,
            );
            self.word.pop();
        }
    }
}

fn search_period(p: u32) -> PeriodResult {
    assert!((1..=120).contains(&p), "period must be in 1..=120");
    let p_i = p as i64;
    let mut combined = PeriodResult::default();
    for target_sum in 0..=p_i / 2 {
        for start in -target_sum..=p_i - target_sum {
            let mut search = Search {
                p: p_i,
                target_sum,
                start,
                word: Vec::with_capacity(p as usize),
                result: PeriodResult::default(),
            };
            search.visit(0, start, 0);
            combined.cycles += search.result.cycles;
            combined.passing.extend(search.result.passing);
            for (factor, count) in search.result.obstructions {
                *combined.obstructions.entry(factor).or_default() += count;
            }
            for (period, count) in search.result.witness_periods {
                *combined.witness_periods.entry(period).or_default() += count;
            }
            combined.denominator_witnesses += search.result.denominator_witnesses;
        }
    }
    combined
}

fn phase_obstruction(word: &[i8]) -> (u128, u32, bool) {
    let p = word.len() as u32;
    let modulus = (1i128 << p) - 1;
    let mut c = 0i128;
    let mut d = 0i128;
    for (j, &digit) in word.iter().enumerate() {
        let weight = 1i128 << (p as usize - 1 - j);
        c += digit as i128 * weight;
        d += digit as i128 * weight * (j as i128 + 2);
    }
    let p_c = p as i128 * c;
    assert_eq!(p_c % modulus, 0, "slope cycle was not integral");
    let z = p_c / modulus;
    let divisor = gcd(c.unsigned_abs(), modulus as u128) as i128;
    let numerator = (z + d).unsigned_abs();
    let common = gcd(numerator, divisor as u128);
    let obstruction = divisor as u128 / common;
    let mut witness_period = p;
    if obstruction != 1 {
        for k in 1..=p {
            if p % k != 0 {
                continue;
            }
            let factor = (1u128 << k) - 1;
            let local = gcd(divisor as u128, factor);
            if local > 1 && numerator % local != 0 {
                witness_period = k;
                break;
            }
        }
    }
    let denominator = p / gcd(p as u128, z.unsigned_abs()) as u32;
    let denominator_factor = (1u128 << denominator) - 1;
    let denominator_local = gcd(divisor as u128, denominator_factor);
    let denominator_witness =
        denominator_local > 1 && numerator % denominator_local != 0;
    (obstruction, witness_period, denominator_witness)
}

fn gcd(mut a: u128, mut b: u128) -> u128 {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

fn parse_args() -> (u32, u32) {
    let args: Vec<String> = env::args().collect();
    let mut min_period = 1u32;
    let mut max_period = 42u32;
    let mut i = 1usize;
    while i < args.len() {
        match args[i].as_str() {
            "--min-period" => {
                i += 1;
                min_period = args.get(i).expect("missing --min-period value").parse().expect("bad period");
            }
            "--max-period" => {
                i += 1;
                max_period = args.get(i).expect("missing --max-period value").parse().expect("bad period");
            }
            other => panic!("unknown argument: {other}"),
        }
        i += 1;
    }
    assert!(min_period <= max_period);
    (min_period, max_period)
}

fn main() {
    let (min_period, max_period) = parse_args();
    let mut total = 0u64;
    for p in min_period..=max_period {
        let result = search_period(p);
        total += result.cycles;
        println!(
            "period={p:3} cycles={:12} passing={}",
            result.cycles,
            result.passing.len()
        );
        if result.cycles > 0 {
            let factors: Vec<String> = result
                .obstructions
                .iter()
                .take(12)
                .map(|(factor, count)| format!("{factor}:{count}"))
                .collect();
            println!("  obstruction cofactors {}", factors.join(", "));
            let witnesses: Vec<String> = result
                .witness_periods
                .iter()
                .map(|(period, count)| format!("{period}:{count}"))
                .collect();
            println!("  first divisor witnesses {}", witnesses.join(", "));
            println!(
                "  reduced-denominator witnesses {}/{}",
                result.denominator_witnesses, result.cycles
            );
        }
        for word in result.passing.iter().take(10) {
            println!("  PASS {word:?}");
        }
    }
    println!("total cycles checked: {total}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn known_cycle_counts_and_obstruction() {
        let p6 = search_period(6);
        assert_eq!(p6.cycles, 6);
        assert!(p6.passing.is_empty());

        let p12 = search_period(12);
        assert_eq!(p12.cycles, 30);
        assert!(p12.passing.is_empty());

    }

    #[test]
    fn denominator_three_baseline_identity() {
        for h in 1u32..=15 {
            let p = 6 * h;
            let m = 3 * h;
            let modulus = (1i128 << p) - 1;
            let g = modulus / 3;
            let z = 2 * h as i128;
            let mut d_all_y = 0i128;
            for ell in 0..m {
                d_all_y +=
                    (1i128 << (p - 2 - 2 * ell)) * (2 * ell as i128 + 3);
            }
            assert_eq!(z + d_all_y, 11 * g / 3);

            let mut base4 = 0i128;
            for j in 0..h {
                base4 += 7 * (1i128 << (6 * j));
            }
            assert_eq!(g / 3, base4);
            assert_eq!(g % 2, 1);
        }
    }

    #[test]
    fn denominator_seven_baseline_identity() {
        for h in 1u32..=5 {
            let p = 21 * h;
            let blocks = 7 * h;
            let modulus = (1i128 << p) - 1;
            let g = modulus / 7;
            let z = 9 * h as i128;
            let mut d_all_p = 0i128;
            for ell in 0..blocks {
                let power = 3 * (blocks - 1 - ell);
                d_all_p += (1i128 << power) * (9 * ell as i128 + 6);
            }
            assert_eq!(z + d_all_p, 51 * g / 7);

            let mut base8 = 0i128;
            for j in 0..h {
                base8 += 42_799 * (1i128 << (21 * j));
            }
            assert_eq!(g / 7, base8);
            assert_eq!(g % 2, 1);
        }
    }

    #[test]
    fn denominator_nine_baseline_identity() {
        for h in 1u32..=6 {
            let blocks = 3 * h;
            let p = 6 * blocks;
            let modulus = (1i128 << p) - 1;
            let g = modulus / 9;
            let z = 2 * h as i128;
            let mut d_all_n = 0i128;
            for ell in 0..blocks {
                let power = 6 * (blocks - 1 - ell);
                d_all_n += (1i128 << power) * (42 * ell as i128 + 27);
            }
            assert_eq!(z + d_all_n, 83 * g / 21);
            assert_eq!(g % 2, 1);
        }
    }
}
