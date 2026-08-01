fn unit_state(n: i128, quotient: i128, returned: i128) -> bool {
    let d_coord = n - 2 * quotient;
    (n + 3 + returned) % 4 == 0
        && returned >= 1
        && returned <= d_coord - 3
        && 4 * returned <= n + d_coord + 2
}

fn pure_gaps(n: i128, quotient: i128, returned: i128) -> Vec<(u32, i128)> {
    let d_coord = n - 2 * quotient;
    let mut answer = Vec::new();
    for gap in 0..=70u32 {
        let power = 1i128 << (gap + 2);
        let Some(scaled_returned) = power.checked_mul(returned) else {
            break;
        };
        let next_returned = scaled_returned - n - i128::from(gap) - 5;
        let scale = 1i128 << (gap + 4);
        if (d_coord - 3 - returned) % 2 == 0
            && (d_coord - 3 - returned) / 2 >= 2
            && (1..=scale).contains(&next_returned)
            && d_coord + i128::from(gap) - 3 - next_returned >= scale
        {
            let exponent = gap + 2;
            assert!(
                (returned + 4) * (1i128 << (exponent - 1)) + quotient - i128::from(exponent) + 1
                    <= n
            );
            assert!(n <= returned * (1i128 << exponent) - i128::from(exponent) - 4);
            answer.push((gap, next_returned));
        }
    }
    answer
}

fn family(a: i128, q_parameter: u32) -> (u32, i128, i128, u32) {
    let span = 8 * q_parameter;
    let total_power = 1i128 << span;
    let numerator = a * (total_power - 1) + 24;
    assert_eq!(numerator % 9, 0);
    let n0 = numerator / 9 - i128::from(span) - 3;
    let c_numerator = a * (1i128 << (span - 3)) + a + 3;
    assert_eq!(c_numerator % 9, 0);
    let c = c_numerator / 9;
    (span, n0, c, span - 5)
}

#[test]
fn pure_upper_dyadic_windows_are_disjoint() {
    let mut states = 0u64;
    let mut gates = 0u64;
    for n in 2..=300i128 {
        for quotient in 0..n.min(12) {
            for returned in 5..=n.min(40) {
                if !unit_state(n, quotient, returned) {
                    continue;
                }
                let options = pure_gaps(n, quotient, returned);
                assert!(options.len() <= 1);
                states += 1;
                gates += u64::try_from(options.len()).unwrap();
            }
        }
    }
    assert_eq!(states, 27_113);
    assert_eq!(gates, 7_698);
}

#[test]
fn two_renewal_family_has_one_more_gate_then_stops() {
    let mut checked = 0u64;
    for a in 7..=32i128 {
        if a % 3 == 0 {
            continue;
        }
        let q_parameter = if a % 3 == 1 { 4 } else { 8 };
        let (span, n0, c, large_gap) = family(a, q_parameter);
        let endpoint_n = n0 + i128::from(span);
        assert_eq!(
            pure_gaps(endpoint_n, 3, a),
            vec![(large_gap, c - i128::from(span))]
        );

        let child_n = n0 + 2 * i128::from(span) - 3;
        let child_f = c - i128::from(span);
        assert!(unit_state(child_n, 4, child_f));
        assert!(pure_gaps(child_n, 4, child_f).is_empty());
        assert_eq!(8 * child_f - child_n - 6, a - 9 * i128::from(span));
        assert!(n0 - 16 * i128::from(span) + 2 * a - 62 > 0);
        checked += 1;
    }
    assert_eq!(checked, 18);
}
