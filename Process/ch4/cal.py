import numpy as np

def cal_t(T):
    return 3.57e-10/np.exp(-3.69/8.617e-5/(T+273.15))

if __name__ == "__main__":
    # Your main code here
    temperatures = [1000, 1100, 1200]
    results = [cal_t(T)/3600 for T in temperatures]
    print(results, 'h')
