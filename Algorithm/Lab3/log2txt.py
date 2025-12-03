import os
import pathlib
import argparse
def rename_log_to_txt(root_dir='.'):
    """
    递归查找 root_dir 下所有 .log 文件，并将其扩展名改为 .txt
    """
    root = pathlib.Path(root_dir).resolve()
    for log_file in root.rglob('data.log'):
        if log_file.is_file():
            new_name = log_file.with_suffix('.csv')
            # 避免覆盖已存在的 .txt 文件
            if new_name.exists():
                print(f"⚠️  跳过（目标已存在）: {log_file} → {new_name}")
                continue
            try:
                log_file.rename(new_name)
                print(f"✅ 重命名: {log_file} → {new_name}")
            except Exception as e:
                print(f"❌ 错误处理 {log_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="递归将 .log 文件重命名为 .txt 文件")
    parser.add_argument("root_dir")
    args = parser.parse_args()
    rename_log_to_txt(args.root_dir)