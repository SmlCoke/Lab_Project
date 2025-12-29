import numpy as np

C1 = 7.72e2
C1_cm2s = C1*1e-8/3600  # in cm^2/s
C2 = 6.23e6
C2_cm2s = C2*1e-4/3600  # in cm/s
E1 = 1.23 # in eV
E2 = 2.0 # in eV
k = 8.62e-5 # in eV/K
if __name__ == "__main__":
    mode = int(input("请选择模式（1-给定氧化层厚度，计算所需时间；2-给定时间，计算氧化层厚度）："))
    if mode == 1:
        x = float(input("请输入欲氧化SiO2厚度（nm）："))
        x0 = float(input("请输入初始SiO2厚度（nm）："))
        T = float(input("请输入氧化温度（℃）：")) + 273.15  # 转换为K
        x_cm = x * 1e-7  # 转换为cm
        x0_cm = x0 * 1e-7  # 转换为cm
        B = C1_cm2s*np.exp(-E1/(k*T))
        B_A = C2_cm2s*np.exp(-E2/(k*T))
        A = B / B_A
        print(f"系数A = {A:.8e} cm, B = {B:.8e} cm²/s")
        tau = (x0_cm**2 + A*x0_cm)/B
        print(f"偏移量 tau 为：{tau:.8f} 秒")
        print(f"即氧化初始厚度的时间为：{tau/3600:.8f} 小时")
        t = (x_cm**2 + A*x_cm)/B  # in s
        t_hr = t / 3600  # 转换为小时
        print(f"总共需要氧化时间为：{t_hr:.8f} 小时，{t/60:.4f} 分钟")
        print(f"其中额外氧化时间为：{t_hr - tau/3600:.8f} 小时，{(t - tau)/60:.4f} 分钟")
    else:
        t_hr = float(input("请输入氧化时间（小时）："))
        t = t_hr * 3600  # 转换为秒
        x0 = float(input("请输入初始SiO2厚度（nm）："))
        T = float(input("请输入氧化温度（℃）：")) + 273.15  # 转换为K
        x0_cm = x0 * 1e-7  # 转换为cm
        B = C1_cm2s*np.exp(-E1/(k*T))
        B_A = C2_cm2s*np.exp(-E2/(k*T))
        A = B / B_A
        tau = (x0_cm**2 + A*x0_cm)/B
        print(f"偏移量 tau 为：{tau:.8f} 秒")
        print(f"即氧化初始厚度的时间为：{tau/3600:.8f} 小时，{tau/60:.4f} 分钟")
        x_cm = (-A + np.sqrt(A**2 + 4*B*(t+tau)))/2  # in cm
        x_nm = x_cm * 1e7  # 转换为nm
        print(f"氧化后的SiO2厚度为：{x_nm:.8f} nm")