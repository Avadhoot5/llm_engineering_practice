use std::time::Instant;

const N: usize = 10000;
const INITIAL_SEED: u32 = 42;
const MIN_VAL: i64 = -10;
const MAX_VAL: i64 = 10;
const NUM_RUNS: usize = 20;

// LCG parameters
const A: u32 = 1664525;
const C: u32 = 1013904223;

// Generate next LCG value (mod 2^32)
#[inline]
fn lcg_next(value: u32) -> u32 {
    value.wrapping_mul(A).wrapping_add(C)
}

// Compute maximum subarray sum for a sequence of length `n`
#[inline]
fn max_subarray_sum(n: usize, seed: u32, min_val: i64, max_val: i64) -> i64 {
    let width = (max_val - min_val + 1) as u32;
    let mut lcg_val = seed;
    let mut max_sum: i64 = i64::MIN;
    let mut current_sum: i64 = 0;

    for _ in 0..n {
        lcg_val = lcg_next(lcg_val);
        let num = (lcg_val % width) as i64 + min_val;
        current_sum = std::cmp::max(num, current_sum + num);
        max_sum = std::cmp::max(max_sum, current_sum);
    }

    max_sum
}

// Sum maximum subarray sums over 20 seeds derived from the initial seed
#[inline]
fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i64, max_val: i64) -> i64 {
    let mut total_sum: i64 = 0;
    let mut lcg_val = initial_seed;
    for _ in 0..NUM_RUNS {
        lcg_val = lcg_next(lcg_val);
        total_sum += max_subarray_sum(n, lcg_val, min_val, max_val);
    }
    total_sum
}

fn main() {
    let start = Instant::now();
    let result = total_max_subarray_sum(N, INITIAL_SEED, MIN_VAL, MAX_VAL);
    let elapsed = start.elapsed();
    let secs = elapsed.as_secs_f64();
    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6} seconds", secs);
}