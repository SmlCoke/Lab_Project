# Lab4 Task1 Delay Measurement Automation

本目录包含了用于自动化全加器（Full Adder）延迟测量的Python脚本。

## 文件说明

- `generate_sp.py`: 生成不同输入模式的HSPICE测试脚本
- `run_sp.py`: 批量运行HSPICE仿真
- `parse_delay.py`: 解析仿真结果并生成统计报告
- `subckt.sp`: 全加器子电路定义（在Lab4根目录）

## 使用流程

### 1. 生成HSPICE测试脚本

```bash
# 生成FA16和FA28的所有延迟测试脚本
python3 generate_sp.py --fa-type both --output-dir .

# 只生成FA16的测试脚本
python3 generate_sp.py --fa-type FA16 --output-dir .

# 只生成FA28的测试脚本
python3 generate_sp.py --fa-type FA28 --output-dir .
```

生成的文件将保存在以下目录结构中：
```
Task1/
├── FA16/
│   └── delay/
│       ├── FA16_delay_A_to_Sum_B0_Cin0.sp
│       ├── FA16_delay_A_to_Sum_B0_Cin1.sp
│       └── ... (共24个测试文件)
└── FA28/
    └── delay/
        ├── FA28_delay_A_to_Sum_B0_Cin0.sp
        ├── FA28_delay_A_to_Sum_B0_Cin1.sp
        └── ... (共24个测试文件)
```

### 2. 运行HSPICE仿真

```bash
# 运行所有delay测试
python3 run_sp.py --base-dir .

# 只运行FA16的测试
python3 run_sp.py --base-dir . --fa-type FA16

# 只运行FA28的测试
python3 run_sp.py --base-dir . --fa-type FA28

# 预览将要运行的文件（不实际运行）
python3 run_sp.py --base-dir . --dry-run
```

注意：确保系统中已安装HSPICE并且`hspice`命令可用。

### 3. 解析结果并生成统计

```bash
# 解析所有延迟测试结果
python3 parse_delay.py . --output delay_summary

# 指定不同的输出文件名
python3 parse_delay.py . --output my_results
```

这将生成以下文件：
- `delay_summary.csv`: 详细的延迟测量数据（CSV格式）
- `delay_summary.xlsx`: 详细的延迟测量数据（Excel格式）
- `delay_summary_stats.txt`: 统计摘要（文本格式）

## 延迟测试模式说明

对于全加器的每个输入到输出的路径，脚本会测试所有可能的静态输入组合：

### 测试路径

1. **A -> Sum**: 测量A输入变化时Sum输出的延迟
   - 静态输入组合: B=0/1, Cin=0/1 (共4种)

2. **B -> Sum**: 测量B输入变化时Sum输出的延迟
   - 静态输入组合: A=0/1, Cin=0/1 (共4种)

3. **Cin -> Sum**: 测量Cin输入变化时Sum输出的延迟
   - 静态输入组合: A=0/1, B=0/1 (共4种)

4. **A -> Cout**: 测量A输入变化时Cout输出的延迟
   - 静态输入组合: B=0/1, Cin=0/1 (共4种)

5. **B -> Cout**: 测量B输入变化时Cout输出的延迟
   - 静态输入组合: A=0/1, Cin=0/1 (共4种)

6. **Cin -> Cout**: 测量Cin输入变化时Cout输出的延迟
   - 静态输入组合: A=0/1, B=0/1 (共4种)

总计：每种全加器设计（FA16/FA28）有 6路径 × 4组合 = 24个测试用例

### 延迟测量指标

每个测试用例测量以下三个指标：

- **tpLH**: 低到高传播延迟（输入上升沿到输出上升沿）
- **tpHL**: 高到低传播延迟（输入下降沿到输出下降沿）
- **tp**: 平均传播延迟 = (tpLH + tpHL) / 2

## 结果分析

运行`parse_delay.py`后，可以通过以下方式查看结果：

1. **详细数据**: 打开`delay_summary.xlsx`查看每个测试用例的完整数据
2. **统计摘要**: 查看`delay_summary_stats.txt`获取每条路径的最小、最大和平均延迟
3. **自定义分析**: 使用`delay_summary.csv`进行进一步的数据处理和可视化

## 示例输出

统计摘要示例：
```
Delay Measurement Statistics (in picoseconds)
======================================================================

FA16:
  Path                 Min          Max          Avg          Count   
  --------------------------------------------------------------------
  A_to_Cout              25.30        35.40        30.20          4
  A_to_Sum               28.50        42.10        35.80          4
  B_to_Cout              26.10        36.20        31.50          4
  B_to_Sum               29.20        43.50        36.90          4
  Cin_to_Cout            22.40        28.30        25.10          4
  Cin_to_Sum             30.10        38.60        34.20          4

FA28:
  Path                 Min          Max          Avg          Count   
  --------------------------------------------------------------------
  A_to_Cout              27.50        38.20        32.60          4
  A_to_Sum               32.40        46.80        39.50          4
  ...
```

## 参考资料

这些脚本的设计参考了以下Lab3中的脚本：
- `DIC/Lab3/parser_mt.py`: .mt文件解析方法
- `DIC/Lab3/Task2/generate_sp.py`: .sp脚本生成模板
- `DIC/Lab3/Task2/run_sp.py`: 批量运行HSPICE的方法

## 注意事项

1. 运行仿真前确保HSPICE已正确安装并配置
2. 仿真时间取决于测试用例数量和系统性能，请耐心等待
3. 如果某些仿真失败，可以查看对应的.lis文件了解错误信息
4. 生成的.tr0, .ic0, .st0等中间文件可以根据需要删除以节省空间
