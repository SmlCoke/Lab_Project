import numpy


def Guassian(x, t, D, Q):
    return Q / numpy.sqrt(4 * numpy.pi * D * t) * numpy.exp(-x**2 / (4 * D * t))
if __name__ == "__main__":
    D = float(input("请输入扩散系数(cm²/s)："))
    Q = float(input("请输入注入剂量(atoms/cm²)："))
    t = float(input("请输入扩散时间(s)："))
    x = float(input("请输入深度(μm)："))
    x_cm = x * 1e-4  # 转换为cm
    concentration = Guassian(x_cm, t, D, Q)
    print(f"当t = {t} 秒，深度 x = {x} 微米时，掺杂浓度为: {concentration:.3e} atoms/cm³")

