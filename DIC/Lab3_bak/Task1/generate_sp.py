# gen_sp.py
import argparse
import itertools 
from pathlib import Path

TEMPLATE_TOP = """*****************************************************
* Lab3 - Task 1: Use Logical Effort to CMulti Gates
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../16nfet.pm'
.include '../16pfet.pm'

* source
Vdd vdd 0 DC 'SUPPLY'
Vpulse vpulse 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)

* 我们认为，所有PMOS的bulk接到vdd，所有NMOS的bulk接到gnd

* Sub circuit: INVerter definition
* SN = SP = CMulti
.subckt INV in out vdd gnd Lg = 20n SN = 1 SP = 1 
Mn out in gnd gnd nfet L='Lg' NFIN ='SN'
Mp out in vdd vdd pfet L='Lg' NFIN ='SP'
.ends INV

* Sub circuit: 3-NAND
* g = 2
* SN = CMulti/2*3
* SP = CMulti/2
.subckt NAND3 in1 in2 in3 out vdd gnd Lg=20n SN = 1 SP = 1 
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='SP'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='SP'
Mp3 out in3 vdd vdd pfet L='Lg' NFIN='SP'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='SN'
Mn2 source1 in2 source2 gnd nfet L='Lg' NFIN='SN'
Mn3 source2 in3 gnd gnd nfet L='Lg' NFIN='SN'
.ends NAND3

* Sub circuit: 2-NOR
* g = 1.5
* SN = CMulti/1.5
* SP = CMulti/1.5*2
.subckt NOR2 in1 in2 out vdd gnd Lg=20n SN = 1 SP = 1
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR2

* Transistor CMulti variable
.param SN_2 = 1
.param SN_3 = 1
.param SN_4 = 1
.param SP_2 = 1
.param SP_3 = 1
.param SP_4 = 1

Xinv1 vpulse inv1_out vdd gnd INV CMulti = 1 Lg = 'Lg'
Xnand3 inv1_out vdd vdd nand3_out vdd gnd NAND3 SN='SN_2' SP = 'SP_2' Lg = 'Lg'
Xnor2 nand3_out gnd nor2_out vdd gnd NOR2 SN = 'SN_3' SP = 'SP_3' Lg = 'Lg'
Xinv2 nor2_out inv2_out vdd gnd INV SN = 'SN_4' SP = 'SP_4' Lg = 'Lg'
Xinv_load inv2_out inv_load_out vdd gnd INV CMulti = '64' Lg = 'Lg'


{sweepdata}

.tran 1p 20n sweep data = sweepdata 
.measure tran tpLH TRIG V(vpulse) = '0.5*SUPPLY' RISE = 4 TARG V(inv2_out) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(vpulse) = '0.5*SUPPLY' FALL = 4 TARG V(inv2_out) = '0.5*SUPPLY' FALL = 4
.measure tran tp param='(tpLH+tpHL)/2'

.probe tran V(*) I(*)
.end
"""


# 注：不同逻辑门N管P管尺寸关系：
# INV: SN = SP
# NAND2: SN = 2SP
# NOR2: SP = 2SN
# NAND3: SN = 3SP
# NOR3: SP = 3SN

# accurate的意思是，精确计算每个器件的尺寸，然后实际应用时再取整(四舍五入)，一定程度上防止向下取整的误差累计
def load_parameter_accurate():
    """
    生成参数扫描列表。
    根据逻辑门类型自动计算匹配的SP尺寸，确保PDN和PUN导通电阻相同。
    配置方式：指定SN变量名、逻辑门类型、SN扫描范围。
    """
    '''
    best value:
    NAND3 int:
    SN_2: 6 
    SP_2: 2
    SN_3: 5 
    SP_3: 9
    SN_4: 17 
    SP_4: 17
    '''
    # 1. 配置区域
    # 格式： "SN变量名": ("逻辑门类型", [SN扫描值列表])
    # 程序会自动推导对应的 SP变量名 (将SN替换为SP)
    # 支持的逻辑门类型: INV, NAND2, NOR2, NAND3, NOR3
    gate_configs = {
        "SN_2": ("NAND3", [5, 6, 7]), 
        "SN_3": ("NOR2", [3, 5, 7]),
        "SN_4": ("INV",   [14, 17, 20])
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
        
        # 计算该级逻辑门所有可能的 (SN, SP) 组合
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
    # combinations 的元素结构类似: ((sn2, sp2), (sn3, sp3), (sn4, sp4))
    combinations = list(itertools.product(*stage_combinations))

    # 构造 HSPICE .data 块字符串
    lines = []
    lines.append(f".data sweepdata {' '.join(param_names)}")
    
    for combo in combinations:
        # 展平元组: ((sn2, sp2), (sn3, sp3)) -> (sn2, sp2, sn3, sp3)
        flat_combo = []
        for pair in combo:
            flat_combo.extend(pair)
            
        # 将数字转换为字符串并用空格连接
        line = " ".join(map(str, flat_combo))
        lines.append(line)
        
    lines.append(".enddata")
    
    return "\n".join(lines)

def write_for_N(outdir='.'):
    # 注意：由于 load_parameter_accurate 返回值已更改为字符串，
    # 此处的调用逻辑需要适配 Task1 的模板。
    # Task1 的模板只需要填充 sweepdata，不需要 Task2 那样的复杂参数。
    
    sweep_data_str = load_parameter_accurate()
    
    # 填充模板
    # 注意：TEMPLATE_TOP 中包含 {sweepdata} 占位符
    content = TEMPLATE_TOP.format(sweepdata=sweep_data_str)

    # 自动创建目录并保存脚本
    path_dir = Path(outdir)
    path_dir.mkdir(parents=True, exist_ok=True)
    
    path_sp = path_dir / "task1.sp" 
    path_sp.write_text(content, encoding='utf-8')
    
    print(f"Generated {len(sweep_data_str.splitlines())-2} combinations.")
    print(f"Written {path_sp} done!")

if __name__ == '__main__':
    write_for_N(outdir='.')
    