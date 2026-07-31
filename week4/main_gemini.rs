use std::time::Instant;

fn main() {
    let start = Instant::now();
    let n = 10000;
    let initial_seed = 42;
    let min_val = -10;
    let max_val = 10;
    let range = (max_val - min_val + 1) as i64;

    let mut total_sum: i64 = 0;
    let mut current_seed = initial_seed as u64;

    for _ in 0..20 {
        current_seed = (1664525u64.wrapping_mul(current_seed).wrapping_add(1013904223)) & 0xFFFFFFFF;
        let seed = current_seed;

        let mut val = seed;
        let mut random_numbers = Vec::with_capacity(n);
        for _ in 0..n {
            val = (1664525u64.wrapping_mul(val).wrapping_add(1013904223)) & 0xFFFFFFFF;
            random_numbers.push(((val as i64 % range) + min_val as i64) as i32);
        }

        let mut max_sum = i64::MIN;
        for i in 0..n {
            let mut current_sum: i64 = 0;
            for j in i..n {
                current_sum += random_numbers[j] as i64;
                if current_sum > max_sum {
                    max_sum = current_sum;
                }
            }
        }
        total_sum += max_sum;
    }
    let elapsed = start.elapsed();
    let secs = elapsed.as_secs_f64();
    println!("Total Maximum Subarray Sum (20 runs): {}", total_sum);
    println!("Execution Time Gemini: {:.6} seconds", secs);
}