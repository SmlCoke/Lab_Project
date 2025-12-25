import os
import re
import subprocess
from pathlib import Path

def main():
    root = Path(__file__).parent  # 当前脚本所在目录
    pattern_dir = re.compile(r'^pattern\d$') 
    pattern_file = re.compile(r'^adder\d_power_tb.sp$')  # 匹配特定 sp 文件

    # 递归遍历所有子目录
    for subdir in root.rglob('*'):
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
