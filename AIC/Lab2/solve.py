def cal_I(k_, beta, VGS, VTH):
    return 1/2 * k_ * beta * ((VGS - VTH) ** 2)

def cal_k(beta, VGS, VTH, I):
    return 2 * I / (beta * (VGS - VTH) ** 2)

def I_mirror(k_, beta, Rs, K):
    return 2/k_/beta*(1/Rs)**2*(1/K**0.5-1)**2

if __name__ == "__main__":
    beta = 5
    VGS = -507.241e-3
    VTH = -456.654e-3
    K = 8
    I = 9.836e-6
    k_ = cal_k(beta, VGS, VTH, I)/8
    print(f"kp' = {k_}")

    print(f'i_3 = {cal_I(k_, beta, VGS, VTH)*1e6*8}uA')

    print(f'i_4 = {cal_I(k_, beta, -664.611e-3, -456.524e-3)*1e6}uA')

    print(f"I_mirror = {I_mirror(k_, beta, 16e3, 8)*1e6} uA")