#include <iostream>
#include <vector>

// 判断集合是否可以被划分为两个和相等的子集
// 使用动态规划算法
bool subsetPartition(const std::vector<int>& S) {
    int n = S.size();
    int sum = 0;
    
    // 计算集合总和
    for (int i = 0; i < n; i++) {
        sum += S[i];
    }
    
    // 如果总和为奇数，无法划分
    if (sum % 2 != 0) {
        return false;
    }
    
    int target = sum / 2;
    
    // dp[i][j] 表示使用前 i 个元素能否凑出和为 j
    std::vector<std::vector<bool>> dp(n + 1, std::vector<bool>(target + 1, false));
    
    // 初始化：和为 0 总是可以达到（不选任何元素）
    for (int i = 0; i <= n; i++) {
        dp[i][0] = true;
    }
    
    // 动态规划填表
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= target; j++) {
            // 不选第 i 个元素
            dp[i][j] = dp[i-1][j];
            
            // 选第 i 个元素（如果可以）
            if (j >= S[i-1]) {
                dp[i][j] = dp[i][j] || dp[i-1][j - S[i-1]];
            }
        }
    }
    
    return dp[n][target];
}

// 空间优化版本：使用一维数组
bool subsetPartitionOptimized(const std::vector<int>& S) {
    int n = S.size();
    int sum = 0;
    
    for (int i = 0; i < n; i++) {
        sum += S[i];
    }
    
    if (sum % 2 != 0) {
        return false;
    }
    
    int target = sum / 2;
    std::vector<bool> dp(target + 1, false);
    dp[0] = true;
    
    // 逐个考虑每个元素
    for (int i = 0; i < n; i++) {
        // 从后往前更新，避免重复使用同一元素
        for (int j = target; j >= S[i]; j--) {
            dp[j] = dp[j] || dp[j - S[i]];
        }
    }
    
    return dp[target];
}

int main() {
    // 测试用例1：可以划分
    std::vector<int> S1 = {1, 5, 11, 5};
    std::cout << "测试集合 {1, 5, 11, 5}: ";
    if (subsetPartition(S1)) {
        std::cout << "可以划分为两个和相等的子集" << std::endl;
    } else {
        std::cout << "不能划分为两个和相等的子集" << std::endl;
    }
    
    // 测试用例2：不能划分
    std::vector<int> S2 = {1, 2, 3, 5};
    std::cout << "测试集合 {1, 2, 3, 5}: ";
    if (subsetPartition(S2)) {
        std::cout << "可以划分为两个和相等的子集" << std::endl;
    } else {
        std::cout << "不能划分为两个和相等的子集" << std::endl;
    }
    
    // 测试用例3：使用优化版本
    std::vector<int> S3 = {3, 1, 1, 2, 2, 1};
    std::cout << "测试集合 {3, 1, 1, 2, 2, 1} (优化版本): ";
    if (subsetPartitionOptimized(S3)) {
        std::cout << "可以划分为两个和相等的子集" << std::endl;
    } else {
        std::cout << "不能划分为两个和相等的子集" << std::endl;
    }
    
    return 0;
}
