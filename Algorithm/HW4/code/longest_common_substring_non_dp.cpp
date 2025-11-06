#include <iostream>
#include <string>
#include <algorithm>

// 非动态规划算法：对角线扫描法
// 时间复杂度：Θ(nm)
// 核心思想：在两个字符串形成的比较矩阵中，沿着所有可能的对角线进行扫描
// 每个字符恰好被访问一次，因此总时间复杂度为Θ(nm)
std::string longestCommonSubstringDiagonal(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    int maxLength = 0;
    int endIndexX = 0;
    
    // 阶段1：扫描从X的每个位置开始，Y从0开始的对角线
    // 这些对角线覆盖了矩阵的下三角部分
    for (int startX = 0; startX < n; startX++) {
        int length = 0;
        int i = startX;
        int j = 0;
        
        // 沿对角线方向扫描
        while (i < n && j < m) {
            if (X[i] == Y[j]) {
                length++;
                if (length > maxLength) {
                    maxLength = length;
                    endIndexX = i;
                }
            } else {
                length = 0;  // 子串必须连续，遇到不匹配就重置
            }
            i++;
            j++;
        }
    }
    
    // 阶段2：扫描从Y的每个位置开始（跳过0，因为已经在阶段1处理），X从0开始的对角线
    // 这些对角线覆盖了矩阵的上三角部分
    for (int startY = 1; startY < m; startY++) {
        int length = 0;
        int i = 0;
        int j = startY;
        
        // 沿对角线方向扫描
        while (i < n && j < m) {
            if (X[i] == Y[j]) {
                length++;
                if (length > maxLength) {
                    maxLength = length;
                    endIndexX = i;
                }
            } else {
                length = 0;  // 子串必须连续，遇到不匹配就重置
            }
            i++;
            j++;
        }
    }
    
    if (maxLength == 0) {
        return "";
    }
    
    return X.substr(endIndexX - maxLength + 1, maxLength);
}

int main() {
    // 测试用例1：作业中的示例
    std::string X1 = "photograph";
    std::string Y1 = "tomography";
    
    std::cout << "=== 测试用例 1 ===" << std::endl;
    std::cout << "X = \"" << X1 << "\"" << std::endl;
    std::cout << "Y = \"" << Y1 << "\"" << std::endl;
    
    std::string result1 = longestCommonSubstringDiagonal(X1, Y1);
    std::cout << "最长公共子串: \"" << result1 << "\"" << std::endl;
    std::cout << "长度: " << result1.length() << std::endl << std::endl;
    
    // 测试用例2
    std::string X2 = "ABABC";
    std::string Y2 = "BABCA";
    
    std::cout << "=== 测试用例 2 ===" << std::endl;
    std::cout << "X = \"" << X2 << "\"" << std::endl;
    std::cout << "Y = \"" << Y2 << "\"" << std::endl;
    
    std::string result2 = longestCommonSubstringDiagonal(X2, Y2);
    std::cout << "最长公共子串: \"" << result2 << "\"" << std::endl;
    std::cout << "长度: " << result2.length() << std::endl << std::endl;
    
    // 测试用例3：完全不同的字符串
    std::string X3 = "abc";
    std::string Y3 = "def";
    
    std::cout << "=== 测试用例 3 ===" << std::endl;
    std::cout << "X = \"" << X3 << "\"" << std::endl;
    std::cout << "Y = \"" << Y3 << "\"" << std::endl;
    
    std::string result3 = longestCommonSubstringDiagonal(X3, Y3);
    std::cout << "最长公共子串: \"" << result3 << "\"" << std::endl;
    std::cout << "长度: " << result3.length() << std::endl << std::endl;
    
    // 测试用例4：相同字符串
    std::string X4 = "ABCD";
    std::string Y4 = "ABCD";
    
    std::cout << "=== 测试用例 4 ===" << std::endl;
    std::cout << "X = \"" << X4 << "\"" << std::endl;
    std::cout << "Y = \"" << Y4 << "\"" << std::endl;
    
    std::string result4 = longestCommonSubstringDiagonal(X4, Y4);
    std::cout << "最长公共子串: \"" << result4 << "\"" << std::endl;
    std::cout << "长度: " << result4.length() << std::endl << std::endl;
    
    // 测试用例5：一个字符串是另一个的子串
    std::string X5 = "abcdefgh";
    std::string Y5 = "cdef";
    
    std::cout << "=== 测试用例 5 ===" << std::endl;
    std::cout << "X = \"" << X5 << "\"" << std::endl;
    std::cout << "Y = \"" << Y5 << "\"" << std::endl;
    
    std::string result5 = longestCommonSubstringDiagonal(X5, Y5);
    std::cout << "最长公共子串: \"" << result5 << "\"" << std::endl;
    std::cout << "长度: " << result5.length() << std::endl;
    
    return 0;
}
