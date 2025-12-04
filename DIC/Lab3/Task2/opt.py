import numpy as np
from scipy.optimize import fsolve

def f(N):
    return N*2304**(1/N) + N + 2

def f_prime(N):
    # 原函数: N*2304**(1/N) + N + 2
    # 求导后: 2304**(1/N) - 2304**(1/N)*np.log(2304)/N + 1
    return (1-np.log(2304)/N)*2304**(1/N) + 1

if __name__ == "__main__":
    root = fsolve(f_prime, x0=6)
    print(f"optimal_N = {root}")
    print(f"f_prime = {f_prime(root)}")
    print(f"D_min = {f(root)}")
    print(f"hopt = {2304**(1/root)}")

    for m in range(0, 20):
        N = m+3
        print(f"m = {m}, N = {N}, D = {f(N)}, hopt = {2304**(1/N)}")
