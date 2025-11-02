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

// 改进版本，尝试减少一些不必要的计算：由于只会利用LSP=1的mask_index进行，因此没必要为MSP=0的mask_index开辟空间
std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_fast_v2(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::vector<std::vector<uint16_t>> dp(mask_nums/2, std::vector<uint16_t>(node_nums, INF));
    std::vector<std::vector<uint8_t>> next_node(mask_nums/2, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp[1/2][0] = 0;


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

                    if (dp[solved_index/2][node_j] == INF)
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                    uint16_t candidate = dp[solved_index/2][node_j] + adj[node_index][node_j];
                    if (candidate < best_length)
                    {
                        best_length = candidate;
                        best_node_j = node_j;
                    }
                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    dp[mask_index/2][node_index] = best_length;
                    next_node[mask_index/2][node_index] = best_node_j;
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
        if (dp[full_index/2][node_index] + adj[0][node_index] < best_length)
        {
            best_length = dp[full_index/2][node_index] + adj[0][node_index];
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
        uint8_t next = next_node[mask/2][current_node];
        if (next == 255) {
            std::__throw_runtime_error("Error: invalid next_node (255) during path reconstruction.");
        }
        mask ^= (1u << current_node); // 注销当前结点
        current_node = next;
        best_path.push_back(current_node);
    }

    return {best_path, best_length};

}


// --------------------- solve_TSP_with_dp_fast_v3 辅助函数 ---------------------
// 预计算组合数表，comb_table[n][k]表示从n个元素中选取k个元素的组合数
// 传入参数n : 最大的数
std::vector<std::vector<uint32_t>> load_combinational_table(const std::uint8_t n)
{
    std::vector<std::vector<uint32_t>> comb_table(n + 1, std::vector<uint32_t>(n + 1, 0));
    for (std::uint8_t i = 0; i <= n; ++i) {
        comb_table[i][0] = 1; // 从i个元素中选0个元素的组合数为1
        comb_table[i][i] = 1; // 从i个元素中选i个元素的组合数为1
        for (std::uint8_t j = 1; j < i; ++j) {
            comb_table[i][j] = comb_table[i - 1][j - 1] + comb_table[i - 1][j];
            // 动态规划计算，状态转移方程！
        }
    }
    return comb_table;
}

uint32_t combination_index(uint32_t a, uint8_t M, uint8_t N, const std::vector<std::vector<uint32_t>> & C)
{
    // 计算组合数二进制序列在所有C(M,N)种组合中的索引（最低索引从0开始）
    uint32_t index = 0;
    uint8_t count = 0;
    for (uint8_t i = 0; i < M; ++i) {
        if (a & (1u << i)) {
            ++count;
            index += C[i][count];
        }
    }
    return index;
}

uint8_t arg_combination_index(uint32_t index, uint8_t M, uint8_t N, const std::vector<std::vector<uint32_t>> & C)
{
    // 根据组合数二进制序列的索引，反向计算出对应的二进制序列
    uint8_t a = 0;
    uint8_t count = N;
    for (int8_t i = M - 1; i >= 0; --i) {
        if (index >= C[i][count]) {
            a |= (1u << i);
            index -= C[i][count];
            --count;
        }
        if (count == 0) break; // 提前结束
    }
    return a;
}


std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_fast_v3(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    std::vector<std::vector<uint32_t>> comb_table = load_combinational_table(node_nums); // 预计算组合数表

    std::vector<std::vector<uint16_t>> dp_prev(1, std::vector<uint16_t>(node_nums, INF));  // 记录节点个数为node_num-1的各个掩码对应路径总长
    std::vector<std::vector<uint16_t>> dp_curr(1, std::vector<uint16_t>(node_nums, INF));  // 记录节点个数为node_num的各个掩码对应路径总长
    std::vector<std::vector<uint8_t>> next_node(mask_nums/2, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp_prev[0][0] = 0;

    // 集合V'中的结点数量，从2开始遍历到node_nums - 1
    for (uint8_t node_num = 2; node_num <= node_nums; node_num++)
    {
        dp_curr.resize(comb_table[node_nums-1][node_num-1], std::vector<uint16_t>(node_nums, INF));
        // 我们不为LSP=1的序列分配存储空间，那么考虑node_num数量的结点时，所需要存储的二进制序列只有C_{node_nums-1}^{node_num-1}
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
                    
                    // 计算solved_index在组合数集合中的索引，对应其在dp_prev中的index
                    uint32_t solved_index_index = combination_index(solved_index>>1, node_nums-1, node_num-2, comb_table);

                    if (dp_prev[solved_index_index][node_j] == INF)
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                    uint16_t candidate = dp_prev[solved_index_index][node_j] + adj[node_index][node_j];
                    if (candidate < best_length)
                    {
                        best_length = candidate;
                        best_node_j = node_j;
                    }
                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    // 计算mask_index在c(node_nums-1, node_num-1)中的索引
                    uint32_t mask_index_index = combination_index(mask_index>>1, node_nums-1, node_num-1, comb_table);
                    dp_curr[mask_index_index][node_index] = best_length;
                    next_node[mask_index/2][node_index] = best_node_j;
                }
                else
                {
                    std::__throw_runtime_error("Error: A best_length was calculated to be INF!");
                }

            }
        }

        // 将当前一层的数据搬到dp_prev，然后清空dp_curr
        dp_prev = std::move(dp_curr);
        std::vector<std::vector<uint16_t>>().swap(dp_curr);

    }

    uint16_t best_length = std::numeric_limits<uint16_t>::max();
    uint8_t best_first_node_index = 0;
    // 最佳路径中的第一个结点，用于生成完整路径
    uint32_t full_index = (1 << node_nums) - 1;
    uint32_t full_index_index = combination_index(full_index>>1, node_nums-1, node_nums-1,comb_table);
    for (uint8_t node_index = 1; node_index < node_nums; node_index++)
    {
        if (dp_prev[full_index_index][node_index] + adj[0][node_index] < best_length)
        {
            best_length = dp_prev[full_index_index][node_index] + adj[0][node_index];
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
        uint8_t next = next_node[mask/2][current_node];
        if (next == 255) {
            std::__throw_runtime_error("Error: invalid next_node (255) during path reconstruction.");
        }
        mask ^= (1u << current_node); // 注销当前结点
        current_node = next;
        best_path.push_back(current_node);
    }

    return {best_path, best_length};

}
// ======================= Statistics Tracking Versions =======================

std::tuple<std::vector<uint8_t>, uint16_t, uint64_t, uint64_t> solve_TSP_with_dp_with_stat(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    uint64_t total_subproblems = 0;  // 所有子问题数（包括重复）
    uint64_t unique_subproblems = 0; // 首次出现的子问题数（不计重复）

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::unordered_map<state, uint16_t, statehash> dp_solved;
    std::unordered_map<state, uint16_t, statehash> dp_curr;

    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp_solved[{1,0}] = 0;
    dp_curr[{1,0}] = 0;
    unique_subproblems++; // 初始状态

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

                    total_subproblems++; // 访问子问题
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
                    unique_subproblems++; // 新子问题
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
        total_subproblems++; // 最后查找最优解也计入
        if (dp_solved[{full_index, node_index}] + adj[0][node_index] < best_length)
        {
            best_length = dp_solved[{full_index, node_index}] + adj[0][node_index];
            best_first_node_index = node_index;
        }
    }

    // 注意：此版本不实现路径重建，返回占位符路径（与原solve_TSP_with_dp函数行为一致）
    return {{0,0}, best_length, total_subproblems, unique_subproblems};

}

std::tuple<std::vector<uint8_t>, uint16_t, uint64_t, uint64_t> solve_TSP_with_dp_fast_with_stat(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    uint64_t total_subproblems = 0;  // 所有子问题数（包括重复）
    uint64_t unique_subproblems = 0; // 首次出现的子问题数（不计重复）

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::vector<std::vector<uint16_t>> dp(mask_nums, std::vector<uint16_t>(node_nums, INF));
    std::vector<std::vector<uint8_t>> next_node(mask_nums, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp[1][0] = 0;
    unique_subproblems++; // 初始状态


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

                    total_subproblems++; // 访问子问题
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
                    unique_subproblems++; // 新子问题
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
        total_subproblems++; // 最后查找最优解也计入
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

    return {best_path, best_length, total_subproblems, unique_subproblems};

}

std::tuple<std::vector<uint8_t>, uint16_t, uint64_t, uint64_t> solve_TSP_with_dp_fast_v2_with_stat(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    uint64_t total_subproblems = 0;  // 所有子问题数（包括重复）
    uint64_t unique_subproblems = 0; // 首次出现的子问题数（不计重复）

    // 键值对一次存放：需要访问的结点(必定包含0), 当前结点编号(0~29), 遍历一遍回到0的路径权重
    std::vector<std::vector<uint16_t>> dp(mask_nums/2, std::vector<uint16_t>(node_nums, INF));
    std::vector<std::vector<uint8_t>> next_node(mask_nums/2, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp[1/2][0] = 0;
    unique_subproblems++; // 初始状态


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

                    total_subproblems++; // 访问子问题
                    if (dp[solved_index/2][node_j] == INF)
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                    uint16_t candidate = dp[solved_index/2][node_j] + adj[node_index][node_j];
                    if (candidate < best_length)
                    {
                        best_length = candidate;
                        best_node_j = node_j;
                    }
                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    dp[mask_index/2][node_index] = best_length;
                    next_node[mask_index/2][node_index] = best_node_j;
                    unique_subproblems++; // 新子问题
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
        total_subproblems++; // 最后查找最优解也计入
        if (dp[full_index/2][node_index] + adj[0][node_index] < best_length)
        {
            best_length = dp[full_index/2][node_index] + adj[0][node_index];
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
        uint8_t next = next_node[mask/2][current_node];
        if (next == 255) {
            std::__throw_runtime_error("Error: invalid next_node (255) during path reconstruction.");
        }
        mask ^= (1u << current_node); // 注销当前结点
        current_node = next;
        best_path.push_back(current_node);
    }

    return {best_path, best_length, total_subproblems, unique_subproblems};

}

std::tuple<std::vector<uint8_t>, uint16_t, uint64_t, uint64_t> solve_TSP_with_dp_fast_v3_with_stat(const std::vector<std::vector<uint16_t>> & adj, bool verbose)
{
    uint8_t node_nums = adj.size(); // 结点数量
    uint32_t mask_nums = 1 << node_nums; // 掩码数量，即所有可能使用到的结点集合的数量

    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    uint64_t total_subproblems = 0;  // 所有子问题数（包括重复）
    uint64_t unique_subproblems = 0; // 首次出现的子问题数（不计重复）

    std::vector<std::vector<uint32_t>> comb_table = load_combinational_table(node_nums); // 预计算组合数表

    std::vector<std::vector<uint16_t>> dp_prev(1, std::vector<uint16_t>(node_nums, INF));  // 记录节点个数为node_num-1的各个掩码对应路径总长
    std::vector<std::vector<uint16_t>> dp_curr(1, std::vector<uint16_t>(node_nums, INF));  // 记录节点个数为node_num的各个掩码对应路径总长
    std::vector<std::vector<uint8_t>> next_node(mask_nums/2, std::vector<uint8_t>(node_nums, 255)); // 记录当前状态的最优后继结点
    // 从结点0开始，遍历结点集合{0}并回到结点0的路径长度为0
    dp_prev[0][0] = 0;
    unique_subproblems++; // 初始状态

    // 集合V'中的结点数量，从2开始遍历到node_nums - 1
    for (uint8_t node_num = 2; node_num <= node_nums; node_num++)
    {
        dp_curr.resize(comb_table[node_nums-1][node_num-1], std::vector<uint16_t>(node_nums, INF));
        // 我们不为LSP=1的序列分配存储空间，那么考虑node_num数量的结点时，所需要存储的二进制序列只有C_{node_nums-1}^{node_num-1}
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
                    
                    // 计算solved_index在组合数集合中的索引，对应其在dp_prev中的index
                    uint32_t solved_index_index = combination_index(solved_index>>1, node_nums-1, node_num-2, comb_table);

                    total_subproblems++; // 访问子问题
                    if (dp_prev[solved_index_index][node_j] == INF)
                    {
                        std::__throw_runtime_error("Error: Cannot find the solution which should be get when solving the previous sub-problem!");
                    }

                    uint16_t candidate = dp_prev[solved_index_index][node_j] + adj[node_index][node_j];
                    if (candidate < best_length)
                    {
                        best_length = candidate;
                        best_node_j = node_j;
                    }
                }

                if (best_length != std::numeric_limits<uint16_t>::max())
                {
                    // 计算mask_index在c(node_nums-1, node_num-1)中的索引
                    uint32_t mask_index_index = combination_index(mask_index>>1, node_nums-1, node_num-1, comb_table);
                    dp_curr[mask_index_index][node_index] = best_length;
                    next_node[mask_index/2][node_index] = best_node_j;
                    unique_subproblems++; // 新子问题
                }
                else
                {
                    std::__throw_runtime_error("Error: A best_length was calculated to be INF!");
                }

            }
        }

        // 将当前一层的数据搬到dp_prev，然后清空dp_curr
        dp_prev = std::move(dp_curr);
        std::vector<std::vector<uint16_t>>().swap(dp_curr);

    }

    uint16_t best_length = std::numeric_limits<uint16_t>::max();
    uint8_t best_first_node_index = 0;
    // 最佳路径中的第一个结点，用于生成完整路径
    uint32_t full_index = (1 << node_nums) - 1;
    uint32_t full_index_index = combination_index(full_index>>1, node_nums-1, node_nums-1,comb_table);
    for (uint8_t node_index = 1; node_index < node_nums; node_index++)
    {
        total_subproblems++; // 最后查找最优解也计入
        if (dp_prev[full_index_index][node_index] + adj[0][node_index] < best_length)
        {
            best_length = dp_prev[full_index_index][node_index] + adj[0][node_index];
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
        uint8_t next = next_node[mask/2][current_node];
        if (next == 255) {
            std::__throw_runtime_error("Error: invalid next_node (255) during path reconstruction.");
        }
        mask ^= (1u << current_node); // 注销当前结点
        current_node = next;
        best_path.push_back(current_node);
    }

    return {best_path, best_length, total_subproblems, unique_subproblems};

}
