//
// Created by 21035 on 2025/11/01.
//

#ifndef REFALGORITHMS
#define REFALGORITHMS

#include <cstdint>
#include <vector>
#include <tuple>
#include <limits>
#include <iostream>
#include <algorithm>

std::tuple<std::vector<uint8_t>, uint16_t> TSP_2opt(const std::vector<std::vector<uint16_t>> &adj, bool verbose);
#endif //REFALGORITHMS