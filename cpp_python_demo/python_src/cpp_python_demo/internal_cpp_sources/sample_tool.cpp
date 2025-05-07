#include <iostream>
#include <vector>
#include <string>
#include <numeric>

int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::cout << "Hello from sample_tool (C++)! You passed: " << argv[1] << std::endl;
    } else {
        std::cout << "Hello from sample_tool (C++)! No arguments passed." << std::endl;
    }
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    long long sum = 0;
    for(int n : numbers) { sum += n; }
    std::cout << "The sum of 1-5 is " << sum << std::endl;
    return 0;
} 