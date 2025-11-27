# gen_sp.py
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

* Sub circuit: 2-NOR
.subckt NOR2 in1 in2 out vdd gnd size=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='size'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='size'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='size'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='size'
.ends NOR2

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
XNAND2_0 NA1 NA0 NA1_NA0 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_1 NA1 PA0 NA1_PA0 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_2 PA1 NA0 PA1_NA0 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_3 PA1 PA0 PA1_PA0 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_4 NA3 NA2 NA3_NA2 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_5 NA3 PA2 NA3_PA2 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_6 PA3 NA2 PA3_NA2 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_7 PA3 PA2 PA3_PA2 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'

* The last layer is 16 NOR2 gates. After this layer, we get 16 outputs
* which is A3'A2'A1'A0', A3'A2'A1'A0, to A3A2A1A0
.param y = 1
XNOR2_0  NA3_NA2 NA1_NA0 word_0  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_1  NA3_NA2 NA1_PA0 word_1  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_2  NA3_NA2 PA1_NA0 word_2  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_3  NA3_NA2 PA1_PA0 word_3  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_4  NA3_PA2 NA1_NA0 word_4  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_5  NA3_PA2 NA1_PA0 word_5  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_6  NA3_PA2 PA1_NA0 word_6  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_7  NA3_PA2 PA1_PA0 word_7  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_8  PA3_NA2 NA1_NA0 word_8  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_9  PA3_NA2 NA1_PA0 word_9  vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_10 PA3_NA2 PA1_NA0 word_10 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_11 PA3_NA2 PA1_PA0 word_11 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_12 PA3_PA2 NA1_NA0 word_12 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_13 PA3_PA2 NA1_PA0 word_13 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_14 PA3_PA2 PA1_NA0 word_14 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'
XNOR2_15 PA3_PA2 PA1_PA0 word_15 vdd gnd NOR2 size = "{XNOR2_size}" Lg = '20n'   

* About critical path, we can obviously see that the path which passes 2'inv is the longest.
* Such path has an general feature, it has PA!
* We choose to optimize the path: 
* A3 -> Xinv31 -> NA3 -> Xinv32 -> PA3 -> XNAND2_7 -> PA3_PA2 -> XNOR2_15 -> word_15
* Xinv31: g = 1, b = 1, f = Xinv32_size/Xinv31_size 
* Xinv32: g = 1, b: (XNAND2_7, XNAND2_6), b = 2, f = XNAND2_7_size/Xinv32_size
* XNAND2_7: g = 3/2, b = (XNOR2_12, XNOR2_13, XNOR2_14, XNOR2_15), b= 4, f = XNOR2_15_size/XNAND2_7_size
* XNOR2_15: g = 3/2, b = 1
* Then there are 2m invs, g = 1, b = 1, f = ratio of size stage by stage
* G = 1 * 3/2 *3/2 * 1... = 9/4, B = 8, F = 128  
* H = 2304
* D = NH^(1/N) + p(Xinv32)(=1) + p(XNAND2_7) + p(XNOR2_15) + p(2m*inv)
* D = (2m+3)2304^[1/(2m+3)] + 1 + 2 + 2 + 2m = (2m+4=3)2304**[1/(2m+3)] + 2m + 5 = NH**(1/N) + N + 1
* solve critical point of NH**(1/N) + N + 1
{instance_lines}

.tran 1p 20n 
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V({output}) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V({output}) = '0.5*SUPPLY' FALL = 4
.measure tran tp param='(tpLH+tpHL)/2'
.end
"""

# accurate的意思是，精确计算每个器件的尺寸和等效扇出，然后实际应用时再取整(四舍五入)，一定程度上防止向下取整的误差累计
def load_parameter_accurate(m):
    # generate instance lines up to m, m refers to the number of buffers(1 buffer = 2 inverter)
    hopt = 2304**(1/(2*m+3))
    Xinv2_f = hopt/1/2 # 先计算inv2等效扇出
    XNAND2_size = Xinv2_f # 然后计算NAND2的尺寸
    
    XNAND2_f = hopt/(3/2)/4   # 先计算NAND2等效扇出
    XNOR2_size = XNAND2_f * XNAND2_size # 然后计算NOR2的尺寸

    XNOR2_f = hopt/(3/2)/1 # 先计算NOR2等效扇出
    X_inv_buffer_0_size = XNOR2_f * XNOR2_size # 然后计算第一级别缓冲反相器的尺寸
    if (m==0):
        inst_lines = ["Xinv_load word_15 load_out vdd gnd INV size = '128' Lg = '20n'"]
        all_fs = [Xinv2_f, XNAND2_f, XNOR2_f]
        all_sizes = [1, XNAND2_size, XNOR2_size]
        all_sizes_for_use = [1, int(XNAND2_size+0.5), int(XNOR2_size+0.5)]
        return int(XNAND2_size+0.5), int(XNOR2_size+0.5), all_fs, all_sizes, all_sizes_for_use, '\n'.join(inst_lines), "word_15"

    buffer_inv_fs = [hopt/1/1]  # 存储所有缓冲反相器的等效扇出
    buffer_inv_sizes = [X_inv_buffer_0_size] # 存储所有缓冲反相器的尺寸
    inst_lines = [] # 存储sp语句
    inst_lines.append(f"Xinv_buffer_0 word_15 buffer_out_0 vdd gnd INV size = '{int(X_inv_buffer_0_size+0.5)}' Lg = '20n'") # 尺寸必须是整数，这里我们直接向下取整

    buffer_inv_size_for_use = [] # 存储实际用到的缓冲反相器尺寸，因为要取整
    buffer_inv_size_for_use.append(int(X_inv_buffer_0_size+0.5))

    last_node = ["buffer_out_0"]
    for i in range(2*m-1):
        buffer_inv_size = buffer_inv_sizes[-1] * buffer_inv_fs[-1] # 先计算当前缓冲反相器的尺寸
        f = hopt/1/1 # 计算当前缓冲反相器的等效扇出
        buffer_inv_fs.append(f)
        buffer_inv_sizes.append(buffer_inv_size)
        inst_lines.append(f"Xinv_buffer_{i+1} buffer_out_{i} buffer_out_{i+1} vdd gnd INV size = '{int(buffer_inv_size+0.5)}' Lg = '20n'") # 尺寸必须是整数，这里我们直接向下取整

        buffer_inv_size_for_use.append(int(buffer_inv_size+0.5))
        last_node.append(f"buffer_out_{i+1}")

    inst_lines.append(f"Xinv_load {last_node[-1]} load_out vdd gnd INV size = '128' Lg = '20n'")
    all_fs = [Xinv2_f, XNAND2_f, XNOR2_f] + buffer_inv_fs
    all_sizes = [1, XNAND2_size, XNOR2_size] + buffer_inv_sizes
    all_sizes_for_use = [1, int(XNAND2_size+0.5), int(XNOR2_size+0.5)] + buffer_inv_size_for_use
    # 如果all_sizes_for_use中由任意一个元素值为0，判定为此种模式不行，因为 Nfin 必须大于 1。
    if any(size == 0 for size in all_sizes_for_use):
        return None
    return int(XNAND2_size+0.5), int(XNOR2_size+0.5), all_fs, all_sizes, all_sizes_for_use, '\n'.join(inst_lines), last_node[-1]

def write_for_N(m, outdir='.'):
    if (load_parameter_accurate(m) is None):
        print(f"Invalid configuration for m={m}, in this case, some gates have 0 Nfins.")
        return
    XNAND2_size, XNOR2_size, all_fs, all_sizes, all_sizes_for_use, inst_lines, output = load_parameter_accurate(m)
    log_content = f'''
    When num of Inverters is {2*m}:
    hopt = {2304**(1/(2*m+3))}
    Dmin = {f(2*m+3)}
    XNAND2_size: {XNAND2_size}
    XNOR2_size: {XNOR2_size}
    All gate f(from Xinv2): {all_fs}
    All gate sizes(from Xinv2): {all_sizes}
    All gate sizes(for use, from Xinv2): {all_sizes_for_use}
    '''
    content = TEMPLATE_TOP.format(XNAND2_size = XNAND2_size, XNOR2_size = XNOR2_size, instance_lines=inst_lines, output=output)

    # 自动创建目录并保存脚本
    path_dir = Path(outdir) / f'm={m}'   # 目标文件夹，例如 ./N=4
    path_dir.mkdir(parents=True, exist_ok=True)  # ✅ 自动创建（含父目录）
    path_sp = path_dir / f"task2_m{m}.sp"   # 最终文件路径
    path_log = path_dir / f"task2_m{m}.log"   # 日志文件路径
    path_sp.write_text(content,encoding='utf-8')
    path_log.write_text(log_content,encoding='utf-8')
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