# Algorithm HW4 代码实现

本目录包含算法作业4的C++代码实现。

## 文件说明

### 题目1：集合划分问题
- **subset_partition.cpp**: 使用动态规划求解集合划分问题

### 题目2：最长公共子串问题
- **longest_common_substring_dp.cpp**: 使用动态规划算法求解最长公共子串
- **longest_common_substring_non_dp.cpp**: 使用非动态规划算法（对角线扫描法）求解最长公共子串

## 编译和运行

所有程序使用C++11标准编译，需要支持STL标准库。

### 编译方式

```bash
# 编译集合划分问题
g++ -std=c++11 -o subset_partition subset_partition.cpp

# 编译最长公共子串（动态规划）
g++ -std=c++11 -o lcs_dp longest_common_substring_dp.cpp

# 编译最长公共子串（非动态规划）
g++ -std=c++11 -o lcs_non_dp longest_common_substring_non_dp.cpp
```

### 运行方式

```bash
# 运行集合划分问题测试
./subset_partition

# 运行最长公共子串（动态规划）测试
./lcs_dp

# 运行最长公共子串（非动态规划）测试
./lcs_non_dp
```

## 代码特点

1. **严格遵循要求**：所有STL容器和算法都使用`std::`前缀，没有使用`using namespace std;`
2. **完整测试用例**：每个程序都包含多个测试用例，验证算法正确性
3. **详细注释**：代码中包含中文注释，便于理解算法思路
4. **优化实现**：部分算法提供了空间优化版本（如滚动数组）

## 算法复杂度

### 题目1：集合划分问题
- 时间复杂度：O(n × sum)，其中n为集合大小，sum为元素总和
- 空间复杂度：O(n × sum)，可优化为O(sum)

### 题目2：最长公共子串问题

#### 动态规划算法
- 时间复杂度：Θ(nm)，其中n和m分别为两个字符串的长度
- 空间复杂度：O(nm)，可优化为O(m)

#### 非动态规划算法（对角线扫描法）
- 时间复杂度：Θ(nm)
- 空间复杂度：O(1)
