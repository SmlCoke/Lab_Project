# gen_sp.py

from pathlib import Path

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 3: Use Logical Effort to Optimize 5×32 Decoder
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../../16nfet.pm'
.include '../../16pfet.pm'

* source
Vdd vdd 0 DC 'SUPPLY'
VA4 A4 0 DC '0'
VA3 A3 0 DC '0'
VA2 A2 0 DC '0'
VA1 A1 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)
VA0 A0 0 DC '0'

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
.subckt INV in out vdd gnd size=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='size'
Mp out in vdd vdd pfet L='Lg' NFIN ='size'
.ends INV

* Sub circuit: 2-NAND
.subckt NAND2 in1 in2 out vdd gnd size=1 Lg=20n
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='size'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='size'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='size'
Mn2 source1 in2 gnd gnd nfet L='Lg' NFIN='size'
.ends NAND2

* Sub circuit: 3-NOR
.subckt NOR3 in1 in2 in3 out vdd gnd size=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='size'
Mp2 source_p1 in2 source_p2 vdd pfet L='Lg' NFIN='size'
Mp3 source_p2 in3 vdd vdd pfet L='Lg' NFIN='size'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='size'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='size'
Mn3 out in3 gnd gnd nfet L='Lg' NFIN='size'
.ends NOR3

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
XinvPA0 PA0 NPA0 vdd gnd INV size = '{XinvPA0_size}' Lg = '20n'

XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 PA0  word_0  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 NPA0 word_1  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 PA0  word_2  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 NPA0 word_3  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 PA0  word_4  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 NPA0 word_5  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 PA0  word_6  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 NPA0 word_7  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 PA0  word_8  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 NPA0 word_9  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 PA0  word_10 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 NPA0 word_11 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 PA0  word_12 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 NPA0 word_13 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 PA0  word_14 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 NPA0 word_15 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 PA0  word_16 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 NPA0 word_17 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 PA0  word_18 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 NPA0 word_19 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 PA0  word_20 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 NPA0 word_21 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 PA0  word_22 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 NPA0 word_23 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 PA0  word_24 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 NPA0 word_25 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 PA0  word_26 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 NPA0 word_27 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 PA0  word_28 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 NPA0 word_29 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 PA0  word_30 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 NPA0 word_31 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'  

* About critical path, we can obviously see that the path which passes 3'inv(A0 -> NA0 -> PA0 -> NPA0) is the longest.
* Such paths we have two kinds, take A0/A1 as input for example:
* A0 -> Xinv01 -> NA0 -> Xinv02 -> PA0 -> XinvPA0 -> NPA0 -> XNOR3_0 -> word_0
* A1 -> Xinv11 -> NA1 -> Xinv12 -> PA1 -> XNAND2_1 -> NA2_PA1 -> XNOR3_2 -> word_2
* Path1: 
* Xinv02: p = 1, g = 1, f = XinvPA0_size/Xinv02_size, b = (16*XNOR3 + XinvPA0)/XinvPA0 C
* XinvPA0: p = 1, g = 1, f = XNOR3_0_size/XinvPA0_size, b = 16
* XNOR3_0: p = 3, g = 2, f = Xbuffer_0_size/XNOR3_0_size, b = 1
* H1 = x1 + 16y + 16y/x1 + 2z_1/y + z_2/z_1 + ... + z_m/z_(m-1) + 256/zm
* Then there are m inv
* Path2:
* Xinv12: p = 1, g = 1, f = XNAND2_1/Xinv12, b = 2 
* XNAND2_1: p = 2, g = 3/2, f = XNOR3_2/XNAND2_1, b = 8
* XNOR3_2: p = 3, g = 2, f = Xbuffer_0_size/XNOR3_2_size, b = 1
* H2 = 2x2 + 12y/x2 + 2z_1/y + z_2/z_1 + ... + z_m/z_(m-1) + 256/zm
* G2 = 3, B2 = 16, F2 = 256
* H2min = 12288
* P = (1 + 2 + 3 + m) + (m+3)12288**[1/(m+3)] = (m+3)12288**[1/(m+3)] + m + 6 = N12288**(1/N) + N + 3

* x1 = XinvPA0_size, x2 = XNAND2_size, y = XNOR3_size

{instance_lines}

.tran 1p 10n 
.probe V(*) I(*)
{measure_lines}
.measure tran tp param='(tpLH+tpHL)/2'
.end
"""


    
    
    

# accurate的意思是，精确计算每个器件的尺寸和等效扇出，然后实际应用时再取整(四舍五入)，一定程度上防止向下取整的误差累计
def load_parameter_accurate(m):
    # generate instance lines up to m, m refers to the number of buffers(1 buffer = 1 inverter)
    hopt = 12288**(1/(m+3))

    # 计算XNAND2_1尺寸
    Xinv12_f = hopt/1/2
    XNAND2_size = Xinv12_f
    XNAND2_size_for_use = int(XNAND2_size + 0.5) if XNAND2_size + 0.5 > 1 else 1

    # 计算XNOR3尺寸
    XNAND2_f = hopt/2/8
    XNOR3_size = XNAND2_f * XNAND2_size
    XNOR3_size_for_use = int(XNOR3_size + 0.5) if XNOR3_size + 0.5 > 1 else 1  # 四舍五入取整

    # 逐级计算buffer尺寸
    buffer_sizes = [hopt*XNOR3_size/2]
    buffer_sizes_for_use = [int(size+0.5) for size in buffer_sizes]

    buffer_f = hopt/1/1
    for i in range(1,m):
        buffer_sizes.append(buffer_f*buffer_sizes[-1])
        buffer_sizes_for_use.append(int(buffer_sizes[-1]+0.5))

    # 强制让计算出来的尺寸不为0
    for index in range(len(buffer_sizes_for_use)):
        if buffer_sizes_for_use[index] == 0:
            buffer_sizes_for_use[index] = 1

    last_node = [f"buffer_out_{0}"]
    instances_lines = [f"Xbuffer_0 word_2 buffer_out_0 vdd gnd INV size = '{buffer_sizes_for_use[0]}' Lg='20n'\n"]
    for i in range(1,m):
        instances_lines.append(f"Xbuffer_{i} buffer_out_{i-1} buffer_out_{i} vdd gnd INV size='{buffer_sizes_for_use[i]}' Lg='20n'\n")
        last_node.append(f"buffer_out_{i}")
    instances_lines.append(f"Xinv_load {last_node[-1]} load_out vdd gnd INV size='256' Lg='20n'\n")
    measures_lines = []
    if (m %2 == 0):
        measures_lines.append(f".measure tran tpLH TRIG V(NA1) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measures_lines.append(f".measure tran tpHL TRIG V(NA1) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")
    else:
        measures_lines.append(f".measure tran tpLH TRIG V(NA1) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measures_lines.append(f".measure tran tpHL TRIG V(NA1) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")

    instances_lines = "".join(instances_lines)
    measures_lines = "".join(measures_lines)

    return XNAND2_size, XNAND2_size_for_use, XNOR3_size, XNOR3_size_for_use, buffer_sizes, buffer_sizes_for_use, instances_lines, measures_lines




def write_for_N(m, outdir='.'):
    if (load_parameter_accurate(m) is None):
        print(f"Invalid configuration for m={m}, in this case, some gates have 0 Nfins.")
        return
    XNAND2_size, XNAND2_size_for_use, XNOR3_size, XNOR3_size_for_use, buffer_sizes, buffer_sizes_for_use, inst_lines, measure_lines = load_parameter_accurate(m)
    log_content = f'''
    When num of Inverters is {m}:
    hopt: {12288**(1/(m+3))}
    XNAND2_size: {XNAND2_size}
    XNAND2_size (for use): {XNAND2_size_for_use}
    XNOR3_size: {XNOR3_size}
    XNOR3_size (for use): {XNOR3_size_for_use}
    all buffer sizes: {buffer_sizes}
    all buffer sizes (for use): {buffer_sizes_for_use}
    '''
    content = TEMPLATE_TOP.format(XinvPA0_size = XNAND2_size_for_use, XNAND2_size = XNAND2_size_for_use, XNOR3_size = XNOR3_size_for_use, instance_lines=inst_lines, measure_lines=measure_lines)

    # 自动创建目录并保存脚本
    path_dir = Path(outdir) / f'H2_m{m}'   # 目标文件夹，例如 ./N=4
    path_dir.mkdir(parents=True, exist_ok=True)  # ✅ 自动创建（含父目录）
    path_sp = path_dir / f"task3_H2_m{m}.sp"   # 最终文件路径
    path_log = path_dir / f"task3_H2_m{m}.log"   # 日志文件路径
    path_sp.write_text(content,encoding='utf-8')
    path_log.write_text(log_content,encoding='utf-8')
    print(f"Written {path_log} done!")
    print(f"Written {path_sp} done!")

if __name__ == '__main__':
    for i in range(2, 9):
        write_for_N(i, outdir='.')
