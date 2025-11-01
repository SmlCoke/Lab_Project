//
// Created by 21035 on 2025/9/30.
//
#include "load_numbers.h"

std::vector<uint32_t> get_numbers_from_log(const std::string & filename)
{
    std::vector<uint32_t> numbers;

    // 读入文件
    std::ifstream infile(filename);

    if (!infile.is_open()) {
        throw("Log file cannot be open ");
    }

    int value;

    // 逐个读入整数
    while (infile >> value) {
        numbers.push_back(value);
    }
    infile.close();

    return numbers;
}
