import pandas as pd
import argparse 
import os
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find optimal parameters from CSV.")
    parser.add_argument("stat_dir", type=str, help="Path to the execute stat program.")
    args = parser.parse_args()

    pattern = re.compile("(.*)\.csv$")
    for root, dirs, files in os.walk(args.stat_dir):
        for filename in files:
            match = pattern.match(filename)
            if not match:
                continue
            csv_path = os.path.join(root, filename)
            csv_name = str(match.group(1)) # 索引从1开始

            result_name = f"{csv_name}_optimal.log"
            result_path = os.path.join(args.stat_dir, result_name)

            df = pd.read_csv(csv_path)
            min_tp_row = df.loc[df['tp'].idxmin()]

            with open(result_path, "w", encoding="utf-8") as f:
                f.write(min_tp_row.to_string())

            print(f"csv数据{csv_path}统计完成，结果保存至{result_path}")