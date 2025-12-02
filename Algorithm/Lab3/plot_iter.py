import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
from matplotlib.font_manager import FontProperties
T_16 = FontProperties(fname= r'C:\\Windows\\Fonts\\times.ttf', size = 16)    # Times New Roman
T_14 = FontProperties(fname= r'C:\\Windows\\Fonts\\times.ttf', size = 14)    # Times New Roman
T_12 = FontProperties(fname= r'C:\\Windows\\Fonts\\times.ttf', size = 12)    # Times New Roman

def plot_sa_curve(csv_file, x_mode='log'):
    if not os.path.exists(csv_file):
        print(f"错误: 文件 '{csv_file}' 不存在。")
        return

    print(f"正在读取数据: {csv_file} ...")
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"读取 CSV 失败: {e}")
        return

    # 计算历史最佳分数曲线，该曲线必定连续，能够很直白的看出算法优化效果
    df['BestScore'] = df['CurrentScore'].cummax()

    plt.figure(figsize=(10, 6))

    # 1. 绘制当前分数 (使用散点图，更能体现高温下的随机性)
    # plt.scatter(df['Temp'], df['CurrentScore'], s=10, c='blue', alpha=0.15, label='Current Score')
    # 如果绘制处所有数据点，则svg文件也会很大，所以直接放弃散点图

    # 2. 绘制历史最佳分数 (使用连线，体现收敛趋势)
    plt.plot(df['Temp'], df['BestScore'], color='red', linewidth=2, label='Best Score')

    # 设置坐标轴
    plt.xlabel('Temperature (Log Scale)', fontproperties=T_14)
    plt.ylabel('Score', fontproperties=T_14)
    # plt.title(f'Simulated Annealing: Score vs Temperature\n{csv_file}', fontproperties=T_16)

    # 设置 X 轴为对数坐标 (因为退火温度通常是指数下降的，线性坐标会导致低温段挤在一起)
    if x_mode == 'log':
        plt.xscale('log')

    # 反转 X 轴 (让高温在左边，低温在右边，符合时间推进的直觉)
    plt.gca().invert_xaxis()

    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(prop = T_14)
    plt.tight_layout()

    # 保存图片
    output_img = csv_file.replace('.csv', '.pdf')
    plt.savefig(output_img)
    print(f"图表已保存至: {output_img}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot SA Score vs Temperature")
    parser.add_argument("csv_file", help="Path to the CSV data file")
    parser.add_argument("x_mode",  help = "X轴模式: linear 或 log", choices=['linear', 'log'], default='log')
    args = parser.parse_args()

    plot_sa_curve(args.csv_file, args.x_mode)