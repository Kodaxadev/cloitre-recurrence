fn coefficients(gaps: &[u32]) -> (i128, i128, i128, i128) {
    let mut shift = 0i128;
    let mut p_coeff = 1i128;
    let mut b_coeff = 0i128;
    let mut c_coeff = 0i128;
    for &gap in gaps {
        let scale = 1i128 << (gap + 2);
        p_coeff *= scale;
        b_coeff = scale * b_coeff + 1;
        c_coeff = scale * c_coeff + shift + i128::from(gap) + 5;
        shift += i128::from(gap) + 2;
    }
    (shift, p_coeff, b_coeff, c_coeff)
}

fn evolve(start_n: i128, start_f: i128, gaps: &[u32]) -> (i128, i128) {
    let mut index = start_n;
    let mut residue = start_f;
    for &gap in gaps {
        residue = (1i128 << (gap + 2)) * residue - index - i128::from(gap) - 5;
        index += i128::from(gap) + 2;
    }
    (index, residue)
}

fn decode_word(mut code: u32, length: usize) -> Vec<u32> {
    let mut gaps = Vec::with_capacity(length);
    for _ in 0..length {
        gaps.push(code % 4);
        code /= 4;
    }
    gaps
}

#[test]
fn fixed_word_endpoints_recover_the_start_index() {
    let mut checked = 0u64;
    for length in 1..=5usize {
        let word_count = 4u32.pow(u32::try_from(length).unwrap());
        for code in 0..word_count {
            let gaps = decode_word(code, length);
            let (shift, p_coeff, b_coeff, c_coeff) = coefficients(&gaps);
            assert!(b_coeff > 0);
            for start_n in 2..=40i128 {
                for start_f in 1..=10i128 {
                    let (end_n, end_f) = evolve(start_n, start_f, &gaps);
                    assert_eq!(end_n, start_n + shift);
                    assert_eq!(end_f, p_coeff * start_f - b_coeff * start_n - c_coeff);
                    let numerator = p_coeff * start_f - c_coeff - end_f;
                    assert_eq!(numerator % b_coeff, 0);
                    assert_eq!(numerator / b_coeff, start_n);
                    checked += 1;
                }
            }
        }
    }
    assert_eq!(checked, 531_960);
}
