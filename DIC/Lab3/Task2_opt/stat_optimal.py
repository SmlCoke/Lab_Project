import pandas as pd

if __name__ == "__main__":
    # 读取csv文件，找到tp列最小的那一行对应的所有值
    df = pd.read_csv("task2_opt.csv")
    min_tp_row = df.loc[df['tp'].idxmin()]
    print("Optimal parameters:")
    print(min_tp_row)