#include <iostream>
#include "algorithms.h"
#include "load_numbers.h"
#include <chrono>
#include <filesystem>

// pro1: 采用暴力搜索的方式，时间复杂度: O(n^2)
void solve_pro1(std::vector<uint32_t> & numbers)
{
    std::cout << "\n" << "Brute_force_search_pro: " << std::endl;
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::pair<std::vector<uint32_t>, uint32_t> results = Brute_force_search_pro(numbers);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The integer that appears the most times is : ";
    print_vector(results.first);
    std::cout << "and its number of occurrences: ";
    std::cout << results.second << std::endl;
}


void solve_pro2(std::vector<uint32_t> & numbers)
{
    std::cout << "\n" << "Merge_sort_search:  " << std::endl;
    std::vector<uint32_t> numbers_after_sorting(numbers.size());
    // pro2测量的时间包括归并排序以及最终扫描的时间总和
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    merge_sort(numbers,numbers_after_sorting, 0,numbers.size()-1);
    std::pair<std::vector<uint32_t>, uint32_t> results = search_max_counts(numbers_after_sorting);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The integer that appears the most times is : ";
    print_vector(results.first);
    std::cout << "and its number of occurrences: ";
    std::cout << results.second << std::endl;
}

void solve_pro3(std::vector<uint32_t> & numbers)
{
    std::cout << "\n" << "Divide_and_conquer_search:  " << std::endl;
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    result res = search_max_counts_with_merge_result(numbers, 0, numbers.size() - 1);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The integer that appears the most times is : ";
    print_vector(res.nums);
    std::cout << "and its number of occurrences: ";
    std::cout << res.counts << std::endl;
}

void solve_pro4(std::vector<uint32_t> & numbers)
{
    std::cout << "\n" << "hash_search:  " << std::endl;
    using clock = std::chrono::steady_clock;
    auto begin_time = clock::now();

    std::pair<std::vector<uint32_t>, uint32_t> results = search_max_counts_with_hash(numbers);

    auto end_time = clock::now();
    auto dur_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - begin_time).count();
    auto dur_ms = std::chrono::duration<double, std::milli>(end_time - begin_time).count();

    // 输出结果：运行时间以及查找结果
    std::cout << "Consumes: " << dur_ns << " ns (" << dur_ms << " ms)\n";
    std::cout << "The integer that appears the most times is : ";
    print_vector(results.first);
    std::cout << "and its number of occurrences: ";
    std::cout << results.second << std::endl;
}


int main() {
    std::cout << "Current working directory: "
              << std::filesystem::current_path() << std::endl;
    std::string filename = "./1000000.log";
    std::vector<uint32_t> numbers = get_numbers_from_log(filename);
    // Part1. 暴力搜索
    // solve_pro1(numbers);

    // // Part2. 排序扫描，先用归并排序将数组排序（复杂度O(nlogn)），然后一次遍历，统计出现次数最多的元素（复杂度O(n)，可能由多个元素）
    // solve_pro2(numbers);
    
    // // Part3. 利用分治算法 + unordered_map查找
    // solve_pro3(numbers);
    
    // Part4. 利用哈希表的思想。因为我们已知数组元素上界为数组长度的十分之一，因此直接开辟一个定长数组，扫描一次原数组并++即可
    solve_pro4(numbers);

    return 0;
}
