import subprocess
import os

if __name__ == "__main__":
    T0 = [10000, 20000]
    TT = [1]
    de = [5, 7, 88]
    times = [1000, 2000]

    for t0 in T0:
        for t in TT:
            for d in de:
                for time in times:
                    # 构造目录名
                    dir_name = f'{t0}_{t}_{d}_{time}'
                    result_dir = os.path.join('greedy_results', dir_name)
                    
                    # 如果目录不存在则创建
                    if not os.path.exists(result_dir):
                        os.makedirs(result_dir)
                    
                    print(f"Running flow for: {dir_name}")

                    # 1. 运行 eda.py
                    # 修正：使用 stdout=f_log 代替 '>'
                    process_log_path = os.path.join(result_dir, 'process.txt')
                    data_csv_path = os.path.join(result_dir, 'data.csv')
                    
                    with open(process_log_path, 'w', encoding='utf-8') as f_log:
                        subprocess.run(['python', 
                                        'eda.py', 
                                        'cells.spi',
                                        'AN2D2',
                                        data_csv_path,
                                        str(t0),
                                        f'0.{d}',
                                        str(time)],
                                        stdout=f_log) # 将标准输出重定向到文件
                    
                    # 2. 运行 evaluator.py
                    # 修正：使用 stdout=f_score 代替 '>'
                    score_log_path = os.path.join(result_dir, 'score.txt')
                    with open(score_log_path, 'w', encoding='utf-8') as f_score:
                        subprocess.run(['python', 
                                        'evaluator.py', 
                                        'AN2D2.json',
                                        'AN2D2',
                                        'cells.spi'],
                                        stdout=f_score)
                    
                    # 3. 运行 plot_iter.py
                    # 修正：文件名从 plot.py 改为 plot_iter.py
                    subprocess.run(['python', 
                                    'plot_iter.py', 
                                    data_csv_path,
                                    'log'])

