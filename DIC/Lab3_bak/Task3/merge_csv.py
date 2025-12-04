import pandas as pd
import argparse
import os
import re
if __name__ == "__main__":
    # 读取指定文件夹下的m=\d+文件夹中的task2_m\d+.csv文件（只有一行数据），并且混合成一个df，混合时注明这一行的对应哪一个文件夹m=\d+
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="指定文件夹路径")
    args = parser.parse_args()

    folder_path = args.folder
    csv_files = []
    ms = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if re.match(r"task3_H1_pro_m\d+\.csv", file):
                csv_files.append(os.path.join(root, file))
                match = re.search(r"task3_H1_pro_m(\d+)\.csv", str(file))
                ms.append(match.group(1) if match else None)

    # 读取所有csv文件，并将它们合并成一个DataFrame
    df_list = []
    for index, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        df['m'] = ms[index]
        df_list.append(df)

    merged_df = pd.concat(df_list, ignore_index=True)
    print(merged_df)
    merged_df.to_csv(os.path.join(folder_path, "merged_H1_pro.csv"), index=False)
