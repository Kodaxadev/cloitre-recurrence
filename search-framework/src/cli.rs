//! Minimal `--key value` / `--key=value` argument parser. No dependencies.

use std::collections::BTreeMap;

pub struct Args(pub BTreeMap<String, String>);

impl Args {
    pub fn parse() -> Args {
        let mut map = BTreeMap::new();
        let argv: Vec<String> = std::env::args().skip(1).collect();
        let mut i = 0;
        while i < argv.len() {
            let a = &argv[i];
            if let Some(rest) = a.strip_prefix("--") {
                if let Some((k, v)) = rest.split_once('=') {
                    map.insert(k.to_string(), v.to_string());
                    i += 1;
                } else if i + 1 < argv.len() && !argv[i + 1].starts_with("--") {
                    map.insert(rest.to_string(), argv[i + 1].clone());
                    i += 2;
                } else {
                    map.insert(rest.to_string(), "1".to_string());
                    i += 1;
                }
            } else {
                i += 1;
            }
        }
        Args(map)
    }

    pub fn u64(&self, k: &str, default: u64) -> u64 {
        self.0
            .get(k)
            .map(|v| v.replace('_', "").parse().unwrap_or_else(|_| panic!("bad --{k}")))
            .unwrap_or(default)
    }

    pub fn usize(&self, k: &str, default: usize) -> usize {
        self.u64(k, default as u64) as usize
    }

    pub fn str(&self, k: &str, default: &str) -> String {
        self.0.get(k).cloned().unwrap_or_else(|| default.to_string())
    }

    pub fn flag(&self, k: &str) -> bool {
        self.0.contains_key(k)
    }
}

/// Wall-clock seconds since an arbitrary epoch, for timing only.
pub fn now() -> f64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs_f64())
        .unwrap_or(0.0)
}
