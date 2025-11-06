#include <iostream>
#include <string>
#include <algorithm>

// 方法1：后缀数组方法 - 使用字符串查找
// 这是一个简化版本，通过枚举所有可能的子串来实现
std::string longestCommonSubstringBruteForce(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    std::string result = "";
    int maxLength = 0;
    
    // 枚举 X 的所有子串
    for (int i = 0; i < n; i++) {
        for (int len = 1; len <= n - i; len++) {
            std::string substr = X.substr(i, len);
            
            // 检查这个子串是否在 Y 中出现
            if (Y.find(substr) != std::string::npos) {
                if (len > maxLength) {
                    maxLength = len;
                    result = substr;
                }
            } else {
                // 如果当前长度的子串不在 Y 中，更长的也不会在
                break;
            }
        }
    }
    
    return result;
}

// 方法2：优化的滑动窗口方法
// 对每个 X 中的起始位置和 Y 中的起始位置进行比较
std::string longestCommonSubstringSliding(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    int maxLength = 0;
    int endIndexX = 0;
    
    // 对于 X 的每个起始位置
    for (int i = 0; i < n; i++) {
        // 对于 Y 的每个起始位置
        for (int j = 0; j < m; j++) {
            int length = 0;
            int x = i, y = j;
            
            // 从当前位置开始，尽可能匹配更长的子串
            while (x < n && y < m && X[x] == Y[y]) {
                length++;
                x++;
                y++;
            }
            
            // 更新最长公共子串
            if (length > maxLength) {
                maxLength = length;
                endIndexX = i + length - 1;
            }
        }
    }
    
    if (maxLength == 0) {
        return "";
    }
    
    return X.substr(endIndexX - maxLength + 1, maxLength);
}

// 方法3：基于哈希的方法 - 使用滚动哈希
// 这个方法通过二分查找长度，然后用哈希判断是否存在该长度的公共子串
#include <unordered_set>

bool hasCommonSubstringOfLength(const std::string& X, const std::string& Y, int len, std::string& result) {
    std::unordered_set<std::string> substringsX;
    
    // 收集 X 中所有长度为 len 的子串
    for (int i = 0; i <= (int)X.length() - len; i++) {
        substringsX.insert(X.substr(i, len));
    }
    
    // 检查 Y 中是否有匹配的子串
    for (int i = 0; i <= (int)Y.length() - len; i++) {
        std::string substr = Y.substr(i, len);
        if (substringsX.find(substr) != substringsX.end()) {
            result = substr;
            return true;
        }
    }
    
    return false;
}

std::string longestCommonSubstringBinarySearch(const std::string& X, const std::string& Y) {
    int n = X.length();
    int m = Y.length();
    int left = 0, right = std::min(n, m);
    std::string result = "";
    
    // 二分查找最长公共子串的长度
    while (left <= right) {
        int mid = (left + right) / 2;
        std::string tempResult;
        
        if (hasCommonSubstringOfLength(X, Y, mid, tempResult)) {
            result = tempResult;
            left = mid + 1;  // 尝试找更长的
        } else {
            right = mid - 1;  // 长度太长，减小
        }
    }
    
    return result;
}

int main() {
    // 测试用例1：作业中的示例
    std::string X1 = "photograph";
    std::string Y1 = "tomography";
    
    std::cout << "X = \"" << X1 << "\"" << std::endl;
    std::cout << "Y = \"" << Y1 << "\"" << std::endl << std::endl;
    
    std::cout << "方法1 - 暴力枚举法:" << std::endl;
    std::string result1 = longestCommonSubstringBruteForce(X1, Y1);
    std::cout << "最长公共子串: \"" << result1 << "\"" << std::endl;
    std::cout << "长度: " << result1.length() << std::endl << std::endl;
    
    std::cout << "方法2 - 滑动窗口法:" << std::endl;
    std::string result2 = longestCommonSubstringSliding(X1, Y1);
    std::cout << "最长公共子串: \"" << result2 << "\"" << std::endl;
    std::cout << "长度: " << result2.length() << std::endl << std::endl;
    
    std::cout << "方法3 - 二分查找+哈希法:" << std::endl;
    std::string result3 = longestCommonSubstringBinarySearch(X1, Y1);
    std::cout << "最长公共子串: \"" << result3 << "\"" << std::endl;
    std::cout << "长度: " << result3.length() << std::endl << std::endl;
    
    // 测试用例2
    std::string X2 = "ABABC";
    std::string Y2 = "BABCA";
    std::cout << "X = \"" << X2 << "\"" << std::endl;
    std::cout << "Y = \"" << Y2 << "\"" << std::endl;
    std::cout << "滑动窗口法结果: \"" << longestCommonSubstringSliding(X2, Y2) << "\"" << std::endl;
    
    return 0;
}
