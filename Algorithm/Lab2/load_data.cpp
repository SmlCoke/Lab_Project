//
// Created by 21035 on 2025/10/28.
//

#include "load_data.h"

#include <algorithm>

std::vector<std::vector<std::uint16_t>> load_data(const std::string & dataset, const bool & verbose) {
    // 打开文件
    std::cout << "input file path: " << dataset.c_str() << std::endl;
    std::ifstream infile(dataset);
    if (!infile.is_open()) {
        std::__throw_runtime_error("Error: cannot load in dataset");
    }

    uint16_t begin, end, weight;
    uint16_t n = 0;

    // 首次遍历确定城市数量上限（假设城市编号从0开始）
    std::vector<std::tuple<uint16_t, uint16_t, uint16_t>> edges;
    while (infile >> begin >> end >> weight) {
        edges.emplace_back(begin, end, weight);
        n = std::max(n, std::max(begin, end));
    }
    n += 1; // 城市编号从0开始，+1得到城市数

    // 初始化邻接矩阵
    const uint16_t Weight_INF = std::numeric_limits<uint16_t>::max() / 2; // 防止溢出
    std::vector<std::vector<uint16_t>> Adj(n, std::vector<uint16_t>(n, Weight_INF));

    // 自己到自己距离设为0
    for (uint16_t i = 0; i < n; ++i) Adj[i][i] = 0;

    // 读入边信息
    for (auto [u, v, w] : edges) {
        Adj[u][v] = w;
    }

    // 打印邻接矩阵
    if (verbose)
    {
        std::cout << "Adjacency Matrix: " << std::endl;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (Adj[i][j] == Weight_INF) std::cout << "INF\t";
                else std::cout << Adj[i][j] << "\t";
            }
            std::cout << std::endl;
        }
    }


    return Adj;
}
