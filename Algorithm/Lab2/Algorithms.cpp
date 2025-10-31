//
// Created by 21035 on 2025/10/28.
//

#include "Algorithms.h"


struct state {
    uint32_t mask;
    // 掩码mask，1代表接下来要去访问的结点
    // 我们只需要考虑LSB为1的mask序列
    uint8_t curr; // 从curr开始访问Mask中的结点
    bool operator==(const state &other) const noexcept {
        return mask == other.mask && curr == other.curr;
    }
};

struct statehash {
    // 自定义哈希函数，讲mask左移五位，为当前城市编号（0~29<32=2^5）腾出空间
    size_t operator()(const state &s) const noexcept {
        return ((uint64_t)s.mask << 5) ^ s.curr;
    }
};

std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::unordered_map<state, uint16_t, statehash> dp_solved;
    std::unordered_map<state, uint16_t, statehash> dp_curr;
\
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp_solved[{1,0}] = 0;
    dp_curr[{1,0}] = 0;

    // 集合V'中的结点数量，从2开始遍历到node_nums - 1
    for (uint8_t node_num = 2; node_num <= node_nums; node_num++)
    {
        for (uint32_t mask_index = 1; mask_index < mask_nums; mask_index = mask_index + 2)
        {
            // 如果结点0位置处为0，则不需要考虑这些序列，我们默认结点0处的值为1，这样就能排除一半序列

            // 如果mask_index序列中的1的个数不等于node_num，也即即将访问的结点个数不匹配，则跳过该序列
            if (std::popcount(mask_index) != node_num) continue;

            for (uint8_t node_index = 1; node_index < node_nums; node_index++)
            {
                if (!(mask_index & (1 << node_index))) continue; // 当前结点不在集合V'中，跳过

                uint32_t solved_index = mask_index ^ (1 << node_index); // 在当前集合序列中删除该结点

                uint16_t best_length = std::numeric_limits<uint16_t>::max();
                
                // 遍历新的集合序列中的结点，寻找下一个访问的结点是多少时，能够使得当前dp[mask_index][node_index]最小
                for (uint8_t node_j = 0; node_j < node_nums; node_j++)
                {
                    // 这里node_j从0开始，是为了处理node_num=2的边界情况
                    // 不会有将{mask_index, 0}添加进入dp_curr的情况，因为node_index从1开始
                    if (node_j == node_index)  continue; // 删除不可能情况

                    if (node_j == 0 && node_num != 2) continue;  // 排除边界情况

                    if (!(solved_index & 1 << node_j)) continue; // 结点j不在待访问结点集合中

                    auto it = dp_solved.find({solved_index, node_j});
                    if (it != dp_solved.end())
                    {
                        uint16_t candidate = it->second + adj[node_index][node_j];
                        if (candidate < best_length)
                        {
                            best_length = candidate;
                        }
                    }

                    else
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    dp_curr[{mask_index, node_index}] = best_length;
                    // child[{mask_index, node_index}] = best_node_j;
                }
                else
                {
                    std::__throw_runtime_error("Error: A best_length was calculated to be INF!");
                }

            }
        }
        dp_solved = dp_curr;
        dp_curr.clear();
        dp_curr.rehash(0);

    }

    uint16_t best_length = std::numeric_limits<uint16_t>::max();
    uint8_t best_first_node_index = 0;
    // 最佳路径中的第一个结点，用于生成完整路径
    uint32_t full_index = (1 << node_nums) - 1;
    for (uint8_t node_index = 1; node_index < node_nums; node_index++)
    {
        if (dp_solved[{full_index, node_index}] + adj[0][node_index] < best_length)
        {
            best_length = dp_solved[{full_index, node_index}] + adj[0][node_index];
            best_first_node_index = node_index;
        }
    }

    return {{0,0}, best_length};

}

std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_fast(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::vector<std::vector<uint16_t>> dp(mask_nums, std::vector<uint16_t>(node_nums, INF));
    std::vector<std::vector<uint8_t>> next_node(mask_nums, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp[1][0] = 0;


    // 集合V'中的结点数量，从2开始遍历到node_nums - 1
    for (uint8_t node_num = 2; node_num <= node_nums; node_num++)
    {
        for (uint32_t mask_index = 1; mask_index < mask_nums; mask_index = mask_index + 2)
        {
            // 如果结点0位置处为0，则不需要考虑这些序列，我们默认结点0处的值为1，这样就能排除一半序列

            // 如果mask_index序列中的1的个数不等于node_num，也即即将访问的结点个数不匹配，则跳过该序列
            if (std::popcount(mask_index) != node_num) continue;

            for (uint8_t node_index = 1; node_index < node_nums; node_index++)
            {
                if (!(mask_index & (1 << node_index))) continue; // 当前结点不在集合V'中，跳过

                uint32_t solved_index = mask_index ^ (1 << node_index); // 在当前集合序列中删除该结点

                uint16_t best_length = std::numeric_limits<uint16_t>::max();
                uint8_t best_node_j = 0; // 当前状态的最优后继结点

                // 遍历新的集合序列中的结点，寻找下一个访问的结点是多少时，能够使得当前dp[mask_index][node_index]最小
                for (uint8_t node_j = 0; node_j < node_nums; node_j++)
                {
                    // 这里node_j从0开始，是为了处理node_num=2的边界情况
                    // 不会有将{mask_index, 0}添加进入dp_curr的情况，因为node_index从1开始
                    if (node_j == node_index)  continue; // 删除不可能情况

                    if (node_j == 0 && node_num != 2) continue;  // 排除边界情况

                    if (!(solved_index & 1 << node_j)) continue; // 结点j不在待访问结点集合中

                    if (dp[solved_index][node_j] == INF)
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                    uint16_t candidate = dp[solved_index][node_j] + adj[node_index][node_j];
                    if (candidate < best_length)
                    {
                        best_length = candidate;
                        best_node_j = node_j;
                    }
                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    dp[mask_index][node_index] = best_length;
                    next_node[mask_index][node_index] = best_node_j;
                }
                else
                {
                    std::__throw_runtime_error("Error: A best_length was calculated to be INF!");
                }

            }
        }

    }

    uint16_t best_length = std::numeric_limits<uint16_t>::max();
    uint8_t best_first_node_index = 0;
    // 最佳路径中的第一个结点，用于生成完整路径
    uint32_t full_index = (1 << node_nums) - 1;
    for (uint8_t node_index = 1; node_index < node_nums; node_index++)
    {
        if (dp[full_index][node_index] + adj[0][node_index] < best_length)
        {
            best_length = dp[full_index][node_index] + adj[0][node_index];
            best_first_node_index = node_index;
        }
    }

    // 根据 next_node 回溯最优路径（修复）
    std::vector<uint8_t> best_path;
    best_path.reserve(node_nums + 1);
    best_path.push_back(0); // 起点
    uint8_t current_node = best_first_node_index;
    uint32_t mask = full_index;
    best_path.push_back(current_node);

    while (mask != 1) { // 只剩下起点0时停止
        uint8_t next = next_node[mask][current_node];
        if (next == 255) {
            std::__throw_runtime_error("Error: invalid next_node (255) during path reconstruction.");
        }
        mask ^= (1u << current_node); // 注销当前结点
        current_node = next;
        best_path.push_back(current_node);
    }

    return {best_path, best_length};

}

// 帮助函数：计算给定状态(mask, curr)的DP值，按需计算
uint16_t compute_dp_val(uint32_t mask, uint8_t curr, const std::vector<std::vector<uint16_t>>& adj,
                        std::unordered_map<state, uint16_t, statehash>& memo)
{
    // 检查是否已计算
    auto it = memo.find({mask, curr});
    if (it != memo.end()) {
        return it->second;
    }
    
    // 基础情况
    if (mask == 1 && curr == 0) {
        return 0;
    }
    
    // 计算
    uint32_t prev_mask = mask ^ (1u << curr);
    uint16_t best = std::numeric_limits<uint16_t>::max() / 2;
    
    for (uint8_t j = 0; j < adj.size(); j++) {
        if (!(prev_mask & (1u << j))) continue;
        
        uint16_t prev_val = compute_dp_val(prev_mask, j, adj, memo);
        uint16_t candidate = prev_val + adj[curr][j];
        if (candidate < best) {
            best = candidate;
        }
    }
    
    memo[{mask, curr}] = best;
    return best;
}

std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_fast_pro(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size();
    uint32_t full_mask = (1 << node_nums) - 1;

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    // 使用记忆化递归，只计算需要的状态
    std::unordered_map<state, uint16_t, statehash> memo;
    memo[{1, 0}] = 0;
    
    // 查找最优解
    uint16_t best_length = INF;
    uint8_t best_first_node = 0;
    
    for (uint8_t node_index = 1; node_index < node_nums; node_index++)
    {
        uint16_t val = compute_dp_val(full_mask, node_index, adj, memo);
        if (val + adj[0][node_index] < best_length)
        {
            best_length = val + adj[0][node_index];
            best_first_node = node_index;
        }
    }

    // 重建路径：从终点回溯，每次找最优前驱
    std::vector<uint8_t> best_path;
    best_path.reserve(node_nums + 1);
    best_path.push_back(0);
    best_path.push_back(best_first_node);
    
    uint8_t current_node = best_first_node;
    uint32_t mask = full_mask;
    
    while (mask != 1) {
        uint32_t prev_mask = mask ^ (1u << current_node);
        uint16_t current_val = compute_dp_val(mask, current_node, adj, memo);
        
        // 找最优前驱
        uint8_t next_node = 255;
        for (uint8_t j = 0; j < node_nums; j++) {
            if (!(prev_mask & (1u << j))) continue;
            
            uint16_t prev_val = compute_dp_val(prev_mask, j, adj, memo);
            if (prev_val + adj[current_node][j] == current_val) {
                next_node = j;
                break;
            }
        }
        
        if (next_node == 255) {
            std::__throw_runtime_error("Error: Cannot find next node in path reconstruction!");
        }
        
        mask = prev_mask;
        current_node = next_node;
        best_path.push_back(current_node);
    }

    return {best_path, best_length};
}
