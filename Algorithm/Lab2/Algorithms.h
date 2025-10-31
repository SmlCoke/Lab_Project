//
// Created by 21035 on 2025/10/28.
//

#ifndef LAB2_ALGORITHMS_H
#define LAB2_ALGORITHMS_H
#include <cstdint>
#include <iostream>
#include <vector>
#include <tuple>
#include <bit>
#include <unordered_map>
#include <bits/stdc++.h>

std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp(const std::vector<std::vector<uint16_t>> & adj, bool verbose);
std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_fast(const std::vector<std::vector<uint16_t>> & adj, bool verbose);
std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_with_path(const std::vector<std::vector<uint16_t>> &adj, bool verbose);
#endif //LAB2_ALGORITHMS_H