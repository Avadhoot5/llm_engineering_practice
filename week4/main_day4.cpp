#include <cstdio>
#include <cstdint>
#include <chrono>

static inline double calculate(uint32_t iterations, int param1, int param2) {
    double result = 1.0;
    double j = (double)param1 - (double)param2; // initial j = i*param1 - param2 for i=1
    const double step = (double)param1;         // increment of j per iteration
    const double offset = (double)param2 * 2.0; // j2 = j + 2*param2

    uint32_t blocks = iterations / 8;
    for (uint32_t k = 0; k < blocks; ++k) {
        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;

        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;
    }

    for (uint32_t r = iterations % 8; r; --r) {
        result -= 1.0 / j;
        result += 1.0 / (j + offset);
        j += step;
    }

    return result;
}

int main() {
    using clock = std::chrono::high_resolution_clock;
    auto start_time = clock::now();

    double result = calculate(200000000u, 4, 1) * 4.0;

    auto end_time = clock::now();
    double elapsed = std::chrono::duration<double>(end_time - start_time).count();

    std::printf("Result: %.12f\n", result);
    std::printf("Execution Time: %.6f seconds\n", elapsed);
    return 0;
}