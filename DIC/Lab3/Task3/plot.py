import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 1. 设置字体
T_16 = FontProperties(fname=r'C:\\Windows\\Fonts\\times.ttf', size=16)
T_14 = FontProperties(fname=r'C:\\Windows\\Fonts\\times.ttf', size=14)
T_12 = FontProperties(fname=r'C:\\Windows\\Fonts\\times.ttf', size=12)

# 2. 准备数据
# Critical Path 1
m_h1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
tp_h1 = [93.52, 73.76, 70.42, 68.97, 69.98, 78.50, 80.79, 81.77, 84.21]

# Critical Path 1 (Pro)
m_h1_pro = [1, 2, 3, 4, 5, 6, 7, 8]
tp_h1_pro = [152.10, 85.64, 74.25, 65.17, 65.65, 66.69, 71.29, 72.84]

# Critical Path 2
m_h2 = [2, 3, 4, 5, 6, 7, 8]
tp_h2 = [52.52, 49.63, 50.27, 49.08, 51.17, 52.20, 53.64]

# 3. 绘图 - 创建 1 行 2 列的子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# --- 左子图：Critical Path 1 & Pro ---
ax1.plot(m_h1, tp_h1, marker='o', linestyle='-', label='Critical Path 1', color='tab:blue')
ax1.plot(m_h1_pro, tp_h1_pro, marker='s', linestyle='--', label='Critical Path 1 (Pro)', color='tab:orange')

ax1.set_xlabel('Number of Inverter Stages ($m$)', fontproperties=T_14)
ax1.set_ylabel('Propagation Delay $t_p$ (ps)', fontproperties=T_14)
ax1.set_xticks(range(1, 11))
ax1.legend(prop=T_12)
ax1.grid(True, linestyle=':', alpha=0.6)

# 设置左子图刻度字体
for label in ax1.get_xticklabels() + ax1.get_yticklabels():
    label.set_fontproperties(T_12)

# --- 右子图：Critical Path 2 ---
ax2.plot(m_h2, tp_h2, marker='^', linestyle='-.', label='Critical Path 2', color='tab:green')

ax2.set_xlabel('Number of Inverter Stages ($m$)', fontproperties=T_14)
ax2.set_ylabel('Propagation Delay $t_p$ (ps)', fontproperties=T_14)
ax2.set_xticks(range(1, 11))
ax2.legend(prop=T_12)
ax2.grid(True, linestyle=':', alpha=0.6)

# 设置右子图刻度字体
for label in ax2.get_xticklabels() + ax2.get_yticklabels():
    label.set_fontproperties(T_12)

# 4. 保存为PDF
plt.tight_layout()
plt.savefig('tp_vs_m_comparison_subplots.pdf', format='pdf')
