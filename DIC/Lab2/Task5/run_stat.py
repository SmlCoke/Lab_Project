import pandas as pd
import argparse
import re
import os
from pathlib import Path

def parse_mt(filepath):
    """
    通用 HSPICE .mt0 文件解析函数
    - 自动识别多行表头
    - 自动跳过描述性头部
    - 自动合并多行标题
    - 自动识别列数并转换为 DataFrame
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.rstrip() for line in f if line.strip()]

    # .mt0文件通常分为两部分：头部描述和数据区
    # ---------- Step 1: 找到标题起始行 ----------
    title_idx = None
    for i, line in enumerate(lines):
        if line.startswith('.TITLE'):
            title_idx = i
            break
    if title_idx is None:
        raise ValueError(f"未找到 .TITLE 行: {filepath}")

    # ---------- Step 2: 提取数据区 ----------
    # 数据区通常分为标题行和数据行
    data_start = title_idx + 1
    data_lines = []
    for line in lines[data_start:]:
        if line.startswith('$') or line.startswith('.END'):
            break
        data_lines.append(line)

    # ---------- Step 3: 识别多行表头 ----------
    header_lines = []
    data_start_idx = 0
    for i, line in enumerate(data_lines):
        # 判断这一行是数字数据的开始（即表头结束）
        if re.match(r'^\s*[-\d]', line):  # 数字或负号开头
            # 如果是数字或者负号开头，代表表头部分识别完成，接下来的是数据区，不用再添加标题行
            data_start_idx = i
            break
        header_lines.append(line)

    # 合并多行表头为一行
    header_text = ' '.join(header_lines)
    headers = re.findall(r'[A-Za-z0-9_\#\+\-\(\)\/]+', header_text)
    # 表头中的指标可能包含的字符：字母、数字、下划线、#、+、-、()、/。其中数字不可能作为开头
    
    # ---------- Step 4: 提取数据 ----------
    data_part = data_lines[data_start_idx:]
    rows = []
    current_row = []
    for line in data_part:
        # 行中全是数值或科学计数法
        tokens = re.findall(r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?', line)
        # 匹配浮点数或者整数，包含科学计数法
        if not tokens:
            continue
        current_row.extend(tokens)
        # 判断一行是否完整：列数相等
        # .mt文件中的数据行大概率是分散的，但是不同行的数据不可能混合在一起，因此这种操作是合理的
        if len(current_row) >= len(headers):
            rows.append(current_row[:len(headers)])
            current_row = current_row[len(headers):]

    df = pd.DataFrame(rows, columns=headers)

    # ---------- Step 5: 转换数值类型 ----------
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except Exception:
            pass

    return df


def parse_mts(dir_path):
    """
    批量解析指定目录下的所有 .mt*文件，每处理一个，就调用 parse_mt 函数进行解析，生成对应名字的excel表格
    随后，将df每一列的数据进行归一化处理，生成对应名字的_excel_normalized.xlsx表格
    归一化公式： (x - min) / (max - min)
    """
    pattern = re.compile(r".*N(\d+)\.xlsx")
    rows = []
    header = ['N', 'tp_total']
    current_row = []
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            N_match = pattern.match(filename)
            if N_match:
                filepath = os.path.join(root, filename)
                print("匹配到文件:", filepath)
                N = N_match.group(1)
                df = pd.read_excel(filepath)
                tp_total = df['tp_total'].iloc[0]
                current_row = [N, tp_total]
                rows.append(current_row)
    summary_df = pd.DataFrame(rows, columns=header)
    summary_df.to_excel(os.path.join(dir_path, "summary.xlsx"), index=False)
    print("✅ 汇总表已导出: summary.xlsx")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Parse a HSPICE result file and display its contents.")
    # parser.add_argument("input_dir", type=str, help="Path to the input directory")
    # args = parser.parse_args()
    # parse_mts(args.input_dir)
    parse_mts("D:\\vscode\\Code\\HSpice\\DIC_exp\\Lab2\\Task5") 


