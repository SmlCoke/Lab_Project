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

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 3: Use Logical Effort to Optimize 5×32 Decoder
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 
.param CM_XinvPA0 = 1
.param CM_NAND2 = 1
.param CM_NOR3 = 1
.param CM_buffer_0 = 1
.param CM_buffer_1 = 1
.param CM_buffer_2 = 1

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
XinvPA0 PA0 NPA0 vdd gnd INV SN='CM_XinvPA0' SP='CM_XinvPA0' Lg = '20n'

* NAND2: SN = int(CM/1.5*2+0.5), SP = int(CM/1.5+0.5)
.param SN_NAND2 = 'int(CM_NAND2/1.5*2+0.5)'
.param SP_NAND2 = 'int(CM_NAND2/1.5+0.5)'
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
.param SN_NOR3 = 'int(CM_NOR3/2+0.5)'
.param SP_NOR3 = 'int(CM_NOR3/2*3+0.5)'

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

* Buffer inverters (m=3), INV: SN = SP = CM
Xbuffer_0 word_2 buffer_out_0 vdd gnd INV SN='CM_buffer_0' SP='CM_buffer_0' Lg='20n'
Xbuffer_1 buffer_out_0 buffer_out_1 vdd gnd INV SN='CM_buffer_1' SP='CM_buffer_1' Lg='20n'
Xbuffer_2 buffer_out_1 buffer_out_2 vdd gnd INV SN='CM_buffer_2' SP='CM_buffer_2' Lg='20n'
Xinv_load buffer_out_2 load_out vdd gnd INV SN='256' SP='256' Lg='20n'
{sweepdata}

.tran 1p 10n sweep data = sweepdata
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA1) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_2) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA1) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_2) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end
"""

def load_parameter_lists():
    """
    生成参数扫描列表，在最优值附近进行精细扫描
    
    注意：这里扫描的是CM（输入栅电容倍数），不是直接的晶体管尺寸
    SPICE中会通过.param语句自动计算对应的SN和SP
    """
    # 最优值中心点（使用CM）
    center = {
        'CM_XinvPA0': 2,
        'CM_NAND2': 2,
        'CM_NOR3': 1,
        'CM_buffer_0': 2,
        'CM_buffer_1': 8,
        'CM_buffer_2': 40
    }
    
    # 定义每个参数的扫描范围和步长
    # 格式：参数名: (中心值, 扫描半径, 步长)
    scan_config = {
        'CM_XinvPA0': (center['CM_XinvPA0'], 1, 1),      # 2±1, 步长1 -> [1, 2, 3]
        'CM_NAND2': (center['CM_NAND2'], 1, 1),      # 2±1, 步长1 -> [1, 2, 3]
        'CM_NOR3': (center['CM_NOR3'], 1, 1),        # 1±1, 步长1 -> [1, 2]
        'CM_buffer_0': (center['CM_buffer_0'], 1, 1),  # 2±1, 步长1 -> [2, 3, 4]
        'CM_buffer_1': (center['CM_buffer_1'], 2, 2),  # 8±2, 步长2 -> [6, 8, 10]
        'CM_buffer_2': (center['CM_buffer_2'], 9, 3),  # 40±9, 步长3 -> [34, 37, 40, 43, 46.49]
    }
    
    # 生成每个参数的扫描值列表
    param_ranges = {}
    for param_name, (center_val, radius, step) in scan_config.items():
        min_val = max(1, center_val - radius)  # 确保最小值≥1
        max_val = center_val + radius
        param_ranges[param_name] = list(range(min_val, max_val + 1, step))
        print(f"{param_name}: {param_ranges[param_name]}")
    
    # 生成笛卡尔积（所有参数组合）
    parameter_lists = []
    for cm_xinvpa0 in param_ranges['CM_XinvPA0']:
        for cm_nand2 in param_ranges['CM_NAND2']:
            for cm_nor3 in param_ranges['CM_NOR3']:
                for cm_buf0 in param_ranges['CM_buffer_0']:
                    for cm_buf1 in param_ranges['CM_buffer_1']:
                        for cm_buf2 in param_ranges['CM_buffer_2']:
                            parameter_lists.append({
                                'CM_XinvPA0': cm_xinvpa0,
                                'CM_NAND2': cm_nand2,
                                'CM_NOR3': cm_nor3,
                                'CM_buffer_0': cm_buf0,
                                'CM_buffer_1': cm_buf1,
                                'CM_buffer_2': cm_buf2
                            })
    print(f"\nGenerated {len(parameter_lists)} parameter combinations")
    print(f"Example parameter combinations:")
    for i, params in enumerate(parameter_lists[:3]):
        print(f"  {i+1}. {params}")
    print(f"  ...")
    
    return parameter_lists
    

def GenSpiceScripts(outdir='.'):
    """
    生成SPICE仿真脚本
    """
    parameter_lists = load_parameter_lists()
    sweepdata_content = [".data sweepdata CM_XinvPA0 CM_NAND2 CM_NOR3 CM_buffer_0 CM_buffer_1 CM_buffer_2 \n"]
    for i, param_dict in enumerate(parameter_lists, 1):
        sweepdata_content.append(f"+ {param_dict['CM_XinvPA0']} {param_dict['CM_NAND2']} {param_dict['CM_NOR3']} {param_dict['CM_buffer_0']} {param_dict['CM_buffer_1']} {param_dict['CM_buffer_2']}\n")
    sweepdata_content.append(".enddata\n")

    sweepdata_content = "".join(sweepdata_content)
    content = TEMPLATE_TOP.format(sweepdata=sweepdata_content)
    file_name = f"task3_opt_H2.sp"
    path_sp = Path(outdir) / file_name
    path_sp.write_text(content, encoding='utf-8')
    print(f"Generated {file_name}")

if __name__ == '__main__':
    GenSpiceScripts()
