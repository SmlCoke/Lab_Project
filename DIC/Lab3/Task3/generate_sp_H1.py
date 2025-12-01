# gen_sp.py
# 
# 本脚本用于生成Task3（5×32译码器）H1路径的SPICE仿真文件
# 
# 关键概念：
# - CM (CMulti): 逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数
# - SN, SP: NMOS和PMOS晶体管的尺寸(NFIN参数)
# 
# CM到SN/SP的转换关系（来自Relation.md）：
# - INV:   SN = CM, SP = CM
# - NAND2: SN = CM/1.5*2, SP = CM/1.5  (g = 1.5)
# - NOR3:  SN = CM/2, SP = CM/2*3      (g = 2)
#
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
VA1 A1 0 DC '0'
VA0 A0 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
* CM到SN/SP转换: SN = CM, SP = CM
.subckt INV in out vdd gnd SN=1 SP=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='SN'
Mp out in vdd vdd pfet L='Lg' NFIN ='SP'
.ends INV

* Sub circuit: 2-NAND
* g = 1.5
* CM到SN/SP转换: SN = CM/1.5*2, SP = CM/1.5
.subckt NAND2 in1 in2 out vdd gnd SN=1 SP=1 Lg=20n
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='SP'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='SP'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='SN'
Mn2 source1 in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NAND2

* Sub circuit: 3-NOR
* g = 2
* CM到SN/SP转换: SN = CM/2, SP = CM/2*3
.subckt NOR3 in1 in2 in3 out vdd gnd SN=1 SP=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 source_p2 vdd pfet L='Lg' NFIN='SP'
Mp3 source_p2 in3 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
Mn3 out in3 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR3

* Circuit: 5 to 32 decoder
* The first layer is 5 inverters. After this layer, we get 5 outputs
* which are NA4, NA3, NA2, NA1, NA0
Xinv41 A4 NA4 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv31 A3 NA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The second layer is 5 inverters. After this layer, we get 5 outputs
* which are PA4, PA3, PA2, PA1, PA0
Xinv42 NA4 PA4 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv32 NA3 PA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 9 outputs
* which is Cartesian Product of (PA4, NA4) with (PA3, NA3) and (PA2, NA2) with (PA1, NA1)
* and NPA0 (inverter for PA0)
* XinvPA0: INV, CM = XinvPA0_size, SN = SP = CM
XinvPA0 PA0 NPA0 vdd gnd INV SN='{SN_XinvPA0}' SP='{SP_XinvPA0}' Lg = '20n'

* NAND2: CM = XNAND2_cm, SN = CM/1.5*2, SP = CM/1.5
XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)
* NOR3: CM = XNOR3_cm, SN = CM/2, SP = CM/2*3

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 PA0  word_0  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 NPA0 word_1  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 PA0  word_2  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 NPA0 word_3  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 PA0  word_4  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 NPA0 word_5  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 PA0  word_6  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 NPA0 word_7  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 PA0  word_8  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 NPA0 word_9  vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 PA0  word_10 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 NPA0 word_11 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 PA0  word_12 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 NPA0 word_13 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 PA0  word_14 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 NPA0 word_15 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 PA0  word_16 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 NPA0 word_17 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 PA0  word_18 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 NPA0 word_19 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 PA0  word_20 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 NPA0 word_21 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 PA0  word_22 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 NPA0 word_23 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 PA0  word_24 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 NPA0 word_25 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 PA0  word_26 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 NPA0 word_27 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 PA0  word_28 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 NPA0 word_29 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 PA0  word_30 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 NPA0 word_31 vdd gnd NOR3 SN="{SN_NOR3}" SP="{SP_NOR3}" Lg='20n'  

* About critical path, we can obviously see that the path which passes 3'inv(A0 -> NA0 -> PA0 -> NPA0) is the longest.
* Such paths we have two kinds, take A0/A1 as input for example:
* A0 -> Xinv01 -> NA0 -> Xinv02 -> PA0 -> XinvPA0 -> NPA0 -> XNOR3_1 -> word_1
* A1 -> Xinv11 -> NA1 -> Xinv12 -> PA1 -> XNAND2_1 -> NA2_PA1 -> XNOR3_2 -> word_2
* Path1: 
* Xinv02: p = 1, g = 1, f = XinvPA0_size/Xinv02_size, b = (16*XNOR3 + XinvPA0)/XinvPA0 C
* XinvPA0: p = 1, g = 1, f = XNOR3_1_size/XinvPA0_size, b = 16
* XNOR3_1: p = 3, g = 2, f = Xbuffer_0_size/XNOR3_1_size, b = 1
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

# =============================================================================
# CM到SN/SP转换函数
# =============================================================================

def cm_to_sn_sp_inv(cm):
    """INV: SN = SP = CM"""
    return cm, cm

def cm_to_sn_sp_nand2(cm):
    """NAND2: g = 1.5, SN = CM/1.5*2, SP = CM/1.5"""
    sn = cm / 1.5 * 2
    sp = cm / 1.5
    return sn, sp

def cm_to_sn_sp_nor3(cm):
    """NOR3: g = 2, SN = CM/2, SP = CM/2*3"""
    sn = cm / 2
    sp = cm / 2 * 3
    return sn, sp

def solve_q(m):
    """
    求解最优q值（用于H1路径优化）
    这些值是预计算好的数值解
    """
    if m == 1:
        return 21.65280595
    if m == 2:
        return 10.28186416
    if m == 3:
        return 6.55236799
    if m == 4:
        return 4.84011329
    if m == 5:
        return 3.8920352
    if m == 6:
        return 3.30131451
    if m == 7:
        return 2.90237908
    if m == 8:
        return 2.61683266
    if m == 9:
        return 2.40330133
    else:
        raise ValueError(f"Unsupported m={m}")
    
# =============================================================================
# accurate的意思是，精确计算每个器件的尺寸和等效扇出，然后实际应用时再取整(四舍五入)
# 一定程度上防止向下取整的误差累计
# 
# 注意：现在计算的是CM（输入栅电容倍数），然后通过转换函数得到SN和SP
# =============================================================================
def load_parameter_accurate(m):
    """
    生成参数配置
    
    参数:
        m: 缓冲反相器的数量
        
    返回:
        各种尺寸参数和实例行
    """
    q = solve_q(m)
    
    # 计算NOR3的CM（输入栅电容倍数）
    CM_NOR3 = 512/(q**(m+1))
    
    # 将CM_NOR3转换为SN和SP
    SN_NOR3_raw, SP_NOR3_raw = cm_to_sn_sp_nor3(CM_NOR3)
    SN_NOR3 = max(1, int(SN_NOR3_raw + 0.5))
    SP_NOR3 = max(1, int(SP_NOR3_raw + 0.5))

    # 计算XinvPA0的CM（输入栅电容倍数）
    # 对于INV，CM = 尺寸
    CM_XinvPA0 = 4*CM_NOR3**(1/2)
    SN_XinvPA0, SP_XinvPA0 = cm_to_sn_sp_inv(CM_XinvPA0)
    SN_XinvPA0 = max(1, int(SN_XinvPA0 + 0.5))
    SP_XinvPA0 = max(1, int(SP_XinvPA0 + 0.5))
    
    # NAND2的CM与XinvPA0相同（在原代码中这样设置）
    CM_NAND2 = CM_XinvPA0
    SN_NAND2_raw, SP_NAND2_raw = cm_to_sn_sp_nand2(CM_NAND2)
    SN_NAND2 = max(1, int(SN_NAND2_raw + 0.5))
    SP_NAND2 = max(1, int(SP_NAND2_raw + 0.5))

    # 逐级计算buffer尺寸（INV的CM = 尺寸）
    buffer_cm = [q*CM_NOR3/2]
    buffer_size_for_use = [max(1, int(size+0.5)) for size in buffer_cm]

    for i in range(1, m):
        buffer_cm.append(q*buffer_cm[-1])
        buffer_size_for_use.append(max(1, int(buffer_cm[-1]+0.5)))

    last_node = [f"buffer_out_{0}"]
    # 对于buffer INV，SN = SP = CM
    instances_lines = [f"Xbuffer_0 word_1 buffer_out_0 vdd gnd INV SN='{buffer_size_for_use[0]}' SP='{buffer_size_for_use[0]}' Lg='20n'\n"]
    for i in range(1, m):
        instances_lines.append(f"Xbuffer_{i} buffer_out_{i-1} buffer_out_{i} vdd gnd INV SN='{buffer_size_for_use[i]}' SP='{buffer_size_for_use[i]}' Lg='20n'\n")
        last_node.append(f"buffer_out_{i}")
    instances_lines.append(f"Xinv_load {last_node[-1]} load_out vdd gnd INV SN='256' SP='256' Lg='20n'\n")
    
    measures_lines = []
    if (m % 2 == 0):
        measures_lines.append(f".measure tran tpLH TRIG V(NA0) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measures_lines.append(f".measure tran tpHL TRIG V(NA0) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")
    else:
        measures_lines.append(f".measure tran tpLH TRIG V(NA0) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measures_lines.append(f".measure tran tpHL TRIG V(NA0) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")

    instances_lines = "".join(instances_lines)
    measures_lines = "".join(measures_lines)

    return (CM_XinvPA0, SN_XinvPA0, SP_XinvPA0,
            CM_NAND2, SN_NAND2, SP_NAND2,
            CM_NOR3, SN_NOR3, SP_NOR3,
            buffer_cm, buffer_size_for_use,
            instances_lines, measures_lines)


def write_for_N(m, outdir='.'):
    """
    生成指定m值的SPICE仿真文件
    """
    result = load_parameter_accurate(m)
    if result is None:
        print(f"Invalid configuration for m={m}, in this case, some gates have 0 Nfins.")
        return
    
    (CM_XinvPA0, SN_XinvPA0, SP_XinvPA0,
     CM_NAND2, SN_NAND2, SP_NAND2,
     CM_NOR3, SN_NOR3, SP_NOR3,
     buffer_cm, buffer_size_for_use,
     inst_lines, measure_lines) = result
    
    log_content = f'''
    When num of Inverters is {m}:
    best_q: {solve_q(m)}
    
    XinvPA0 (INV):
      CM_XinvPA0: {CM_XinvPA0}
      SN_XinvPA0: {SN_XinvPA0}
      SP_XinvPA0: {SP_XinvPA0}
    
    NAND2:
      CM_NAND2: {CM_NAND2}
      SN_NAND2: {SN_NAND2}
      SP_NAND2: {SP_NAND2}
    
    NOR3:
      CM_NOR3: {CM_NOR3}
      SN_NOR3: {SN_NOR3}
      SP_NOR3: {SP_NOR3}
    
    Buffer sizes (CM, for INV: SN=SP=CM):
      CM values: {buffer_cm}
      Sizes for use: {buffer_size_for_use}
    '''
    
    content = TEMPLATE_TOP.format(
        SN_XinvPA0=SN_XinvPA0, SP_XinvPA0=SP_XinvPA0,
        SN_NAND2=SN_NAND2, SP_NAND2=SP_NAND2,
        SN_NOR3=SN_NOR3, SP_NOR3=SP_NOR3,
        instance_lines=inst_lines, measure_lines=measure_lines
    )

    # 自动创建目录并保存脚本
    path_dir = Path(outdir) / f'H1_m{m}'
    path_dir.mkdir(parents=True, exist_ok=True)
    path_sp = path_dir / f"task3_H1_m{m}.sp"
    path_log = path_dir / f"task3_H1_m{m}.log"
    path_sp.write_text(content, encoding='utf-8')
    path_log.write_text(log_content, encoding='utf-8')
    print(f"Written {path_log} done!")
    print(f"Written {path_sp} done!")

if __name__ == '__main__':
    for i in range(1, 10):
        write_for_N(i, outdir='.')
