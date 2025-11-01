//
// Created by 21035 on 2025/9/30.
//
#include "algorithms.h"
#include <iostream>

// 统计出现次数最多的整数及其出现次数：暴力搜索算法，O(n^2)
std::pair<std::vector<uint32_t>, uint32_t> Brute_force_search(std::vector<uint32_t>& numbers)
{
    // 定义输出
    std::pair<std::vector<uint32_t>, uint32_t> result;
    std::vector<uint32_t> nums; // 出现最多的整数

    uint32_t global_count = 0;
    uint32_t current_count = 0;
    uint32_t current_num = 0;

    // 暴力搜索找到出现次数最多的整数
    for (uint32_t i = 0; i < numbers.size(); i++)
    {
        current_num = numbers[i];
        current_count = 0;
        for (uint32_t j = 0; j < numbers.size(); j++)
        {
            if (numbers[j] == numbers[i])
            {
                current_count++;
            }
        }

        // 如果整数numbers[i]的出现次数少于全局最大出现次数，则掠过
        if (current_count < global_count) {
            continue;
        }
        // 如果当前整数出现次数等于全局最大出现次数，那么该整数以及之前记录的整数都有可能是出现次数的整数
        else if (current_count == global_count) {
            bool repeat = false;
            for (auto num: nums)
            {
                if (num == current_num)
                {
                    repeat = true;
                    continue;
                }
            }
            if (!repeat) nums.push_back(current_num);
        }
        // 如果当前整数的出现次数严格大于全局最大出现次数，那么记录该整数的信息
        else {
            nums.clear();  // 记录前，先清空此前记录的整数
            nums.push_back(current_num);
            global_count = current_count;
        }
    }

    result.first = nums;
    result.second = global_count;

    return result;
}

// Pro1: 暴力搜索改良版：重复元素不再搜索，但复杂度依旧是O(n^2)
std::pair<std::vector<uint32_t>, uint32_t> Brute_force_search_pro(std::vector<uint32_t>& numbers)
{
    // 定义输出
    std::pair<std::vector<uint32_t>, uint32_t> result;
    std::vector<uint32_t> nums; // 出现最多的整数

    uint32_t global_count = 0;
    uint32_t current_count = 0;
    uint32_t current_num = 0;
    std::set<uint32_t> accessed_number;
    // 暴力搜索找到出现次数最多的整数
    for (uint32_t i = 0; i < numbers.size(); i++)
    {
        current_num = numbers[i];
        current_count = 0;

        if (accessed_number.count(current_num))
        {
            continue;
        }
        else
        {
            accessed_number.insert(current_num);
        }
        for (uint32_t j = 0; j < numbers.size(); j++)
        {
            if (numbers[j] == numbers[i])
            {
                current_count++;
            }
        }

        // 如果整数numbers[i]的出现次数少于全局最大出现次数，则掠过
        if (current_count < global_count) {
            continue;
        }
        // 如果当前整数出现次数等于全局最大出现次数，那么该整数以及之前记录的整数都有可能是出现次数的整数
        else if (current_count == global_count) {
            bool repeat = false;
            for (auto num: nums)
            {
                if (num == current_num)
                {
                    repeat = true;
                    continue;
                }
            }
            if (!repeat) nums.push_back(current_num);
        }
        // 如果当前整数的出现次数严格大于全局最大出现次数，那么记录该整数的信息
        else {
            nums.clear();  // 记录前，先清空此前记录的整数
            nums.push_back(current_num);
            global_count = current_count;
        }
    }

    result.first = nums;
    result.second = global_count;

    return result;
}

// 归并排序函数
void merge_sort(std::vector<uint32_t> & numbers, std::vector<uint32_t> & results, uint32_t begin, uint32_t end)
{
    if (begin < end)
    {
        uint32_t middle = (begin + end)/2;
        merge_sort(numbers, results, begin, middle);
        merge_sort(numbers, results, middle + 1, end);
        merge(numbers, results, begin, middle, end);
    }
}
// 归并排序的合并函数
void merge(std::vector<uint32_t> & numbers, std::vector<uint32_t> & results, uint32_t begin, uint32_t mid, uint32_t end)
{
    uint32_t L_index = begin;
    uint32_t R_index = mid + 1;
    uint32_t index = begin;
    while (L_index <= mid && R_index <= end)
    {
        if (numbers[L_index] <= numbers[R_index])
        {
            results.at(index++) = numbers.at(L_index++); // 左侧元素更小，移入左侧元素
        }
        else
        {
            results.at(index++) = numbers.at(R_index++); // 右侧元素更小，移入右侧元素
        }
    }
    while (R_index <= end) results.at(index++) = numbers.at(R_index++);

    while (L_index <= mid) results.at(index++) = numbers.at(L_index++);

    // 将排序好的元素按需存回numbers，否则归并时会按照原数组的顺序排序
    for (uint32_t i = begin; i <= end; i++)
        numbers[i] = results[i];
}

// 基于有序数组的线性扫描函数，确定有序数组中出现次数最多的函数以及出现次数
std::pair<std::vector<uint32_t>, uint32_t> search_max_counts(std::vector<uint32_t>& numbers)
{
    std::pair<std::vector<uint32_t>, uint32_t> result;
    std::vector<uint32_t> nums;
    uint32_t global_count = 0;
    uint32_t current_count = 0;
    uint32_t current_num = numbers[0];
    for (unsigned int number : numbers)
    {

        if (number == current_num)
        {
            current_count++;
        }
        else  // 如果当前访问的正整数不等于当前记录的正整数，则代表记录的正整数段访问结束，可以更新全局信息
        {
            if (current_count > global_count) // 当前正整数的出现次数已经超过了最大出现次数，更新
            {
                global_count = current_count;
                nums.clear();
                nums.push_back(current_num);
            }
            else if (current_count == global_count) // 当前正整数的出现次数等于最大出现次数，保留
            {
                nums.push_back(current_num);
            }

            current_num = number;
            current_count = 1;
        }
    }

    result.first = nums;
    result.second = global_count;

    return result;

}

// Pro3. 分治算法 + unordered_map，合并映射表
result search_max_counts_with_merge_result(std::vector<uint32_t> & numbers, uint32_t begin, uint32_t end)
{
    result res;
    if (begin > end)
    {
        return res;
        // 返回一个空的频率映射表
    }

    else if (begin == end)
    {
        res.freq_map = new std::unordered_map<uint32_t, uint32_t>;
        res.nums.push_back(numbers[begin]);
        res.counts = 1;
        (*(res.freq_map))[numbers[begin]] = 1;
        return res;
    }

    else  // 如果 begin < end 执行正常分治操作
    {
        uint32_t mid = (begin + end)/2;
        result res_Left = search_max_counts_with_merge_result(numbers, begin, mid);
        result res_Right = search_max_counts_with_merge_result(numbers, mid + 1, end);

        // 将返回得到的两个小映射表合并为一个大映射表
        // 合并策略：遍历更小的映射表，尽可能避免带来额外开销
        // 遍历小映射表的复杂度为O(k)，k = n/2, n/4, ..., 在大映射表中查找元素的复杂度为O(1)
        // 交换一次，确保Left为小映射表
        if (res_Left.freq_map->size() > res_Right.freq_map->size())
        {
            std::swap(res_Left, res_Right);
        }

        for (auto & freq_pair : *(res_Left.freq_map))
        {
            uint32_t current_num =freq_pair.first;
            uint32_t current_count = freq_pair.second;

            // 在较大的映射表中搜索当前整数
            auto it = res_Right.freq_map->find(current_num);
            if (it != res_Right.freq_map->end())
            {
                // 如果找到此元素，合并出现次数
                it->second += current_count;

                // 合并后元素出现次数等于当前最大出现次数，添加进入nums
                if (it->second == res_Right.counts)
                {
                    res_Right.nums.push_back(current_num);
                }

                // 合并后元素出现次数大于当前最大出现次数，更新
                if (it->second > res_Right.counts)
                {
                    res_Right.nums.clear();
                    res_Right.nums.shrink_to_fit();
                    res_Right.nums.push_back(current_num);
                    res_Right.counts = it->second;
                }
            }
            else
            {
                // 如果未找到此元素，添加
                (*(res_Right.freq_map))[current_num] = current_count;

                // 添加后元素出现次数等于当前最大出现次数，添加进入nums
                if (current_count == res_Right.counts)
                {
                    res_Right.nums.push_back(current_num);
                }

                // 合并后元素出现次数大于当前最大出现次数，更新
                if (current_count > res_Right.counts)
                {
                    res_Right.nums.clear();
                    res_Right.nums.shrink_to_fit();
                    res_Right.nums.push_back(current_num);
                    res_Right.counts = current_count;
                }
            }
        }

        delete res_Left.freq_map;
        return res_Right;

    }
}

// Pro4. 基于哈希表的思想，将实际整数作为数组索引，将出现次数作为数组中的值
std::pair<std::vector<uint32_t>, uint32_t> search_max_counts_with_hash(std::vector<uint32_t>& numbers)
{
    std::pair<std::vector<uint32_t>, uint32_t> result;
    uint32_t length = numbers.size();
    uint32_t * map = new uint32_t[length];
    for (uint32_t i = 0; i < length; i++)
    {
        map[i] = 0;
    }
    for (auto number : numbers) {
        map[number]++;
    }

    std::vector<uint32_t> nums;
    uint32_t global_count = 0;
    for (uint32_t i = 0; i < length; i++)
    {
        if (map[i] > global_count)
        {
            global_count = map[i];
            nums.clear();
            nums.push_back(i);
        }
        else if (map[i] ==global_count)
        {
            nums.push_back(i);
        }
    }

    result.first = nums;
    result.second = global_count;

    return result;

}


// 打印vector信息
void print_vector(const std::vector<uint32_t> & numbers)
{
    for (auto number : numbers) {
        std::cout << number << " ";
    }
    std::cout << std::endl;
}