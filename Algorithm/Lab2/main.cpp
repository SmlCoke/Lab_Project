#include <iostream>
#include <chrono>
#include "Algorithms.h"
#include "load_data.h"

void solve1(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = solve_TSP_with_dp(Adj, verbose);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    auto [path, length] = results;
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The minimum total length is : " << length << std::endl;
}

void solve2(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = solve_TSP_with_dp_with_path(Adj, verbose);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    auto [path, length] = results;
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The minimum total length is : " << length << std::endl;
    std::cout << "The corresponding path is : " << std::endl;
    for (int i = 0; i < path.size() - 1; i++)
    {
        std::cout << (int)path[i] << " -> ";
    }
    std::cout << (int)path[path.size() - 1] << std::endl;
}

void solve3(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = solve_TSP_with_dp_fast(Adj, verbose);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    auto [path, length] = results;
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The minimum total length is : " << length << std::endl;
    std::cout << "The corresponding path is : " << std::endl;
    for (int i = 0; i < path.size() - 1; i++)
    {
        std::cout << (int)path[i] << " -> ";
    }
    std::cout << (int)path[path.size() - 1] << std::endl;
}
int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: tsp_solver <input_file_path>" << std::endl;
        return 1;
    }
    std::string file_path = argv[1];
    std::cout << "Input file: " << file_path << std::endl;

    bool verbose = true;

    std::vector<std::vector<std::uint16_t>> Adj = load_data(file_path, verbose);
    solve3(Adj, true);

    return 0;

}