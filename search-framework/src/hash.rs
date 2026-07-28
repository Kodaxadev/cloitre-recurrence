//! Deterministic streaming hash (FNV-1a 64) used for reproducibility digests.
//! Not cryptographic; its only job is to make two runs bit-comparable cheaply.
//! File-level SHA-256 digests are produced separately by the verification tools.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Fnv(pub u64);

impl Default for Fnv {
    fn default() -> Self {
        Fnv(0xcbf2_9ce4_8422_2325)
    }
}

impl Fnv {
    #[inline]
    pub fn write_bytes(&mut self, bs: &[u8]) {
        for &x in bs {
            self.0 ^= x as u64;
            self.0 = self.0.wrapping_mul(0x0000_0100_0000_01b3);
        }
    }

    #[inline]
    pub fn write_u64(&mut self, v: u64) {
        self.write_bytes(&v.to_le_bytes());
    }

    /// Order-independent combination, for merging per-thread digests.
    #[inline]
    pub fn combine_unordered(parts: &[Fnv]) -> u64 {
        parts.iter().fold(0u64, |acc, p| acc ^ p.0.rotate_left(17).wrapping_mul(0x9e37_79b9_7f4a_7c15))
    }
}
