import matplotlib.pyplot as plt

# 四种算法总耗时(改良暴力搜索, 排序加扫描, 分治, 哈希)，数据量分别为100, 1000, 10000, 100000, 1000000(列表从左到右)
# 数据集规模:
scales = [100,1000,10000,100000,1000000]
# 时间单位: ms
time_brute = [0.0253, 0.5669, 49.0998, 4229.89, 401570]
time_merge = [0.0191, 0.2077, 2.7056, 33.5174, 388.76]
time_dc =    [0.1649, 1.0363, 17.2027, 138.263, 1584.6]
time_hash =  [0.0032, 0.0078, 0.0563, 0.3033, 3.1352]

plt.figure()
plt.plot(scales, time_brute, color = "red", label = "Brute Force Search Pro", marker = "s")
plt.plot(scales, time_merge, color = "deepskyblue", label = "Sort and Scan", marker = "v")
plt.plot(scales, time_dc, color = "black", label = "Divide and Conquer", marker = "^")
plt.plot(scales, time_hash, color = "green", label = "Hash", marker = "o")

# plt.xscale('log')
# plt.yscale('log')

# --- 为了报告美观，增加标题、坐标轴标签和图例 ---
plt.title('Algorithm Performance Comparison (Log-Log Scale)')
plt.xlabel('Input Scale (Number of Integers)')
plt.ylabel('Execution Time (ms)')
plt.grid(True, which="both", ls="--") # 增加网格线，更易读
plt.legend() # 显示图例
plt.tight_layout()  # 布局紧凑
plt.savefig("Time_Scale_Linear.pdf", bbox_inches='tight')
# 显示图像
plt.show()
