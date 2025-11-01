//
// Created by 21035 on 2025/9/30.
//

#ifndef LAB1_ALGORITHMS_H
#define LAB1_ALGORITHMS_H
#include <utility>
#include <vector>
#include <set>
#include <unordered_map>

#include "stdint.h"

// Pro1: 统计出现次数最多的整数及其出现次数：暴力搜索算法，O(n^2)
std::pair<std::vector<uint32_t>, uint32_t> Brute_force_search(std::vector<uint32_t>& numbers);
// Pro1: 暴力搜索改良版：重复元素不再搜索，但复杂度依旧是O(n^2)
std::pair<std::vector<uint32_t>, uint32_t> Brute_force_search_pro(std::vector<uint32_t>& numbers);

// Pro2: 先排序，后扫描，采用排序方式为归并排序
// 归并排序函数
void merge_sort(std::vector<uint32_t> & numbers, std::vector<uint32_t> & results, uint32_t begin, uint32_t end);
// 归并排序的合并函数
void merge(std::vector<uint32_t> & numbers, std::vector<uint32_t> & results, uint32_t begin, uint32_t mid, uint32_t end);
// // 基于有序数组的线性扫描函数，确定有序数组中出现次数最多的函数以及出现次数
std::pair<std::vector<uint32_t>, uint32_t> search_max_counts(std::vector<uint32_t>& numbers);

// Pro3： 分治算法，构建并合并映射表，T(n)=2T(n/2)+O(n)，时间复杂度为O(nlogn)
// 线性扫描小映射表，带来的时间复杂度开销为:O(n)，但是对于小映射表中的每一个键，在大映射表中获取只需要O(1)复杂度
// 因此最终之间复杂度还是: O(nlogn)
// 但是本算法实际上还是利用了哈希表unordered_map，算不上纯分治算法？
struct result {
    std::unordered_map<uint32_t, uint32_t>* freq_map; // 频率映射表，用指针，防止交换操作和函数返回时造成大量拷贝开销
    std::vector<uint32_t> nums;                  // 当前出现次数最多的整数
    uint32_t counts;                          // 当前出现次数最多的整数出现的次数
    result() : freq_map(nullptr), nums(), counts(0) {}
};
result search_max_counts_with_merge_result(std::vector<uint32_t> & numbers, uint32_t begin, uint32_t end);

// Pro4. 基于哈希表的思想
std::pair<std::vector<uint32_t>, uint32_t> search_max_counts_with_hash(std::vector<uint32_t>& numbers);

// 打印vector信息
void print_vector(const std::vector<uint32_t> & numbers);
#endif //LAB1_ALGORITHMS_H