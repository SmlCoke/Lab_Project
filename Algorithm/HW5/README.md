# Algorithm HW5 - 随机算法 (Randomized Algorithms)

## 作业内容

设计一个随机算法，用于恢复具有加法同态性质的函数 F 的正确值，其中函数的 1/5 值被恶意篡改。

### 函数性质

- F: {0,1,...,n-1} → {0,1,...,m-1}
- F((x+y) mod n) = (F(x) + F(y)) mod m 对所有 x, y 成立

### 要求

1. 算法对任意 z，以大于 1/2 的概率计算出正确的 F(z)
2. 分析算法运行 3 次时的返回策略和概率变化

## 解决方案

### 核心思想

利用函数的加法同态性质：对于任意 z，随机选择 x，计算 y = (z-x) mod n，则：
```
F(z) = F((x+y) mod n) = (F(x) + F(y)) mod m
```

由于只有 20% 的值被篡改，F(x) 和 F(y) 都正确的概率为 (4/5)² = 16/25 = 0.64 > 0.5

### 算法策略

1. **单次验证**: 随机选择 x，返回 (F[x] + F[y]) mod m
   - 正确概率: 64%

2. **多次投票**: 运行 k 次，返回出现最多的值（众数）
   - k=3 时正确概率: ~70%
   - k=5 时正确概率: ~91%
   - k=10 时正确概率: ~99%

## 文件说明

- `main.tex`: LaTeX 作业报告（包含问题分析、算法设计、伪代码和 C++ 实现）
- `random_function_check.cpp`: 基本实现和示例代码
- `test_algorithm.cpp`: 完整的测试程序，验证算法准确性
- `hw5.pdf`: 作业题目
- `Randomized Algorithms.pdf`: 随机算法讲义

## 编译和运行

### 编译 C++ 代码
```bash
g++ -o random_function_check random_function_check.cpp
./random_function_check
```

### 运行测试
```bash
g++ -o test_algorithm test_algorithm.cpp
./test_algorithm
```

### 编译 LaTeX 文档
```bash
xelatex main.tex
```

## 实验结果

测试 1000 次的实验结果：
- k=1: 准确率 61.6% (理论值 64%)
- k=3: 准确率 78.4% (理论值 ~70%)
- k=5: 准确率 91.1%
- k=10: 准确率 99.4%

结果表明算法有效地恢复了被篡改的函数值！
