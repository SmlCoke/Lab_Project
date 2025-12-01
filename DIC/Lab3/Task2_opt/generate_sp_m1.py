# gen_sp.py
# 
# 本脚本用于生成Task2优化版本（m=1个缓冲反相器）的SPICE仿真文件
# 
# 关键概念：
# - CM (CMulti): 逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数
# - SN, SP: NMOS和PMOS晶体管的尺寸(NFIN参数)
# 
# CM到SN/SP的转换关系（来自Relation.md）：
# - INV:   SN = CM, SP = CM
# - NAND2: SN = CM/1.5*2, SP = CM/1.5  (g = 1.5)
# - NOR2:  SN = CM/1.5, SP = CM/1.5*2  (g = 1.5)
#
from pathlib import Path

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 2: Use Logical Effort to Optimize 4×16 Decoder
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 
.param CM_NAND2 = 1
.param CM_NOR2 = 1
.param CM_buffer_0 = 1

* lib
.include '../../16nfet.pm'
.include '../../16pfet.pm'

* source
Vdd vdd 0 DC 'SUPPLY'
VA3 A3 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)
VA2 A2 0 DC 'SUPPLY'
VA1 A1 0 DC 'SUPPLY'
VA0 A0 0 DC 'SUPPLY'

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

* Sub circuit: 2-NOR
* g = 1.5
* CM到SN/SP转换: SN = CM/1.5, SP = CM/1.5*2
.subckt NOR2 in1 in2 out vdd gnd SN=1 SP=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR2

* Circuit: 4 to 16 decoder
* The first layer is 4 inverters. After this layer, we get 4 outputs
* which are NA3, NA2, NA1, NA0
Xinv31 A3 NA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The second layer is 4 inverters. After this layer, we get 4 outputs
* which are PA3, PA2, PA1, PA0
Xinv32 NA3 PA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 8 outputs
* which is Cartesian Product of (PA3, NA3) with (PA2, NA2) and (PA1, NA1) with (PA0, NA0)
* NAND2: SN_NAND2 = CM_NAND2/1.5*2, SP_NAND2 = CM_NAND2/1.5
.param SN_NAND2 = 'int(CM_NAND2/1.5*2+0.5)'
.param SP_NAND2 = 'int(CM_NAND2/1.5+0.5)'
XNAND2_0 NA1 NA0 NA1_NA0 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_1 NA1 PA0 NA1_PA0 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_2 PA1 NA0 PA1_NA0 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_3 PA1 PA0 PA1_PA0 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_4 NA3 NA2 NA3_NA2 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_5 NA3 PA2 NA3_PA2 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_6 PA3 NA2 PA3_NA2 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'
XNAND2_7 PA3 PA2 PA3_PA2 vdd gnd NAND2 SN="SN_NAND2" SP="SP_NAND2" Lg = '20n'

* The last layer is 16 NOR2 gates. After this layer, we get 16 outputs
* which is A3'A2'A1'A0', A3'A2'A1'A0, to A3A2A1A0
* NOR2: SN_NOR2 = CM_NOR2/1.5, SP_NOR2 = CM_NOR2/1.5*2
.param SN_NOR2 = 'int(CM_NOR2/1.5+0.5)'
.param SP_NOR2 = 'int(CM_NOR2/1.5*2+0.5)'
XNOR2_0  NA3_NA2 NA1_NA0 word_0  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_1  NA3_NA2 NA1_PA0 word_1  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_2  NA3_NA2 PA1_NA0 word_2  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_3  NA3_NA2 PA1_PA0 word_3  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_4  NA3_PA2 NA1_NA0 word_4  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_5  NA3_PA2 NA1_PA0 word_5  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_6  NA3_PA2 PA1_NA0 word_6  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_7  NA3_PA2 PA1_PA0 word_7  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_8  PA3_NA2 NA1_NA0 word_8  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_9  PA3_NA2 NA1_PA0 word_9  vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_10 PA3_NA2 PA1_NA0 word_10 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_11 PA3_NA2 PA1_PA0 word_11 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_12 PA3_PA2 NA1_NA0 word_12 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_13 PA3_PA2 NA1_PA0 word_13 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_14 PA3_PA2 PA1_NA0 word_14 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'
XNOR2_15 PA3_PA2 PA1_PA0 word_15 vdd gnd NOR2 SN="SN_NOR2" SP="SP_NOR2" Lg = '20n'   

* About critical path, we can obviously see that the path which passes 2'inv is the longest.
* Such path has an general feature, it has PA!
* We choose to optimize the path: 
* A3 -> Xinv31 -> NA3 -> Xinv32 -> PA3 -> XNAND2_7 -> PA3_PA2 -> XNOR2_15 -> word_15
* Xinv31: g = 1, b = 1, f = Xinv32_size/Xinv31_size 
* Xinv32: g = 1, b: (XNAND2_7, XNAND2_6), b = 2, f = XNAND2_7_size/Xinv32_size
* XNAND2_7: g = 3/2, b = (XNOR2_12, XNOR2_13, XNOR2_14, XNOR2_15), b= 4, f = XNOR2_15_size/XNAND2_7_size
* XNOR2_15: g = 3/2, b = 1
* Then there are m invs, g = 1, b = 1, f = ratio of size stage by stage
* G = 1 * 3/2 *3/2 * 1... = 9/4, B = 8, F = 128  
* H = 2304
* D = NH^(1/N) + p(Xinv32)(=1) + p(XNAND2_7) + p(XNOR2_15) + p(m*inv)
* D = (m+3)2304^[1/(m+3)] + 1 + 2 + 2 + m = (m+3)2304**[1/(m+3)] + m + 5 = NH**(1/N) + N + 1
* solve critical point of NH**(1/N) + N + 1
* N = 6.05, hopt = 3.59

* Buffer inverter (m=1)
* INV: SN = SP = CM
Xinv_buffer_0 word_15 buffer_out_0 vdd gnd INV SN='CM_buffer_0' SP='CM_buffer_0' Lg = '20n'
Xinv_load buffer_out_0 load_out vdd gnd INV SN='128' SP='128' Lg = '20n'

{sweepdata}

.tran 1p 20n sweep data = sweepdata 
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_0) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_0) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end
"""

def load_parameter_lists():
    """
    生成参数扫描列表，在最优值附近进行精细扫描
    
    注意：这里扫描的是CM（输入栅电容倍数），不是直接的晶体管尺寸
    SPICE中会通过.param语句自动计算对应的SN和SP
    
    最优值参考（基于CM）：
    - CM_NAND2 = 3 (小值，步长±1)
    - CM_NOR2 = 4 (小值，步长±1)
    - CM_buffer_0 = 18 (中等值，步长±2)
    """
    # 最优值中心点（使用CM）
    center = {
        'CM_NAND2': 3,
        'CM_NOR2': 4,
        'CM_buffer_0': 18,
    }
    
    # 定义每个参数的扫描范围和步长
    # 格式：参数名: (中心值, 扫描半径, 步长)
    scan_config = {
        'CM_NAND2': (center['CM_NAND2'], 1, 1),      # 3±1, 步长1 -> [2, 3, 4]
        'CM_NOR2': (center['CM_NOR2'], 1, 1),        # 4±1, 步长1 -> [3, 4, 5]
        'CM_buffer_0': (center['CM_buffer_0'], 4, 2),  # 18±4, 步长2 -> [14, 16, 18, 20, 22]
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
    for cm_nand2 in param_ranges['CM_NAND2']:
        for cm_nor2 in param_ranges['CM_NOR2']:
            for cm_buf0 in param_ranges['CM_buffer_0']:
                parameter_lists.append({
                    'CM_NAND2': cm_nand2,
                    'CM_NOR2': cm_nor2,
                    'CM_buffer_0': cm_buf0
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
    sweepdata_content = [".data sweepdata CM_NAND2 CM_NOR2 CM_buffer_0 \n"]
    for i, param_dict in enumerate(parameter_lists, 1):
        sweepdata_content.append(f"+ {param_dict['CM_NAND2']} {param_dict['CM_NOR2']} {param_dict['CM_buffer_0']}\n")
    sweepdata_content.append(".enddata\n")
    
    sweepdata_content = "".join(sweepdata_content)
    content = TEMPLATE_TOP.format(sweepdata=sweepdata_content)
    file_name = f"task2_s_opt_m1.sp"
    path_sp = Path(outdir) / file_name
    path_sp.write_text(content, encoding='utf-8')
    print(f"Generated {file_name}")

if __name__ == '__main__':
    GenSpiceScripts()