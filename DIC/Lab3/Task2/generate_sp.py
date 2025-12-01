# gen_sp.py
# 
# 本脚本用于生成Task2 4x16译码器的SPICE仿真文件
# 
# 关键概念：
# - CM (CMulti): 逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数
# - SN, SP: NMOS和PMOS晶体管的尺寸(NFIN参数)
# 
# CM到SN/SP的转换关系（来自Relation.md）：
# - INV:   SN = CM, SP = CM
# - NAND2: SN = CM/1.5*2, SP = CM/1.5  (g = 1.5)
# - NOR2:  SN = CM/1.5, SP = CM/1.5*2  (g = 1.5)
# - NAND3: SN = CM/2*3, SP = CM/2      (g = 2)
# - NOR3:  SN = CM/2, SP = CM/2*3      (g = 2)
#
import argparse
from opt import f
from pathlib import Path

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 2: Use Logical Effort to Optimize 4×16 Decoder
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
* NAND2: CM_NAND2 -> SN_NAND2 = CM_NAND2/1.5*2, SP_NAND2 = CM_NAND2/1.5
XNAND2_0 NA1 NA0 NA1_NA0 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_1 NA1 PA0 NA1_PA0 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_2 PA1 NA0 PA1_NA0 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_3 PA1 PA0 PA1_PA0 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_4 NA3 NA2 NA3_NA2 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_5 NA3 PA2 NA3_PA2 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_6 PA3 NA2 PA3_NA2 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'
XNAND2_7 PA3 PA2 PA3_PA2 vdd gnd NAND2 SN="{SN_NAND2}" SP="{SP_NAND2}" Lg = '20n'

* The last layer is 16 NOR2 gates. After this layer, we get 16 outputs
* which is A3'A2'A1'A0', A3'A2'A1'A0, to A3A2A1A0
* NOR2: CM_NOR2 -> SN_NOR2 = CM_NOR2/1.5, SP_NOR2 = CM_NOR2/1.5*2
XNOR2_0  NA3_NA2 NA1_NA0 word_0  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_1  NA3_NA2 NA1_PA0 word_1  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_2  NA3_NA2 PA1_NA0 word_2  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_3  NA3_NA2 PA1_PA0 word_3  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_4  NA3_PA2 NA1_NA0 word_4  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_5  NA3_PA2 NA1_PA0 word_5  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_6  NA3_PA2 PA1_NA0 word_6  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_7  NA3_PA2 PA1_PA0 word_7  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_8  PA3_NA2 NA1_NA0 word_8  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_9  PA3_NA2 NA1_PA0 word_9  vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_10 PA3_NA2 PA1_NA0 word_10 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_11 PA3_NA2 PA1_PA0 word_11 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_12 PA3_PA2 NA1_NA0 word_12 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_13 PA3_PA2 NA1_PA0 word_13 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_14 PA3_PA2 PA1_NA0 word_14 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'
XNOR2_15 PA3_PA2 PA1_PA0 word_15 vdd gnd NOR2 SN="{SN_NOR2}" SP="{SP_NOR2}" Lg = '20n'   

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
{instance_lines}

.tran 1p 20n 
.probe V(*) I(*)
{measure_lines}
.measure tran tp param='(tpLH+tpHL)/2'
.end
"""

# =============================================================================
# CM到SN/SP转换函数
# 根据Relation.md中的对应关系，将CM（输入栅电容倍数）转换为SN和SP（晶体管尺寸）
# =============================================================================

def cm_to_sn_sp_inv(cm):
    """
    INV: SN = SP = CM
    """
    sn = cm
    sp = cm
    return sn, sp

def cm_to_sn_sp_nand2(cm):
    """
    NAND2: g = 1.5
    SN = CM/1.5*2 = CM*4/3
    SP = CM/1.5 = CM*2/3
    """
    sn = cm / 1.5 * 2
    sp = cm / 1.5
    return sn, sp

def cm_to_sn_sp_nor2(cm):
    """
    NOR2: g = 1.5
    SN = CM/1.5 = CM*2/3
    SP = CM/1.5*2 = CM*4/3
    """
    sn = cm / 1.5
    sp = cm / 1.5 * 2
    return sn, sp

# =============================================================================
# accurate的意思是，精确计算每个器件的尺寸和等效扇出，然后实际应用时再取整(四舍五入)，
# 一定程度上防止向下取整的误差累计
# 
# 注意：这里计算的是CM（输入栅电容倍数），然后通过转换函数得到SN和SP
# =============================================================================
def load_parameter_accurate(m):
    """
    生成参数配置
    
    参数:
        m: 缓冲反相器的数量
        
    返回:
        CM_NAND2: NAND2的输入栅电容倍数
        SN_NAND2, SP_NAND2: NAND2的晶体管尺寸
        CM_NOR2: NOR2的输入栅电容倍数  
        SN_NOR2, SP_NOR2: NOR2的晶体管尺寸
        以及其他信息
    """
    # generate instance lines up to m, m refers to the number of buffers(1 buffer = 1 inverter)
    hopt = 2304**(1/(m+3))
    
    # 计算NAND2的CM（输入栅电容倍数）
    # Xinv32的等效扇出 = hopt/g/b = hopt/1/2
    Xinv2_f = hopt/1/2
    CM_NAND2 = Xinv2_f  # NAND2的输入栅电容 = Xinv32的尺寸 * 等效扇出 = 1 * f = f
    
    # 将CM_NAND2转换为SN和SP
    SN_NAND2_raw, SP_NAND2_raw = cm_to_sn_sp_nand2(CM_NAND2)
    SN_NAND2 = max(1, int(SN_NAND2_raw + 0.5))  # 四舍五入取整，最小为1
    SP_NAND2 = max(1, int(SP_NAND2_raw + 0.5))
    
    # 计算NOR2的CM（输入栅电容倍数）
    # NAND2的等效扇出 = hopt/g/b = hopt/(3/2)/4
    XNAND2_f = hopt/(3/2)/4
    CM_NOR2 = XNAND2_f * CM_NAND2  # NOR2的输入栅电容 = NAND2的CM * 等效扇出
    
    # 将CM_NOR2转换为SN和SP
    SN_NOR2_raw, SP_NOR2_raw = cm_to_sn_sp_nor2(CM_NOR2)
    SN_NOR2 = max(1, int(SN_NOR2_raw + 0.5))
    SP_NOR2 = max(1, int(SP_NOR2_raw + 0.5))

    # 计算第一级缓冲反相器的尺寸
    # NOR2的等效扇出 = hopt/g/b = hopt/(3/2)/1
    XNOR2_f = hopt/(3/2)/1
    X_inv_buffer_0_size = XNOR2_f * CM_NOR2  # 缓冲反相器的输入栅电容 = NOR2的CM * 等效扇出
    
    if (m==0):
        inst_lines = ["Xinv_load word_15 load_out vdd gnd INV SN='128' SP='128' Lg = '20n'"]
        all_fs = [Xinv2_f, XNAND2_f, XNOR2_f]
        all_cms = [1, CM_NAND2, CM_NOR2]
        all_cms_for_use = [1, CM_NAND2, CM_NOR2]
        return (CM_NAND2, SN_NAND2, SP_NAND2, CM_NOR2, SN_NOR2, SP_NOR2, 
                all_fs, all_cms, all_cms_for_use, '\n'.join(inst_lines), 
                ".measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V(word_15) = '0.5*SUPPLY' RISE = 4\n.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V(word_15) = '0.5*SUPPLY' FALL = 4\n")

    buffer_inv_fs = [hopt/1/1]  # 存储所有缓冲反相器的等效扇出
    buffer_inv_sizes = [X_inv_buffer_0_size]  # 存储所有缓冲反相器的尺寸（即CM，因为INV的SN=SP=CM）
    inst_lines = []  # 存储sp语句
    
    # 对于INV，SN = SP = CM，所以直接用size
    buffer_0_size_int = max(1, int(X_inv_buffer_0_size + 0.5))
    inst_lines.append(f"Xinv_buffer_0 word_15 buffer_out_0 vdd gnd INV SN='{buffer_0_size_int}' SP='{buffer_0_size_int}' Lg = '20n'")

    buffer_inv_size_for_use = []  # 存储实际用到的缓冲反相器尺寸，因为要取整
    buffer_inv_size_for_use.append(buffer_0_size_int)

    last_node = ["buffer_out_0"]

    for i in range(m-1):
        buffer_inv_size = buffer_inv_sizes[-1] * buffer_inv_fs[-1]  # 先计算当前缓冲反相器的尺寸
        f_val = hopt/1/1  # 计算当前缓冲反相器的等效扇出
        buffer_inv_fs.append(f_val)
        buffer_inv_sizes.append(buffer_inv_size)
        buffer_size_int = max(1, int(buffer_inv_size + 0.5))
        inst_lines.append(f"Xinv_buffer_{i+1} buffer_out_{i} buffer_out_{i+1} vdd gnd INV SN='{buffer_size_int}' SP='{buffer_size_int}' Lg = '20n'")

        buffer_inv_size_for_use.append(buffer_size_int)
        last_node.append(f"buffer_out_{i+1}")

    inst_lines.append(f"Xinv_load {last_node[-1]} load_out vdd gnd INV SN='128' SP='128' Lg = '20n'")
    all_fs = [Xinv2_f, XNAND2_f, XNOR2_f] + buffer_inv_fs
    all_cms = [1, CM_NAND2, CM_NOR2] + buffer_inv_sizes
    all_cms_for_use = [1, CM_NAND2, CM_NOR2] + buffer_inv_size_for_use
    
    # 如果all_cms_for_use中由任意一个元素值为0，判定为此种模式不行，因为 Nfin 必须大于 1。
    # 注意：现在我们已经用max(1, ...)确保了最小为1
    if any(size == 0 for size in buffer_inv_size_for_use):
        return None
    
    # 生成测量语句，如果插入反相器级数为偶数，那么输入和输出变化相反，否则相同
    measure_lines = []
    if (m % 2 == 0):
        measure_lines.append(f".measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measure_lines.append(f".measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")
    else:
        measure_lines.append(f".measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' RISE = 4\n")
        measure_lines.append(f".measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V({last_node[-1]}) = '0.5*SUPPLY' FALL = 4\n")
    measure_lines = "".join(measure_lines)

    return (CM_NAND2, SN_NAND2, SP_NAND2, CM_NOR2, SN_NOR2, SP_NOR2,
            all_fs, all_cms, all_cms_for_use, '\n'.join(inst_lines), measure_lines)

def write_for_N(m, outdir='.'):
    """
    生成指定m值的SPICE仿真文件
    
    参数:
        m: 缓冲反相器的数量
        outdir: 输出目录
    """
    result = load_parameter_accurate(m)
    if result is None:
        print(f"Invalid configuration for m={m}, in this case, some gates have 0 Nfins.")
        return
    
    (CM_NAND2, SN_NAND2, SP_NAND2, CM_NOR2, SN_NOR2, SP_NOR2,
     all_fs, all_cms, all_cms_for_use, inst_lines, measure_lines) = result
    
    log_content = f'''
    When num of Inverters is {2*m}:
    hopt = {2304**(1/(m+3))}
    Dmin = {f(m+3)}
    
    NAND2:
      CM_NAND2 (输入栅电容倍数): {CM_NAND2}
      SN_NAND2: {SN_NAND2}
      SP_NAND2: {SP_NAND2}
    
    NOR2:
      CM_NOR2 (输入栅电容倍数): {CM_NOR2}
      SN_NOR2: {SN_NOR2}
      SP_NOR2: {SP_NOR2}
    
    All gate f(from Xinv2): {all_fs}
    All gate CM(from Xinv2): {all_cms}
    All gate CM(for use, from Xinv2): {all_cms_for_use}
    '''
    
    content = TEMPLATE_TOP.format(
        SN_NAND2=SN_NAND2, SP_NAND2=SP_NAND2,
        SN_NOR2=SN_NOR2, SP_NOR2=SP_NOR2,
        instance_lines=inst_lines, measure_lines=measure_lines
    )

    # 自动创建目录并保存脚本
    path_dir = Path(outdir) / f'm={m}'   # 目标文件夹，例如 ./N=4
    path_dir.mkdir(parents=True, exist_ok=True)  # ✅ 自动创建（含父目录）
    path_sp = path_dir / f"task2_m{m}.sp"   # 最终文件路径
    path_log = path_dir / f"task2_m{m}.log"   # 日志文件路径
    path_sp.write_text(content, encoding='utf-8')
    path_log.write_text(log_content, encoding='utf-8')
    print(f"Written {path_log} done!")
    print(f"Written {path_sp} done!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate SPICE netlist and log for a given m.')
    parser.add_argument('--buffer_inv_nums', '-m', type=int, default=6, help='The value of m (default: 6)')
    parser.add_argument('--outdir', '-o', type=str, default='.', help='The output directory (default: .)')
    args = parser.parse_args()
    for i in range(args.buffer_inv_nums):
        write_for_N(i, outdir=args.outdir)
    # write_for_N(0, outdir=".")