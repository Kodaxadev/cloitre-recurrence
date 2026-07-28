//! Exact orbit dynamics in quotient-remainder coordinates.

/// The exact state of the orbit at index `n`: b_n = q*n + r with 0 <= r < n.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct State {
    pub n: u64,
    pub q: u64,
    pub r: u64,
}

impl State {
    /// b_n = q*n + r.
    #[inline]
    pub fn b(&self) -> u64 {
        self.q
            .checked_mul(self.n)
            .and_then(|x| x.checked_add(self.r))
            .expect("b overflow")
    }

    /// The orbit is absorbing iff q == r; then b_n = q*(n+1) and every later
    /// increment equals q. (Theorem "Absorption".)
    #[inline]
    pub fn absorbed(&self) -> bool {
        self.q == self.r
    }

    /// e_n := r_n - q_n. In this coordinate the dynamics is an exact doubling
    /// map: e_{n+1} = 2*e_n - dq_n*(n+2), hence e_{n+1} == 2*e_n (mod n+2).
    #[inline]
    pub fn e(&self) -> i64 {
        self.r as i64 - self.q as i64
    }

    /// Structural invariant maintained by every function in this module.
    #[inline]
    pub fn check(&self) -> bool {
        self.n >= 1 && self.r < self.n && self.q <= self.n
    }
}

/// One step in raw `b`-form. Costs a division. Valid for every n >= 1.
#[inline]
pub fn step_b(n: u64, b: u64) -> u64 {
    b.checked_add(b % n).expect("b overflow in step_b")
}

/// One step in `(q,r)`-form.
///
/// PRECONDITION: `s.r < s.n` and `s.q <= s.n`. Both are preserved (Lemma
/// "Bounded quotient"), so once entered the loop is division-free forever.
///
/// Derivation: b_{n+1} = q*n + 2r = q*(n+1) + (2r - q), so with d = 2r - q
///     q_{n+1} = q + floor(d/(n+1)),   r_{n+1} = d mod (n+1).
/// Since -(n+1) < -q <= d <= 2n-2 < 2(n+1), the floor lies in {-1,0,1} and the
/// reduction is a single conditional add or subtract.
#[inline]
pub fn step(s: State) -> State {
    debug_assert!(s.check(), "precondition violated: {:?}", s);
    let m = s.n + 1;
    let d = 2 * (s.r as i64) - (s.q as i64);
    if d < 0 {
        // q >= 1 here: q == 0 would force d = 2r >= 0.
        State { n: m, q: s.q - 1, r: (d + m as i64) as u64 }
    } else if (d as u64) >= m {
        State { n: m, q: s.q + 1, r: (d as u64) - m }
    } else {
        State { n: m, q: s.q, r: d as u64 }
    }
}

/// The quotient increment dq_n = q_{n+1} - q_n, always in {-1, 0, +1}.
#[inline]
pub fn dq(s: State) -> i8 {
    let d = 2 * (s.r as i64) - (s.q as i64);
    if d < 0 {
        -1
    } else if (d as u64) >= s.n + 1 {
        1
    } else {
        0
    }
}

/// Run the raw recurrence from b_1 = m until b_n < n^2 (equivalently q_n < n).
///
/// Absorption cannot be skipped: absorption means b_n = c*(n+1) with c < n,
/// which forces b_n < n^2, so no absorbing index lies inside the prologue.
///
/// The prologue has length O(sqrt(m)): with f(n) = b_n - n^2 one has
/// f(n+1) - f(n) = r_n - (2n+1) <= -n-2 < 0. (Lemma "Entry".)
pub fn enter(m: u64) -> State {
    // b_1 mod 1 = 0, so b_2 = m. Start the scan at n = 2.
    let mut n: u64 = 2;
    let mut b: u64 = m;
    loop {
        let n2 = n.checked_mul(n).expect("n^2 overflow in enter");
        if b < n2 {
            break;
        }
        b = step_b(n, b);
        n += 1;
    }
    State { n, q: b / n, r: b % n }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Outcome {
    /// First index t with b_t = c*(t+1), c < t. Increments equal c from then on.
    Stabilized { t: u64, c: u64 },
    /// No absorbing index with n <= max_n; the state reached is returned.
    Unresolved { state: State },
}

/// Smallest absorbing index for start value `m`, searching n <= `max_n`.
/// Readable reference version; `solve_fast` is the hot equivalent.
pub fn solve(m: u64, max_n: u64) -> Outcome {
    let mut s = enter(m);
    loop {
        if s.absorbed() {
            return Outcome::Stabilized { t: s.n, c: s.q };
        }
        if s.n >= max_n {
            return Outcome::Unresolved { state: s };
        }
        s = step(s);
    }
}

/// Hot loop: identical semantics to `solve`, scalars kept in registers.
pub fn solve_fast(m: u64, max_n: u64) -> Outcome {
    let s0 = enter(m);
    let (mut n, mut q, mut r) = (s0.n, s0.q, s0.r);
    loop {
        if q == r {
            return Outcome::Stabilized { t: n, c: q };
        }
        if n >= max_n {
            return Outcome::Unresolved { state: State { n, q, r } };
        }
        let m1 = n + 1;
        let d = 2 * (r as i64) - (q as i64);
        if d < 0 {
            q -= 1;
            r = (d + m1 as i64) as u64;
        } else if (d as u64) >= m1 {
            q += 1;
            r = (d as u64) - m1;
        } else {
            r = d as u64;
        }
        n = m1;
    }
}

/// True iff value `b` at index `n` is absorbing, i.e. b = c*(n+1), 0 <= c < n.
/// This is the divisibility criterion: absorbed <=> (n+1) | b and b/(n+1) < n.
#[inline]
pub fn absorbed_b(n: u64, b: u64) -> bool {
    let m = n + 1;
    b % m == 0 && b / m < n
}
