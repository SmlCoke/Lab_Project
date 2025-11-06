#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

// 使用动态规划求解最长公共子串
std::string longestCommonSubstringDP(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    
    // dp[i][j] 表示以 X[i-1] 和 Y[j-1] 结尾的最长公共子串的长度
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));
    
    int maxLength = 0;  // 最长公共子串的长度
    int endIndex = 0;   // 最长公共子串在 X 中的结束位置
    
    // 填充 DP 表
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (X[i-1] == Y[j-1]) {
                // 如果字符相同，长度在前一个状态基础上加1
                dp[i][j] = dp[i-1][j-1] + 1;
                
                // 更新最长公共子串的信息
                if (dp[i][j] > maxLength) {
                    maxLength = dp[i][j];
                    endIndex = i - 1;  // 记录结束位置
                }
            } else {
                // 如果字符不同，长度为0（因为子串必须连续）
                dp[i][j] = 0;
            }
        }
    }
    
    // 提取最长公共子串
    if (maxLength == 0) {
        return "";
    }
    
    return X.substr(endIndex - maxLength + 1, maxLength);
}

// 空间优化版本：只使用一维数组
std::string longestCommonSubstringDPOptimized(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    
    // 只需要保存上一行的结果
    std::vector<int> dp(m + 1, 0);
    
    int maxLength = 0;
    int endIndex = 0;
    
    for (int i = 1; i <= n; i++) {
        // 从后往前更新，避免覆盖还需要使用的值
        int prev = 0;  // 保存 dp[j-1] 的值（即 dp[i-1][j-1]）
        for (int j = 1; j <= m; j++) {
            int temp = dp[j];  // 保存当前值，供下一次迭代使用
            
            if (X[i-1] == Y[j-1]) {
                dp[j] = prev + 1;
                
                if (dp[j] > maxLength) {
                    maxLength = dp[j];
                    endIndex = i - 1;
                }
            } else {
                dp[j] = 0;
            }
            
            prev = temp;  // 更新 prev 为下一次迭代准备
        }
    }
    
    if (maxLength == 0) {
        return "";
    }
    
    return X.substr(endIndex - maxLength + 1, maxLength);
}

int main() {
    // 测试用例1：作业中的示例
    std::string X1 = "photograph";
    std::string Y1 = "tomography";
    std::cout << "X = \"" << X1 << "\"" << std::endl;
    std::cout << "Y = \"" << Y1 << "\"" << std::endl;
    std::string result1 = longestCommonSubstringDP(X1, Y1);
    std::cout << "最长公共子串: \"" << result1 << "\"" << std::endl;
    std::cout << "长度: " << result1.length() << std::endl << std::endl;
    
    // 测试用例2：另一个例子
    std::string X2 = "abcdefgh";
    std::string Y2 = "xyzdefpqr";
    std::cout << "X = \"" << X2 << "\"" << std::endl;
    std::cout << "Y = \"" << Y2 << "\"" << std::endl;
    std::string result2 = longestCommonSubstringDP(X2, Y2);
    std::cout << "最长公共子串: \"" << result2 << "\"" << std::endl;
    std::cout << "长度: " << result2.length() << std::endl << std::endl;
    
    // 测试用例3：使用优化版本
    std::string X3 = "ABABC";
    std::string Y3 = "BABCA";
    std::cout << "X = \"" << X3 << "\" (优化版本)" << std::endl;
    std::cout << "Y = \"" << Y3 << "\"" << std::endl;
    std::string result3 = longestCommonSubstringDPOptimized(X3, Y3);
    std::cout << "最长公共子串: \"" << result3 << "\"" << std::endl;
    std::cout << "长度: " << result3.length() << std::endl;
    
    return 0;
}
