import pandas as pd

if __name__ == "__main__":
    df = pd.read_excel("task1.xlsx")
    idx = df['tp'].idxmin()
    s2 = df.loc[idx, "s2"]
    s3 = df.loc[idx, "s3"]
    s4 = df.loc[idx, "s4"]
    tp = df.loc[idx, "tp"]

    print(f"最小延时: {tp*1e12}ps")
    print("对应尺寸:")
    print(f"s2: {s2}")
    print(f"s3: {s3}")
    print(f"s4: {s4}")