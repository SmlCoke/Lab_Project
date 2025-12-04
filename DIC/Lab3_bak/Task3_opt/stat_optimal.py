import pandas as pd

if __name__ == "__main__":
    # 读取csv文件，找到tp列最小的那一行对应的所有值
    df = pd.read_csv("task3_opt_H2.csv")
    min_tp_row = df.loc[df['tp'].idxmin()]
    print("Optimal parameters:")
    print(min_tp_row)

    '''
    m = 1
    Optimal parameters:
    index            2.800000e+01
    xnand2_size      3.000000e+00
    xnor2_size       5.000000e+00
    buffer_0_size    1.800000e+01
    tplh             3.561000e-11
    tphl             4.595000e-11
    tp               4.078000e-11
    temper           2.500000e+01
    alter#           1.000000e+00
    Name: 27, dtype: float64
    
    m = 2:
    Optimal parameters:
    index            1.120000e+02
    xnand2_size      2.000000e+00
    xnor2_size       2.000000e+00
    buffer_0_size    6.000000e+00
    buffer_1_size    2.400000e+01
    tplh             4.234000e-11
    tphl             3.304000e-11
    tp               3.769000e-11
    temper           2.500000e+01
    alter#           1.000000e+00
    Name: 111, dtype: float64

    Optimal parameters:
    index            1.000000e+00
    xnand2_size      1.000000e+00
    xnor2_size       1.000000e+00
    buffer_0_size    2.000000e+00
    buffer_1_size    8.000000e+00
    buffer_2_size    2.800000e+01
    tplh             3.422000e-11
    tphl             4.070000e-11
    tp               3.746000e-11
    temper           2.500000e+01
    alter#           1.000000e+00
    Name: 0, dtype: float64
    '''