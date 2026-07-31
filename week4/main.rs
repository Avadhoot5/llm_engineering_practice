use std::time::Instant;

#[inline(always)]
fn lcg_next(state: &mut u32) -> u32 {
    const A: u32 = 1664525;
    const C: u32 = 1013904223;
    *state = state.wrapping_mul(A).wrapping_add(C);
    *state
}

fn max_subarray_sum(n: usize, seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut lcg_state = seed;
    let range = (max_val - min_val + 1) as u32;

    let mut best = i64::MIN;
    let mut cur = 0i64;

    for _ in 0..n {
        let v = lcg_next(&mut lcg_state);
        let num = (v % range) as i64 + min_val as i64;

        if cur > 0 {
            cur += num;
        } else {
            cur = num;
        }

        if cur > best {
            best = cur;
        }
    }

    best
}

fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut state = initial_seed;
    let mut total = 0i64;

    for _ in 0..20 {
        let seed = lcg_next(&mut state);
        total += max_subarray_sum(n, seed, min_val, max_val);
    }

    total
}

fn main() {
    // Parameters
    let n: usize = 10_000;
    let initial_seed: u32 = 42;
    let min_val: i32 = -10;
    let max_val: i32 = 10;

    let start = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let elapsed = start.elapsed();
    let secs = elapsed.as_secs_f64();

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", secs);
}