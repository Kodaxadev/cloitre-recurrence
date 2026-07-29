fn sparse_coefficients(gaps: &[u32]) -> (i128, i128, i128) {
    let span: i128 = gaps.iter().map(|gap| i128::from(gap + 2)).sum();
    let mut prefix = 0i128;
    let mut binary = 0i128;
    let mut weighted = 0i128;
    for &gap in gaps {
        prefix += i128::from(gap + 2);
        let exponent = u32::try_from(span - prefix).unwrap();
        binary += 1i128 << exponent;
        weighted += i128::from(exponent) << exponent;
    }
    (span, binary, weighted)
}

fn recurrence_coefficients(gaps: &[u32]) -> (i128, i128, i128) {
    let mut span = 0i128;
    let mut binary = 0i128;
    let mut constant = 0i128;
    for &gap in gaps {
        let scale = 1i128 << (gap + 2);
        binary = scale * binary + 1;
        constant = scale * constant + span + i128::from(gap) + 5;
        span += i128::from(gap) + 2;
    }
    (span, binary, constant)
}

fn decode_word(mut code: u32, length: usize) -> Vec<u32> {
    let mut gaps = Vec::with_capacity(length);
    for _ in 0..length {
        gaps.push(code % 4);
        code /= 4;
    }
    gaps
}

fn unit_state(n: i128, quotient: i128, returned: i128) -> bool {
    let d_coord = n - 2 * quotient;
    (n + 3 + returned) % 4 == 0
        && returned >= 1
        && returned <= d_coord - 3
        && 4 * returned <= n + d_coord + 2
}

fn pure_gate(n: i128, quotient: i128, returned: i128, gap: u32, next_returned: i128) -> bool {
    let d_coord = n - 2 * quotient;
    let numerator = d_coord - 3 - returned;
    let scale = 1i128 << (gap + 4);
    numerator % 2 == 0
        && numerator / 2 >= 2
        && (1..=scale).contains(&next_returned)
        && d_coord + i128::from(gap) - 3 - next_returned >= scale
}

fn family(a: i128, q_parameter: u32) -> ([i128; 4], [i128; 4], [u32; 3]) {
    let span = 8 * q_parameter;
    let total_power = 1i128 << span;
    let numerator = a * (total_power - 1) + 24;
    assert_eq!(numerator % 9, 0);
    let n0 = numerator / 9 - i128::from(span) - 3;
    assert_eq!((n0 + 3 + a) % 8, 0);
    let b = (n0 + 3 + a) / 8;
    let c_numerator = a * (1i128 << (span - 3)) + a + 3;
    assert_eq!(c_numerator % 9, 0);
    let c = c_numerator / 9;
    (
        [n0 - 3, n0, n0 + i128::from(span) - 3, n0 + i128::from(span)],
        [b, a, c, a],
        [1, span - 5, 1],
    )
}

#[test]
fn sparse_binary_coefficients_match_affine_recurrence() {
    let mut checked = 0u64;
    for length in 1..=6usize {
        let word_count = 4u32.pow(u32::try_from(length).unwrap());
        for code in 0..word_count {
            let gaps = decode_word(code, length);
            let (span, binary, weighted) = sparse_coefficients(&gaps);
            let (old_span, old_binary, constant) = recurrence_coefficients(&gaps);
            assert_eq!(span, old_span);
            assert_eq!(binary, old_binary);
            assert_eq!(constant, (span + 3) * binary - weighted);
            checked += 1;
        }
    }
    assert_eq!(checked, 5_460);
}

#[test]
fn exact_two_renewal_family_passes_local_tests() {
    let mut checked = 0u64;
    for a in 7..=32i128 {
        if a % 3 == 0 {
            continue;
        }
        let q_parameter = if a % 3 == 1 { 4 } else { 8 };
        let (indices, returned, gaps) = family(a, q_parameter);
        for index in 0..4 {
            assert!(unit_state(
                indices[index],
                i128::try_from(index).unwrap(),
                returned[index],
            ));
        }
        for index in 0..3 {
            assert!(pure_gate(
                indices[index],
                i128::try_from(index).unwrap(),
                returned[index],
                gaps[index],
                returned[index + 1],
            ));
            let predicted = (1i128 << (gaps[index] + 2)) * returned[index]
                - indices[index]
                - i128::from(gaps[index])
                - 5;
            assert_eq!(predicted, returned[index + 1]);
            assert_eq!(
                indices[index] + i128::from(gaps[index]) + 2,
                indices[index + 1],
            );
        }
        checked += 1;
    }
    assert_eq!(checked, 18);
}
