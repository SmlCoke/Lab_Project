import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True         

if __name__ == '__main__':
    df = pd.read_excel('task4.xlsx')
    print(df)
    volts = df['supply'].values
    tp_total = (df['tp_total'] * 1e9).values   # ns
    power = np.abs((df['avgpower'] * 1e6).values)      # μW
    edp = (df['edp'] * 1e24).values             # μW·ns^2

    # 图1: tp_total - volts
    plt.figure(figsize=(4, 3))
    plt.scatter(volts, tp_total, s=15, color='black')  # 点大小减半
    plt.plot(volts, tp_total, color='black', linestyle='-')
    plt.xlabel(r'$V_{dd}/V$')
    plt.ylabel(r'$t_{p}/ns$')
    plt.grid(True, linestyle='--', alpha=0.3)
    # 调整布局
    plt.tight_layout()
    plt.savefig('tp_total_vs_volts.pdf')
    plt.close()

    # 图2: power - volts
    plt.figure(figsize=(4, 3))
    plt.plot(volts, power, color='black', linestyle='-')
    plt.scatter(volts, power, s=15, color='black')  # 点大小减半
    plt.xlabel(r'$V_{dd}/V$')
    plt.ylabel(r'$P/ \mu W$')
    plt.grid(True, linestyle='--', alpha=0.3)
    # 调整布局
    plt.tight_layout()
    plt.savefig('power_vs_volts.pdf')
    plt.close()

    # 图3: edp - volts
    plt.figure(figsize=(4, 3))
    plt.plot(volts, edp, color='black', linestyle='-')
    plt.scatter(volts, edp, s=15, color='black')  # 点大小减半
    plt.xlabel(r'$V_{dd}/V$')
    plt.ylabel(r'$edp/ \mu W\,ns^2$')
    plt.grid(True, linestyle='--', alpha=0.3)
    # 调整布局
    plt.tight_layout()
    plt.savefig('edp_vs_volts.pdf')
    plt.close()