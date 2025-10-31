//
// Created by 21035 on 2025/10/28.
//

#ifndef LAB2_LOAD_DATA_H
#define LAB2_LOAD_DATA_H
#include <cstdint>
#include <iostream>
#include <fstream>
#include <vector>
#include <limits>

std::vector<std::vector<std::uint16_t>> load_data(const std::string & dataset, const bool & verbose);
#endif //LAB2_LOAD_DATA_H