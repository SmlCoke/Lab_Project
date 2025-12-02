import subprocess
import os
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run plot_iter.py with specified CSV file and x_mode")
    parser.add_argument("root_dir", help="Path to the root directory")
    args = parser.parse_args()
    root_dir = args.root_dir
    pattern = re.compile("^(.*).csv$")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            match = pattern.match(file)
            if not match:
                continue
            csv_name = match.group(1)
            csv_path = os.path.join(root, file)
            x_mode = 'log'  # 默认使用对数坐标
            subprocess.run(['python', 'plot_iter.py', csv_path, x_mode])

    

    