# gen_sp.py
# 
# 本脚本用于生成Task2二阶段——参数扫描（m=1个缓冲反相器）的SPICE仿真文件
# 
# 
# CM到SN/SP的转换关系（来自Relation.md）：
# - INV:   SN = CM, SP = CM
# - NAND2: SN = CM/1.5*2, SP = CM/1.5  (g = 1.5)
# - NOR2:  SN = CM/1.5, SP = CM/1.5*2  (g = 1.5)
#
from pathlib import Path
import itertools

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 2: Use Logical Effort to Optimize 4×16 Decoder
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 
.param SN_NAND2 = 1
.param SP_NAND2 = 1
.param SN_NOR2 = 1
.param SP_NOR2 = 1
.param SN_buffer_0 = 1
.param SP_buffer_0 = 1
.param SN_buffer_1 = 1
.param SP_buffer_1 = 1
.param SN_buffer_2 = 1
.param SP_buffer_2 = 1
.param SN_buffer_3 = 1
.param SP_buffer_3 = 1

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

* Buffer inverters (m=3)
* INV: SN = SP = CM
Xinv_buffer_0 word_15 buffer_out_0 vdd gnd INV SN="SN_buffer_0" SP="SP_buffer_0" Lg = '20n'
Xinv_buffer_1 buffer_out_0 buffer_out_1 vdd gnd INV SN="SN_buffer_1" SP="SP_buffer_1" Lg = '20n'
Xinv_buffer_2 buffer_out_1 buffer_out_2 vdd gnd INV SN="SN_buffer_2" SP="SP_buffer_2" Lg = '20n'
Xinv_buffer_3 buffer_out_2 buffer_out_3 vdd gnd INV SN="SN_buffer_3" SP="SP_buffer_3" Lg = '20n'
Xinv_load buffer_out_3 load_out vdd gnd INV SN='128' SP='128' Lg = '20n'

{sweepdata}

.tran 1p 20n sweep data = sweepdata
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_3) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_3) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end

"""

def load_parameter_accurate():
    """
    生成参数扫描列表。
    根据逻辑门类型自动计算匹配的SP尺寸，确保PDN和PUN导通电阻相同。
    配置方式：指定SN变量名、逻辑门类型、SN扫描范围。
    """
    '''
    best value:
    NAND2:
        CM_NAND2 (输入栅电容倍数): 1.511209390509403
        SN_NAND2 (NMOS尺寸): 2
        SP_NAND2 (PMOS尺寸): 1

    NOR2:
        CM_NOR2 (输入栅电容倍数): 0.7612512739879339
        SN_NOR2 (NMOS尺寸): 1
        SP_NOR2 (PMOS尺寸): 1

    反相器链：
        缓冲反相器数量 m: 4
        缓冲反相器输入栅电容: [1.5338800983837497, 4.636028017186019, 14.012018148472402, 42.35018681191934]
        缓冲反相器实际用到的尺寸: [2, 5, 14, 42]
    '''
    # 1. 配置区域
    # 格式： "SN变量名": ("逻辑门类型", [SN扫描值列表])
    # 程序会自动推导对应的 SP变量名 (将SN替换为SP)
    # 支持的逻辑门类型: INV, NAND2, NOR2, NAND3, NOR3
    gate_configs = {
        "SN_NAND2": ("NAND2", [1, 2, 3]), 
        "SN_NOR2": ("NOR2", [1, 2]),
        "SN_buffer_0": ("INV",   [1, 2, 3]),
        "SN_buffer_1": ("INV",   [4, 5, 6]),
        "SN_buffer_2": ("INV",   [12, 14, 16]),
        "SN_buffer_3": ("INV",   [40, 42, 44]),
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
    """
    生成SPICE仿真脚本
    """

    sweepdata_content = load_parameter_accurate()
    content = TEMPLATE_TOP.format(sweepdata=sweepdata_content)
    file_name = f"task2_s_opt_m4.sp"
    path_sp = Path(outdir) / file_name
    path_sp.write_text(content, encoding='utf-8')
    print(f"Generated {file_name} !")

if __name__ == '__main__':
    GenSpiceScripts()