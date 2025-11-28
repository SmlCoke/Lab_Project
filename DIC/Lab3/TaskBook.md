# TaskBook
## Task1 USE Logical Effort to size Gates
### 电路情况
组合逻辑门链：(input) -> inv(minimum size) -> 3-NAND -> 2-NOR -> inv2 -> (output) -> load(64×inv)
我们需要选择合适的3-NAND, 2-NOR, inv2尺寸，以使得从input到output的延迟最小
衡量延时的方法为：tp = (tpHL + tpLH)/2

### 理论优化阶段
#### 优化方法建模
（分析待本人完善，你无需帮我补充）
用于理论分析求解的脚本：DIC\Lab3\Task1\opt.py（无需阅读）
#### 理论优化结果
结果被DIC\Lab3\Task1\opt.py保存至：DIC\Lab3\Task1\task1_theo_opt.log（需要阅读）
得到的理论最优解的电路参数为：
```
f1: 3.7224194364083982
f2: 1.8612097182041991
f3: 2.481612957605599
f4: 3.7224194364083982
S1: 1.0000000000000002
S2: 3.7224194364083987
S3: 6.92820323027551
S4: 17.193118909176672
```
由于这里的尺寸size对应着MOSFET模型里的NFIN，必须为整数，所以选择尺寸时四舍五入，为：
S2 = 4, S3 = 7, S4 = 17

### HSPICE仿真阶段
我们在仿真时，不单单只选择
```
S2 = 4, S3 = 7, S4 = 17
```
这一组点，而是在这一组点附近扫描，仿真这些不同尺寸组合下的延迟情况，然后得到最优延迟
用于仿真的HSPICE脚本：DIC\Lab3\Task1\task1.sp（无需阅读），选择的尺寸为：
S2: 2 to 6
S3: 5 to 9
S4: 15 to 19

### 仿真结果与分析
仿真结果见：DIC\Lab3\Task1\task1.csv（需要阅读并整理为LaTeX表格，数据量太大的话可以挑几个典型列出）
其中，最优尺寸组合以及延迟为：
```
index     5.000000e+00
s2        6.000000e+00
s3        5.000000e+00
s4        1.500000e+01
tplh      3.328000e-11
tphl      4.170000e-11
tp        3.749000e-11
temper    2.500000e+01
alter#    1.000000e+00
```
S2 = 6, S3 = 5, S4 = 15
均与理论值不一样，（分析待本人完善，你无需帮我补充）

## Task2 Use Logical Effort to Optimize 4×16 Decoder
### 电路情况
利用互补逻辑门搭建一个完整的4 to 16 Decoder，例如：
```spice
* Circuit: 4 to 16 decoder
* The first layer is 4 inverters. After this layer, we get 4 outputs
* which are NA3, NA2, NA1, NA0
Xinv31 A3 NA3 vdd gnd INV size = '1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV size = '1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV size = '1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV size = '1' Lg = '20n'

* The second layer is 4 inverters. After this layer, we get 4 outputs
* which are PA3, PA2, PA1, PA0
Xinv32 NA3 PA3 vdd gnd INV size = '1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV size = '1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV size = '1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV size = '1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 8 outputs
* which is Cartesian Product of (PA3, NA3) with (PA2, NA2) and (PA1, NA1) with (PA0, NA0)
.param x = 1
XNAND2_0 NA1 NA0 NA1_NA0 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_1 NA1 PA0 NA1_PA0 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_2 PA1 NA0 PA1_NA0 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_3 PA1 PA0 PA1_PA0 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_4 NA3 NA2 NA3_NA2 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_5 NA3 PA2 NA3_PA2 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_6 PA3 NA2 PA3_NA2 vdd gnd NAND2 size = "2" Lg = '20n'
XNAND2_7 PA3 PA2 PA3_PA2 vdd gnd NAND2 size = "2" Lg = '20n'

* The last layer is 16 NOR2 gates. After this layer, we get 16 outputs
* which is A3'A2'A1'A0', A3'A2'A1'A0, to A3A2A1A0
.param y = 1
XNOR2_0  NA3_NA2 NA1_NA0 word_0  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_1  NA3_NA2 NA1_PA0 word_1  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_2  NA3_NA2 PA1_NA0 word_2  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_3  NA3_NA2 PA1_PA0 word_3  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_4  NA3_PA2 NA1_NA0 word_4  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_5  NA3_PA2 NA1_PA0 word_5  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_6  NA3_PA2 PA1_NA0 word_6  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_7  NA3_PA2 PA1_PA0 word_7  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_8  PA3_NA2 NA1_NA0 word_8  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_9  PA3_NA2 NA1_PA0 word_9  vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_10 PA3_NA2 PA1_NA0 word_10 vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_11 PA3_NA2 PA1_PA0 word_11 vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_12 PA3_PA2 NA1_NA0 word_12 vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_13 PA3_PA2 NA1_PA0 word_13 vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_14 PA3_PA2 PA1_NA0 word_14 vdd gnd NOR2 size = "1" Lg = '20n'
XNOR2_15 PA3_PA2 PA1_PA0 word_15 vdd gnd NOR2 size = "1" Lg = '20n'   
```
负载是电容（128倍最小反相器尺寸的反相器实现）
然后，考察其中一条关键路径的延迟并进行优化。（该电路中，所有关键路径的种类都相同，即仅过了相同数量相同种类的逻辑门，因此只需要考虑其中一条即可）
优化方法就是在word_x和负载电容间插入多级反相器，考察从```电路中第一级反相器的输出结点（NA0~NA3）到负载电容输入结点```的最小延迟

### 理论优化阶段
#### 优化方法建模
（分析待本人完善，你无需帮我补充）
用于理论分析求解的脚本：DIC\Lab3\Task2\opt.py（无需阅读）
#### 理论优化结果
结果被DIC\Lab3\Task2\opt.py保存至DIC\Lab3\Task2\task2_theo_opt.log（需要阅读）
其中`D`越小代表延迟越小，可见当：
```
m = 3, N = 6, D = 28.80544711398567, hopt = 3.634241185664279
```
有理论上的最小延迟

### HSPICE仿真阶段

#### 插入反相器级数的进一步确定
虽然理论上在：
```
m = 3, N = 6, D = 28.80544711398567, hopt = 3.634241185664279
```
达到最优延迟，但是实际上可能有出入，因此我尝试了 m=0 到 m=5 的情况，每种情况采用对应的最优尺寸参数，得到了不同级数的延迟结果：DIC\Lab3\Task2\task2_s_opt_m.csv（需要阅读）
可以发现，实际上在`m=2`时有最优延迟

#### 尺寸参数的精细扫描
根据以上的结果，我们不仅仅在`m=2`时扫描参数，在其临近的m=1和m=3时也一同扫描，尽可能的扩大范围得到最优延迟。
此时，对应不同m值的HSPICE脚本的自动化生成以及不同尺寸参数的扫描范围均由：
DIC\Lab3\Task2_opt\generate_sp_m1.py（需要阅读）
DIC\Lab3\Task2_opt\generate_sp_m2.py（需要阅读）
DIC\Lab3\Task2_opt\generate_sp_m3.py（需要阅读）
这三个脚本给出，这三个脚本你需要阅读，并且在报告中注明参数扫描范围。

#### 仿真结果与分析
三种情况的最优尺寸参数以及对应最优延迟：
m=1:
```
index            2.800000e+01
xnand2_size      3.000000e+00
xnor2_size       5.000000e+00
buffer_0_size    1.800000e+01
tplh             3.561000e-11
tphl             4.595000e-11
tp               4.078000e-11
temper           2.500000e+01
alter#           1.000000e+00
```

m=2:
```
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
```

m=3:
```
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
```

可见，在m=3时，我们获得了最优延迟结果。（分析待本人完善，你无需帮我补充）


## Task3 Use Logical Effort to Optimize 5×32 Decoder
### 电路情况
### 电路情况
利用互补逻辑门搭建一个完整的5 to 32 Decoder，例如：
```
* Circuit: 4 to 16 decoder
* The first layer is 4 inverters. After this layer, we get 4 outputs
* which are NA4, NA3, NA2, NA1, NA0
Xinv41 A4 NA4 vdd gnd INV size = '1' Lg = '20n'
Xinv31 A3 NA3 vdd gnd INV size = '1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV size = '1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV size = '1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV size = '1' Lg = '20n'

* The second layer is 4 inverters. After this layer, we get 5 outputs
* which are PA4, PA3, PA2, PA1, PA0
Xinv42 NA4 PA4 vdd gnd INV size = '1' Lg = '20n'
Xinv32 NA3 PA3 vdd gnd INV size = '1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV size = '1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV size = '1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV size = '1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 9 outputs
* which is Cartesian Product of (PA4, NA4) with (PA3, NA3) and (PA2, NA2) with (PA1, NA1)
* and NPA0
XinvPA0 PA0 NPA0 vdd gnd INV size = '4' Lg = '20n'

XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 size = "4" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 size = "4" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 PA0  word_0  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 NPA0 word_1  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 PA0  word_2  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 NPA0 word_3  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 PA0  word_4  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 NPA0 word_5  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 PA0  word_6  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 NPA0 word_7  vdd gnd NOR3 size="1" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 PA0  word_8  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 NPA0 word_9  vdd gnd NOR3 size="1" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 PA0  word_10 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 NPA0 word_11 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 PA0  word_12 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 NPA0 word_13 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 PA0  word_14 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 NPA0 word_15 vdd gnd NOR3 size="1" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 PA0  word_16 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 NPA0 word_17 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 PA0  word_18 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 NPA0 word_19 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 PA0  word_20 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 NPA0 word_21 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 PA0  word_22 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 NPA0 word_23 vdd gnd NOR3 size="1" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 PA0  word_24 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 NPA0 word_25 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 PA0  word_26 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 NPA0 word_27 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 PA0  word_28 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 NPA0 word_29 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 PA0  word_30 vdd gnd NOR3 size="1" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 NPA0 word_31 vdd gnd NOR3 size="1" Lg='20n' 
```
负载是电容（256倍最小反相器尺寸的反相器实现）
然后，考察其中关键路径的延迟并进行优化。
优化方法就是在word_x和负载电容间插入多级反相器，考察从```电路中第一级反相器的输出结点（NA0~NA4）到负载电容输入结点```的最小延迟
但是，与Task2不一致的是，这里有**两种不同的关键路径**，需要独立考虑：
```
critical_path1: A0 -> Xinv01 -> NA0（计算延迟的起始点） -> Xinv02 -> PA0 -> XinvPA0 -> NPA0 -> XNOR3_1 -> word_1（这条路的延迟函数记作H1）
critical_path2: A1 -> Xinv11 -> NA1（计算延迟的起始点） -> Xinv12 -> PA1 -> XNAND2_1 -> NA2_PA1 -> XNOR3_2 -> word_2（这条路的延迟函数记作H2）
```

这两条关键路径独立考虑，给出对应两组最优参数即可，不需要综合考虑（即不需要进行多目标优化）

### 理论优化阶段
#### 优化方法建模
（分析待本人完善，你无需帮我补充）
用于理论分析求解的脚本：DIC\Lab3\Task3\opt_H1.py, DIC\Lab3\Task3\opt_H1_pro.py, DIC\Lab3\Task3\opt_H2.py（无需阅读）（至于为什么会有两个H1，因为采取了不同的考虑方式，H1_pro考虑的更简化，对于只有A0的反转，A1-A4不变有更小的延迟，H1考虑的是更一般的情况）
#### 理论优化结果
结果被上面三个脚本保存至DIC\Lab3\Task3\task3_H1_theo_opt.log、DIC\Lab3\Task3\task3_H1_pro_theo_opt.log、DIC\Lab3\Task3\task3_H2_theo_opt.log（需要阅读）
其中`D`或者`H1_min`越小代表延迟越小。
可见三种情况的理论最优参数分别为：
H1:
```
----------------------------------------------------------------------
------------------------------ When m = 7 ------------------------------
----------------------------------------------------------------------
optimal_p = [2.90237908]
H1_prime = [1.77635684e-15]
H1_min = [27.39690574]
```

H1_pro:
```
m = 4, N = 7, D = 35.36026259938939, hopt = 3.6228946570556264
```

H2:
```
m = 4, N = 7, D = 36.87259707408367, hopt = 3.83894243915481
```


### HSPICE仿真阶段

#### 插入反相器级数的进一步确定
虽然三种情况理论上在上面提到的参数时达到最优延迟，但是实际上可能有出入，因此我也就对插入反相器的个数m进行的上下浮动考虑。
```
H1: m = 1 -> 9
H1_pro: m = 1 -> 8
H2: m = 2 -> 8
```
每种情况采用对应的最优尺寸参数优化，得到了理论最优参数下的最小延迟与m的关系仿真数据见：
```
H1: DIC\Lab3\Task3\merged_H1.csv（需要阅读）
H1_pro: DIC\Lab3\Task3\merged_H1_pro.csv（需要阅读）
H2：DIC\Lab3\Task3\merged_H2.csv（需要阅读）
```
分别在如下参数达到最优：
```
H1: m=4
H1_pro: m=3
H2：m=3
```
因为计算出来的H1最优延迟比H1_pro高很多，同时由于本次实验只考虑H1_pro研究的这种情况，我们下面精细扫描时只考虑H1_pro和H2

#### 尺寸参数的精细扫描
根据以上的结果，由于计算资源优先，两种(H1_pro, H2)情况下我们仅仅在最优m时扫描参数，在其临近的m这一次就不再扫描了。
此时，HSPICE脚本的自动化生成以及不同尺寸参数的扫描范围均由：
DIC\Lab3\Task3_opt\generate_sp_H1_pro.py（需要阅读）
DIC\Lab3\Task3_opt\generate_sp_H2.py（需要阅读）
这三个脚本给出，这三个脚本你需要阅读，并且在报告中注明参数扫描范围。

#### 仿真结果与分析
三种情况的最优尺寸参数以及对应最优延迟：
H1_pro
```
index            7.780000e+02
xinvpa0_size     5.000000e+00
xnand2_size      3.000000e+00
xnor3_size       1.000000e+00
buffer_0_size    3.000000e+00
buffer_1_size    1.100000e+01
buffer_2_size    4.800000e+01
tplh             5.977000e-11
tphl             6.862000e-11
tp               6.419000e-11
temper           2.500000e+01
alter#           1.000000e+00
```

H2:
```
index            1.870000e+02
xinvpa0_size     1.000000e+00
xnand2_size      2.000000e+00
xnor3_size       1.000000e+00
buffer_0_size    3.000000e+00
buffer_1_size    1.000000e+01
buffer_2_size    4.300000e+01
tplh             4.306000e-11
tphl             5.352000e-11
tp               4.829000e-11
temper           2.500000e+01
alter#           1.000000e+00
```

可见，在以上给出的尺寸参数下，我们获得了最优延迟结果。（分析待本人完善，你无需帮我补充）