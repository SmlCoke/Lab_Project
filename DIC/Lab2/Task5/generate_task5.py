# gen_task5_sp.py
from pathlib import Path

TEMPLATE_TOP = """*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = {N}
*****************************************************
.option post=2
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n

.include '../../16nfet.pm'
.include '../../16pfet.pm'

.subckt inv in out vdd gnd nfin=1
Mn out in gnd gnd nfet L='Lg' NFIN='nfin'
Mp out in vdd vdd pfet L='Lg' NFIN='nfin'
.ends inv

Vdd vdd 0 DC 'SUPPLY'
Vin in 0 PULSE (0 'SUPPLY' 400p 25p 25p 400p 800p)

* Chain instances (1x then stages 2..N, then load 256x)
{instances}

* load
XinvL inv{N}_out invL_out vdd 0 inv nfin=256


.tran 1p 10n

{measures}

.probe V(*) I(*)
.end
"""

def gen_instances_and_measures(N):
    # generate instance lines up to N, and final load node invL_out connected to invN_out
    inst_lines = []
    measures = []
    # first stage
    inst_lines.append("Xinv1 in inv1_out vdd 0 inv nfin=1")
    best_fin = 256**(1/N)
    for i in range(2, N+1):
        prev = f"inv{i-1}_out"
        cur = f"inv{i}_out"
        nfin = int(best_fin**(i-1))
        inst_lines.append(f"Xinv{i} {prev} {cur} vdd 0 inv nfin='{nfin}'")

    # generate measure statements tp1..tpN
    # measure each stage delay (input->stage1, stage1->stage2, ...)
    measures.append(".measure tran tpLH1 TRIG V(in) VAL='0.5*SUPPLY' FALL=2 TARG V(inv1_out) VAL='0.5*SUPPLY' RISE=2")
    measures.append(".measure tran tpHL1 TRIG V(in) VAL='0.5*SUPPLY' RISE=2 TARG V(inv1_out) VAL='0.5*SUPPLY' FALL=2")
    measures.append(".measure tran tp1 PARAM='(tpLH1+tpHL1)/2'")
    for k in range(2, N+1):
        trg = f"inv{k-1}_out"
        targ = f"inv{k}_out"
        measures.append(f".measure tran tpLH{k} TRIG V({trg}) VAL='0.5*SUPPLY' FALL=2 TARG V({targ}) VAL='0.5*SUPPLY' RISE=2")
        measures.append(f".measure tran tpHL{k} TRIG V({trg}) VAL='0.5*SUPPLY' RISE=2 TARG V({targ}) VAL='0.5*SUPPLY' FALL=2")
        measures.append(f".measure tran tp{k} PARAM='(tpLH{k}+tpHL{k})/2'")

    # tp_total sum
    summands = '+'.join([f"tp{i}" for i in range(1, N+1)])
    measures.append(f".measure tran tp_total PARAM='{summands}'")
    return '\n'.join(inst_lines), '\n'.join(measures)

def write_for_N(N, outdir='.'):
    instances, measures = gen_instances_and_measures(N)
    content = TEMPLATE_TOP.format(N=N, instances=instances, measures=measures)
    
    # 自动创建目录并保存脚本
    path_dir = Path(outdir) / f'N={N}'   # 目标文件夹，例如 ./N=4
    path_dir.mkdir(parents=True, exist_ok=True)  # ✅ 自动创建（含父目录）
    path = path_dir / f"task5_N{N}.sp"   # 最终文件路径
    path.write_text(content)
    print(f"Written {path} done!")

if __name__ == '__main__':
    for N in range(1, 10):   # generate for N=2..6
        write_for_N(N, outdir='.')
