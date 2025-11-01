import os
import re
import argparse

if __name__ == "__main__":
    

    argparser = argparse.ArgumentParser()
    argparser.add_argument("dir_path", type=str, help="Directory path")
    args = argparser.parse_args()
    dir_path = args.dir_path

    safe = [".png", ".jpg", ".md", ".tex", ".pdf",
            ".sp", ".py", ".cpp", ".h", ".txt", ".log", ".svg"]

    for root, dirs, files in os.walk(dir_path):
            for filename in files:
                if not any(re.search(s, filename) for s in safe):
                    file_path = os.path.join(root, filename)
                    os.remove(file_path)
                    print(f"Deleted temp files: {file_path}")