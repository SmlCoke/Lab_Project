import pandas as pd

if __name__ == "__main__":
    # 示例用法
    df_N4 = pd.read_excel('N=4/task5_op_N4.xlsx')
    df_N5 = pd.read_excel('N=5/task5_op_N5.xlsx')

    # 找出df_N4中tp_total最小的列对应的行
    min_tp_total_N4 = df_N4['tp_total'].min()
    min_tp_total_row_N4 = df_N4[df_N4['tp_total'] == min_tp_total_N4]

    # 找出df_N5中tp_total最小的列对应的行
    min_tp_total_N5 = df_N5['tp_total'].min()
    min_tp_total_row_N5 = df_N5[df_N5['tp_total'] == min_tp_total_N5]
    print("N=4时tp_total最小的行:")
    print(min_tp_total_row_N4)
    print("N=5时tp_total最小的行:")
    print(min_tp_total_row_N5)