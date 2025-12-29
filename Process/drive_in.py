import numpy
import scipy.special as sc


def Guassian(x, t, D, Q):
    return Q / numpy.sqrt(4 * numpy.pi * D * t) * numpy.exp(-x**2 / (4 * D * t))

# 恒定表面浓度扩散
def erfc(x, t, D, Cs):
    # 使用scipy的erfc函数
    return Cs * sc.erfc(x / (2 * numpy.sqrt(D * t)))

if __name__ == "__main__":
    mode = int(input("请选择模式（1-恒定表面浓度扩散；2-高斯扩散）："))
    if mode == 1:
        D = float(input("请输入扩散系数(cm²/s)："))
        Cs = float(input("请输入表面浓度(atoms/cm³)："))
        t = float(input("请输入扩散时间(s)："))
        x = float(input("请输入深度(μm)："))
        x_cm = x * 1e-4  # 转换为cm
        concentration = erfc(x_cm, t, D, Cs)
        print(f"当t = {t} 秒，深度 x = {x} 微米时，掺杂浓度为: {concentration:.3e} atoms/cm³")
    else:
        D = float(input("请输入扩散系数(cm²/s)："))
        Q = float(input("请输入注入剂量(atoms/cm²)："))
        t = float(input("请输入扩散时间(s)："))
        x = float(input("请输入深度(μm)："))
        x_cm = x * 1e-4  # 转换为cm
        concentration = Guassian(x_cm, t, D, Q)
        print(f"当t = {t} 秒，深度 x = {x} 微米时，掺杂浓度为: {concentration:.3e} atoms/cm³")

