import argparse
from collections import Counter

def verify_modes_from_log(filepath, top_k=10):
    # 1. 读取文件
    with open(filepath, 'r') as f:
        numbers = [int(line.strip()) for line in f if line.strip()]

    # 2. 统计频率
    counter = Counter(numbers)

    # 3. 找出最大出现次数
    max_count = max(counter.values())

    # 4. 找出所有众数
    modes = [num for num, count in counter.items() if count == max_count]

    print(f"文件: {filepath}")
    print(f"共 {len(numbers)} 个数字，唯一值数量: {len(counter)}")
    print(f"出现次数最多的值（众数）有 {len(modes)} 个：")
    print(f"众数: {modes}")
    print(f"出现次数: {max_count}")

    # 5. 输出出现次数排名前 top_k 的值（辅助验证）
    print(f"\n出现次数排名前 {top_k} 的值:")
    for num, count in counter.most_common(top_k):
        print(f"  {num}: {count}")

if __name__ == "__main__":
    # 这里改成你的文件路径
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type = str, help = "请输入log文件路径")
    args = parser.parse_args()
    filename = args.file_path
    verify_modes_from_log(filename)
