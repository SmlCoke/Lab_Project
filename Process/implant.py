import numpy as np

# 离子注入的高斯分布模型
def Gaussian(x, Rp, deltaRp, Q):
    return (Q / (deltaRp * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - Rp) / deltaRp) ** 2), Q / (deltaRp * np.sqrt(2 * np.pi))


if __name__ == "__main__":
    Rp = float(input("请输入投影射程 Rp (nm)：")) * 1e-7  # 转换为cm
    deltaRp = float(input("请输入标准偏差 deltaRp (nm)：")) * 1e-7  # 转换为cm
    Q = float(input("请输入注入剂量 Q (atoms/cm²)："))
    x = float(input("请输入深度 x (nm)：")) * 1e-7  # 转换为cm

    concentration, peak_concentration = Gaussian(x, Rp, deltaRp, Q)
    print(f"在深度 x = {x*1e7:.2f} nm 处的掺杂浓度为: {concentration:.3e} atoms/cm³")
    print(f"峰值掺杂浓度为: {peak_concentration:.3e} atoms/cm³")

    # 绘制高斯分布曲线图，并且表明Rp, Rp±ΔRp的辅助线
    import matplotlib.pyplot as plt
    x_values = np.linspace(Rp - 4*deltaRp, Rp + 4*deltaRp, 1000)
    y_values, _ = Gaussian(x_values, Rp, deltaRp, Q)
    plt.plot(x_values * 1e7, y_values, label='Dopant Concentration Profile')
    plt.axvline(Rp * 1e7, color='r', linestyle='--', label='Rp')
    plt.axvline((Rp - deltaRp) * 1e7, color='g', linestyle='--', label='Rp - ΔRp')
    plt.axvline((Rp + deltaRp) * 1e7, color='g', linestyle='--', label='Rp + ΔRp')
    plt.xlabel('Depth (nm)')
    plt.ylabel('Concentration (atoms/cm³)')
    plt.title('Ion Implantation Dopant Profile')    
    plt.legend()
    plt.grid()
    plt.show()