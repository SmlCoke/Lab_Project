# include "RefAlgorithms.h"
// ---------------- 工具函数 ----------------

// 计算路径总长度
static uint16_t path_length(const std::vector<uint8_t> &path,
                            const std::vector<std::vector<uint16_t>> &adj) {
    uint16_t total = 0;
    for (std::size_t i = 0; i + 1 < path.size(); ++i) {
        total += adj[path[i]][path[i + 1]];
    }
    return total;
}

// 最近邻算法生成初始路径
static std::vector<uint8_t> nearest_neighbor(const std::vector<std::vector<uint16_t>> &adj) {
    const uint8_t n = static_cast<uint8_t>(adj.size());
    std::vector<uint8_t> path;
    std::vector<bool> visited(n, false);

    path.reserve(n + 1);
    uint8_t current = 0;
    path.push_back(current);
    visited[current] = true;

    for (uint8_t step = 1; step < n; ++step) {
        uint16_t best_cost = std::numeric_limits<uint16_t>::max();
        uint8_t next_city = 0;
        for (uint8_t j = 0; j < n; ++j) {
            if (!visited[j] && adj[current][j] < best_cost) {
                best_cost = adj[current][j];
                next_city = j;
            }
        }
        path.push_back(next_city);
        visited[next_city] = true;
        current = next_city;
    }

    path.push_back(0); // 回到起点
    return path;
}

// 2-opt 改进算法
static bool two_opt(std::vector<uint8_t> &path,
                    const std::vector<std::vector<uint16_t>> &adj) {
    bool improved = false;
    const std::size_t n = path.size() - 1;

    for (std::size_t i = 1; i < n - 2; ++i) {
        for (std::size_t j = i + 1; j < n - 1; ++j) {
            uint16_t before = adj[path[i - 1]][path[i]] + adj[path[j]][path[j + 1]];
            uint16_t after  = adj[path[i - 1]][path[j]] + adj[path[i]][path[j + 1]];
            if (after < before) {
                std::reverse(path.begin() + i, path.begin() + j + 1);
                improved = true;
            }
        }
    }

    return improved;
}

// ---------------- 主函数接口 ----------------

std::tuple<std::vector<uint8_t>, uint16_t>
TSP_2opt(const std::vector<std::vector<uint16_t>> &adj, bool verbose = false) {
    // 最近邻生成初解
    std::vector<uint8_t> path = nearest_neighbor(adj);
    uint16_t best_length = path_length(path, adj);

    // 使用 2-opt 局部优化
    bool improved = true;
    while (improved) {
        improved = two_opt(path, adj);
        uint16_t new_length = path_length(path, adj);
        if (new_length < best_length) {
            best_length = new_length;
        }
    }

    // 输出（可选）
    if (verbose) {
        std::cout << "Best length: " << best_length << "\nPath: ";
        for (const auto &v : path) {
            std::cout << static_cast<int>(v) << ' ';
        }
        std::cout << std::endl;
    }

    return {path, best_length};
}
