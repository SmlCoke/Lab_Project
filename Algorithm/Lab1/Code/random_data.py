import numpy as np
import argparse
import os

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Generate random numbers')
    parser.add_argument("nums", type = int, help = "Counts of random numbers")
    parser.add_argument("ratio", type = float, help = "The max number over number counts")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_log = os.path.join(script_dir, f"{str(args.nums)}.log")

    # 随机正整数数量
    counts = args.nums

    # 最大正整数值
    max_num = int(args.ratio*args.nums)
    
    numbers = np.random.randint(1, max_num + 1, size = counts)

    # 确保日志目录存在
    os.makedirs(os.path.dirname(output_log), exist_ok=True)

    # 写入文件
    np.savetxt(output_log, numbers, fmt="%d", encoding="utf-8")
        