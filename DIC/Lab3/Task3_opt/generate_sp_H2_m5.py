# gen_sp.py
# 
# 本脚本用于生成Task3优化版本（H2路径）的SPICE仿真文件
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
import itertools
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
* and NPA0
* XinvPA0: INV, SN = SP = CM
XinvPA0 PA0 NPA0 vdd gnd INV SN='SN_XinvPA0' SP='SP_XinvPA0' Lg = '20n'

* NAND2: SN = int(CM/1.5*2+0.5), SP = int(CM/1.5+0.5)
XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)
* NOR3: SN = int(CM/2+0.5), SP = int(CM/2*3+0.5)

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 PA0  word_0  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 NPA0 word_1  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 PA0  word_2  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 NPA0 word_3  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 PA0  word_4  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 NPA0 word_5  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 PA0  word_6  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 NPA0 word_7  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 PA0  word_8  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 NPA0 word_9  vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 PA0  word_10 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 NPA0 word_11 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 PA0  word_12 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 NPA0 word_13 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 PA0  word_14 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 NPA0 word_15 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 PA0  word_16 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 NPA0 word_17 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 PA0  word_18 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 NPA0 word_19 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 PA0  word_20 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 NPA0 word_21 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 PA0  word_22 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 NPA0 word_23 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 PA0  word_24 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 NPA0 word_25 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 PA0  word_26 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 NPA0 word_27 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 PA0  word_28 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 NPA0 word_29 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 PA0  word_30 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 NPA0 word_31 vdd gnd NOR3 SN="SN_NOR3" SP="SP_NOR3" Lg='20n'

* About critical path H2 (A1 input path):
* A1 -> Xinv11 -> NA1 -> Xinv12 -> PA1 -> XNAND2_1 -> NA2_PA1 -> XNOR3_2 -> word_2
* H2min = 12288
* P = (m+3)12288**[1/(m+3)] + m + 6 = N12288**(1/N) + N + 3

* Buffer inverters (m=4), INV: SN = SP = CM
Xbuffer_0 word_2 buffer_out_0 vdd gnd INV SN='SN_buffer_0' SP='SN_buffer_0' Lg='20n'
Xbuffer_1 buffer_out_0 buffer_out_1 vdd gnd INV SN='SN_buffer_1' SP='SN_buffer_1' Lg='20n'
Xbuffer_2 buffer_out_1 buffer_out_2 vdd gnd INV SN='SN_buffer_2' SP='SN_buffer_2' Lg='20n'
Xbuffer_3 buffer_out_2 buffer_out_3 vdd gnd INV SN='SN_buffer_3' SP='SN_buffer_3' Lg='20n'
Xbuffer_4 buffer_out_3 buffer_out_4 vdd gnd INV SN='SN_buffer_4' SP='SN_buffer_4' Lg='20n'
Xinv_load buffer_out_4 load_out vdd gnd INV SN='256' SP='256' Lg='20n'
{sweepdata}

.tran 1p 10n sweep data = sweepdata
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA1) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_4) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA1) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_4) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end
"""

def load_parameter_lists():
    """
    生成参数扫描列表，在最优值附近进行精细扫描
    
    注意：这里扫描的是CM（输入栅电容倍数），不是直接的晶体管尺寸
    SPICE中会通过.param语句自动计算对应的SN和SP
    """
    '''
    best value:
    XinvPA0 (INV):
        CM_XinvPA0: 1.6223896036109775
        SN_XinvPA0（已取整）: 2
        SP_XinvPA0（已取整）: 2
    
    NAND2:
        CM_NAND2: 1.6223896036109775
        SN_NAND2（已取整）: 2
        SP_NAND2（已取整）: 1

    NOR3:
        CM_NOR3: 0.4386913376508308
        SN_NOR3（已取整）: 1
        SP_NOR3（已取整）: 1

    反相器链: (CM, for INV: SN=SP=CM):
        CM values: [0.7117282653989009, 2.309401076758503, 7.493496595001984, 24.314741940850958, 78.89596907864079]
        Sizes for use: [1, 2, 7, 24, 79]
    '''
    # 1. 配置区域
    # 格式： "SN变量名": ("逻辑门类型", [SN扫描值列表])
    # 程序会自动推导对应的 SP变量名 (将SN替换为SP)
    # 支持的逻辑门类型: INV, NAND2, NOR2, NAND3, NOR3
    gate_configs = {
        "SN_XinvPA0": ("INV",   [1, 2, 3]),
        "SN_NAND2": ("NAND2", [2, 3]), 
        "SN_NOR3": ("NOR3", [1, 2]),
        "SN_buffer_0": ("INV",   [1, 2]),
        "SN_buffer_1": ("INV",   [1, 2, 3]),
        "SN_buffer_2": ("INV",   [6, 7, 8]),
        "SN_buffer_3": ("INV",   [22, 24, 26]),
        "SN_buffer_4": ("INV",   [71, 75, 79])
    }

    # ---------------- 以下逻辑自动处理 ----------------
    
    param_names = []      # 存储 .data 的表头变量名
    stage_combinations = [] # 存储每一级逻辑门的 (SN, SP) 组合列表

    # 遍历配置，生成每一级的参数对
    for sn_name, (gate_type, sn_values) in gate_configs.items():
        sp_name = sn_name.replace("SN", "SP")
        
        # 添加到表头 (顺序必须与后面数据生成的顺序一致)
        param_names.append(sn_name)
        param_names.append(sp_name)
        
        # 计算该级逻辑门所有可能的 (SN, SP) 组合，在这一步必须确保PUN和PDN的等效电阻相同，也就是说是P管和N管的尺寸是有一定关系的，关系如下：
        current_stage_pairs = []
        for sn in sn_values:
            sp = 0
            if gate_type == "INV":
                sp = sn
            elif gate_type == "NAND2":
                sp = sn / 2.0
            elif gate_type == "NOR2":
                sp = sn * 2.0
            elif gate_type == "NAND3":
                sp = sn / 3.0
            elif gate_type == "NOR3":
                sp = sn * 3.0
            else:
                raise ValueError(f"Unknown gate type: {gate_type}")
            
            # 强制保留整数
            sp = int(sp+0.5)
            current_stage_pairs.append((sn, sp))
        
        stage_combinations.append(current_stage_pairs)

    # 生成所有级逻辑门的笛卡尔积组合
    combinations = list(itertools.product(*stage_combinations))

    # 构造 .data 语句
    lines = []
    lines.append(f".data sweepdata {' '.join(param_names)}")
    
    for combo in combinations:
        # 展平元组: ((sn2, sp2), (sn3, sp3)) -> (sn2, sp2, sn3, sp3)
        flat_combo = []
        for pair in combo:
            flat_combo.extend(pair)
            
        # 将数字转换为字符串并用空格连接
        line = f"+ {' '.join(map(str, flat_combo))}"
        lines.append(line)
    
    return "\n".join(lines)
    

def GenSpiceScripts(outdir='.'):
    
    sweepdata_content = load_parameter_lists()
    content = TEMPLATE_TOP.format(sweepdata=sweepdata_content)
    file_name = f"task3_opt_H2_m5.sp"
    path_sp = Path(outdir) / file_name
    path_sp.write_text(content, encoding='utf-8')
    print(f"Generated {file_name} !")

if __name__ == '__main__':
    GenSpiceScripts()
