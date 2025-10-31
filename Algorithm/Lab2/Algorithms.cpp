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
    std::unordered_map<state, uint8_t, statehash> child; // 记录当前状态的最优后继结点
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
                uint8_t best_node_j = 0; // 当前状态的最优后继结点

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
                            best_node_j = node_j;
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

    // 根据child map回溯最优路径
    // std::vector<uint8_t> best_path;
    // uint8_t current_node = best_first_node_index;
    // uint32_t current_mask = full_index;
    // while (current_mask > 0)
    // {
    //     best_path.push_back(current_node);
    //     current_node = child[{current_mask, current_node}];
    //     current_mask = current_mask ^ (1 << current_node); // 将结点current_node注销
    // }

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

    // 根据child map回溯最优路径
    std::vector<uint8_t> best_path;
    best_path.push_back(0);
    uint8_t current_node = best_first_node_index;
    uint32_t current_mask = full_index;

    while (current_mask > 0)
    {
        best_path.push_back(current_node);
        current_node = next_node[current_mask][current_node];
        current_mask ^= (1 << current_node); // 将结点current_node注销

    }

    return {best_path, best_length};

}

std::tuple<std::vector<uint8_t>, uint16_t> solve_TSP_with_dp_with_path(const std::vector<std::vector<uint16_t>> &adj, bool verbose)
{
    uint8_t node_nums = adj.size();
    uint32_t mask_nums = 1u << node_nums;
    const uint16_t INF = std::numeric_limits<uint16_t>::max() / 2;

    // dp[mask][i] = 从当前在i结点，访问mask中所有结点再回到0的最短路径长度
    std::vector<std::vector<uint16_t>> dp(mask_nums, std::vector<uint16_t>(node_nums, INF));
    // next_node[mask][i] = 从(i, mask)状态出发的最优下一节点
    std::vector<std::vector<uint8_t>> next_node(mask_nums, std::vector<uint8_t>(node_nums, 255));

    // 初始状态：从0出发，mask={0}
    dp[1][0] = 0;

    // 按集合大小递增遍历
    for (uint8_t node_num = 2; node_num <= node_nums; ++node_num)
    {
        for (uint32_t mask = 1; mask < mask_nums; mask += 2)
        {
            if (std::popcount(mask) != node_num) continue;

            for (uint8_t curr = 1; curr < node_nums; ++curr)
            {
                if (!(mask & (1 << curr))) continue; // 当前结点不在mask中

                uint32_t prev_mask = mask ^ (1 << curr); // 去掉当前结点
                uint16_t best_len = INF;
                uint8_t best_next = 255;

                // 枚举下一个结点
                for (uint8_t nxt = 0; nxt < node_nums; ++nxt)
                {
                    if (nxt == curr) continue;  // 删除不可能情况
                    if (nxt == 0 && node_num != 2) continue; // 避免提前回0
                    if (!(prev_mask & (1 << nxt))) continue; // 结点不在待访问结点集合中

                    uint16_t cand = dp[prev_mask][nxt] + adj[curr][nxt];
                    if (cand < best_len)
                    {
                        best_len = cand;
                        best_next = nxt;
                    }
                }

                if (best_len < INF)
                {
                    dp[mask][curr] = best_len;
                    next_node[mask][curr] = best_next;
                }
            }
        }
    }

    // 计算最终回到0的最短路径
    uint16_t best_length = INF;
    uint8_t best_first_node = 255;
    uint32_t full_mask = (1u << node_nums) - 1;

    for (uint8_t last = 1; last < node_nums; ++last)
    {
        uint16_t cand = dp[full_mask][last] + adj[0][last];
        if (cand < best_length)
        {
            best_length = cand;
            best_first_node = last;
        }
    }

    // 回溯最优路径
    std::vector<uint8_t> best_path;
    best_path.reserve(node_nums + 1);
    best_path.push_back(0); // 起点

    uint8_t curr = best_first_node;
    uint32_t mask = full_mask;
    best_path.push_back(curr);

    while (mask != 1) // mask==1 说明只剩0
    {
        uint8_t nxt = next_node[mask][curr];
        mask ^= (1 << curr);
        curr = nxt;
        best_path.push_back(curr);
    }



    return {best_path, best_length};
}
