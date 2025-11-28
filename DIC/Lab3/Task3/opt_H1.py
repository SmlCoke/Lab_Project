import numpy as np
import pandas as pd
from scipy.optimize import fsolve

def H1(q, m):
    return 8192/q**(m+1) + 128*2**(1/2)/(q**((m+1)/2)) + (m+1)*q

def H1_prime(q,m):
    return -8192*(m+1)/q**(m+2) - 64*(m+1)*2**(1/2)/(q**((m+3)/2)) + (m+1)

if __name__ == "__main__":
    for m in range(0, 20):
        print("-"*70)
        print(f"{'-'*30} When m = {m} {'-'*30}")
        print("-"*70)
        H1 = lambda q: 8192/q**(m+1) + 128*2**(1/2)/(q**((m+1)/2)) + (m+1)*q
        H1_prime = lambda q: -8192*(m+1)/q**(m+2) - 64*(m+1)*2**(1/2)/(q**((m+3)/2)) + (m+1)
        root = fsolve(H1_prime, x0=3)
        print(f"optimal_p = {root}")
        print(f"H1_prime = {H1_prime(root)}")
        print(f"H1_min = {H1(root)}")


    # df = pd.DataFrame(columns=["m", "q", "H1", "H1_prime"])
    # for m in range(10):
    #     print("-"*70)
    #     print(f"{'-'*30} When m = {m} {'-'*30}")
    #     print("-"*70)
    #     H1 = lambda q: 8192/q**(m+1) + 128*2**(1/2)/(q**((m+1)/2)) + (m+1)*q
    #     H1_prime = lambda q: -8192*(m+1)/q**(m+2) - 64*(m+1)*2**(1/2)/(q**((m+3)/2)) + (m+1)
    #     for q in range(1,20):
    #         print(f"H1({q}) = {H1(q)}")
    #         print(f"H1_prime({q}) = {H1_prime(q)}")
    #         df = df._append({"m": m, "q": q, "H1": H1(q), "H1_prime": H1_prime(q)}, ignore_index=True)
    # print(df)
    # df.to_csv("opt_H1.csv", index=False)
    # min_tp_row = df.loc[df['H1'].idxmin()]
    # print("Optimal parameters:")
    # print(min_tp_row)
