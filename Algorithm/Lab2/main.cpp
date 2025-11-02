#include <iostream>
#include <chrono>
#include "Algorithms.h"
#include "RefAlgorithms.h"
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



void solve_fast(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
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

void solve_ref(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = TSP_2opt(Adj, verbose);

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


void solve_fast_v2(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = solve_TSP_with_dp_fast_v2(Adj, verbose);

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

void solve_fast_v3(const std::vector<std::vector<std::uint16_t>> & Adj, bool verbose)
{
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::tuple<std::vector<uint8_t>, uint16_t> results = solve_TSP_with_dp_fast_v3(Adj, verbose);

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

// int main(int argc, char *argv[]) {
//     if (argc < 2) {
//         std::cerr << "Usage: tsp_solver <input_file_path>" << std::endl;
//         return 1;
//     }
//     std::string file_path = argv[1];
//     std::cout << "Input file: " << file_path << std::endl;

//     bool verbose = true;

//     std::vector<std::vector<std::uint16_t>> Adj = load_data(file_path, verbose);
//     solve_fast_v3(Adj, true);

//     return 0;

// }

int main(int argc, char *argv[]) {
    // 检查参数数量
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <input_file_path> <mode>" << std::endl;
        std::cerr << "Example: " << argv[0] << " ../data/att7.txt dp" << std::endl;
        std::cerr << "Available modes: dp | dp_fast | dp_fast_v2 | dp_fast_v3 | ref" << std::endl;
        return 1;
    }

    // 解析命令行参数
    std::string file_path = argv[1];
    std::string mode = argv[2];

    std::cout << "Input file: " << file_path << std::endl;
    std::cout << "Mode: " << mode << std::endl;

    bool verbose = true;

    // 加载数据
    std::vector<std::vector<std::uint16_t>> Adj;
    try {
        Adj = load_data(file_path, verbose);
    } catch (const std::exception &e) {
        std::cerr << "Error loading dataset: " << e.what() << std::endl;
        return 1;
    }

    // 根据模式选择算法
    std::vector<uint8_t> best_path;
    uint16_t best_length = 0;

    try {
        if (mode == "dp") {
            solve1(Adj, verbose);
        } else if (mode == "dp_fast") {
            solve_fast(Adj, verbose);
        } else if (mode == "dp_fast_v2") {
            solve_fast_v2(Adj, verbose);
        } else if (mode == "dp_fast_v3") {
            solve_fast_v3(Adj, verbose);
        } else if (mode == "ref") {
            solve_ref(Adj, verbose);
        } else {
            std::cerr << "Error: Unknown mode \"" << mode << "\"." << std::endl;
            std::cerr << "Available modes: dp | dp_fast | dp_fast_v2 | dp_fast_v3 | ref" << std::endl;
            return 1;
        }
    } catch (const std::exception &e) {
        std::cerr << "Error during TSP solving: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}