#include <iostream>
#include <iomanip>
#include <chrono>

int main() {
    using namespace std;

    // Start timing
    auto start = chrono::steady_clock::now();

    const int param1 = 4;
    const int param2 = 1;
    const unsigned int iterations = 200000000u;

    double result = 1.0;

    // Initialize j values for i = 1
    double j1 = static_cast<double>(param1 * 1 - param2); // 3.0
    double j2 = static_cast<double>(param1 * 1 + param2); // 5.0
    const double step = static_cast<double>(param1);      // 4.0

    // Compute in identical order to Python
    for (unsigned int i = 1; i <= iterations; ++i) {
        result -= 1.0 / j1;
        result += 1.0 / j2;
        j1 += step;
        j2 += step;
    }

    double final_result = result * 4.0;

    // End timing
    auto end = chrono::steady_clock::now();
    double elapsed = chrono::duration<double>(end - start).count();

    cout.setf(ios::fixed);
    cout << "Result: " << setprecision(12) << final_result << '\n';
    cout << "Execution Time: " << setprecision(6) << elapsed << " seconds\n";

    return 0;
}