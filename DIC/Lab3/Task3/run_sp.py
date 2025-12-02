import os
import re
import subprocess
from pathlib import Path
import argparse
def main():
    root = Path(__file__).parent  # 当前脚本所在目录
    parser = argparse.ArgumentParser(description="Run HSPICE simulations in subdirectories.")
    parser.add_argument("H_mode", type = int, help="Specify H1, H2, or H1_pro (1 or 2 or 3)")
    args = parser.parse_args()
    H_mode = args.H_mode
    if H_mode == 1:
        pattern_dir = re.compile(r'^H1_m\d+$')   # 匹配 H1_m6, H1_m7 等文件夹
        pattern_file = re.compile(r'^task3_H1_m\d+\.sp$')  # 匹配 task3_H1_m2.sp 等文件
    elif H_mode == 2:
        pattern_dir = re.compile(r'^H2_m\d+$')   # 匹配 H2_m6, H2_m7 等文件夹
        pattern_file = re.compile(r'^task3_H2_m\d+\.sp$')  # 匹配 task3_H2_m2.sp 等文件
    elif H_mode == 3:
        pattern_dir = re.compile(r'^H1_pro_m\d+$')   # 匹配 H1_pro_m6, H1_pro_m7 等文件夹
        pattern_file = re.compile(r'^task3_H1_pro_m\d+\.sp$')  # 匹配 task3_H1_pro_m2.sp 等文件

    # 遍历所有子目录
    for subdir in root.iterdir():
        if subdir.is_dir() and pattern_dir.match(subdir.name):
            # 在该目录下查找 .sp 文件
            for file in subdir.iterdir():
                if pattern_file.match(file.name):
                    lis_file = file.with_suffix('.lis')
                    cmd = f"hspice {file.name} > {lis_file.name}"

                    print(f"工作目录: {subdir}")
                    print(f"正在执行: {cmd}")

                    # 在该目录下执行 hspice 命令
                    result = subprocess.run(cmd, shell=True, cwd=subdir)

                    print(result)

if __name__ == "__main__":
    main()
