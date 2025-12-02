import sys
import sa_core
import argparse
from dataclasses import dataclass
from typing import List, Optional, Tuple

# fj_pro: 强制标准输出使用 utf-8，解决重定向乱码问题
sys.stdout.reconfigure(encoding='utf-8') 



## 类型和数据结构
# 表示引脚的编号列表，每个元素是一个 net 在 nets 数组中的索引。
Pins = List[int]
# 表示所有 net 的名字数组，例如 ["IN", "OUT", "VDD", "VSS", ...]。
Nets = List[str]
# 表示一个 MOS 晶体管或一个 finger：
@dataclass
class Mos:
    name: str
    id: int # 在当前 PMOS 或 NMOS 列表里的编号（0,1,2,...），用于在数组中定位和更新
    x: int # 在布局中所在列的坐标（列索引），初始化为 -1，布局完成后填上
    s: int
    g: int
    d: int
    w: int # 器件宽度（整数形式，单位是 nm 类似）
    
    
    
## 网表读取相关
# 从 SPICE 文件 cells 里，读取指定 .SUBCKT <cell> ... .ENDS 这一段
def read_cell(cells, cell):
    result = []
    in_block = False

    f = open(cells, "r")
    print("[read_cell] 打开网表文件:", cells)
    for line in f:
        line = line.strip("\n")
        if line == "":
            parts = [""]
        else:
            parts = line.split(" ")

        if len(parts) > 1 and parts[0] == ".SUBCKT" and parts[1] == cell:
            in_block = True
            print("[read_cell] 找到 .SUBCKT:", parts)
            result.append(parts)
        elif in_block:
            result.append(parts)
            if len(parts) > 0 and parts[0] == ".ENDS":
                print("[read_cell] 找到 .ENDS，子电路读取结束")
                f.close()
                print("[read_cell] 子电路内容行数:", len(result))
                return result

    f.close()
    print("[read_cell] 未找到指定 cell，返回结果行数:", len(result))
    return result

## 文件输出 / JSON 输出
def write_to_file(filename, s):
    print("[write_to_file] 写入文件:", filename)
    print("[write_to_file] 写入内容长度:", len(s))
    f = open(filename, "w", encoding="utf-8")
    f.write(s)
    f.close()

def mos_str(tp: bool, nets: Nets, mos: Mos) -> str:
    f = "1" if tp else "0"
    s = (
        f"        \"{mos.name}\": {{\n"
        f"            \"x\": \"{mos.x}\",\n"
        f"            \"y\": \"{f}\",\n"
        f"            \"source\": \"{nets[mos.s]}\",\n"
        f"            \"gate\": \"{nets[mos.g]}\",\n"
        f"            \"drain\": \"{nets[mos.d]}\",\n"
        f"            \"width\": \"{mos.w}\"\n"
        f"        }},\n"
    )
    return s

def mos_ary_str_prime(tp: bool, nets: Nets, mos_lst: List[Mos]) -> str:
    res = "".join(mos_str(tp, nets, m) for m in mos_lst)
    return res

def mos_ary_str(pmos_ary: List[Mos], nmos_ary: List[Mos], net_ary: Nets) -> str:
    print("[mos_ary_str] PMOS 数量:", len(pmos_ary), "NMOS 数量:", len(nmos_ary))
    p_str = mos_ary_str_prime(True, net_ary, pmos_ary)
    n_str = mos_ary_str_prime(False, net_ary, nmos_ary)
    all_str = p_str + n_str
    print("[mos_ary_str] 合并后总长度:", len(all_str))
    return all_str

# 生成最终写入文件的 JSON
def placement_str(pmos_ary: List[Mos], nmos_ary: List[Mos], net_ary: Nets) -> str:
    def remove_last_char(s: str) -> str:
        return s[:-2] if len(s) > 2 else ""

    print("[placement_str] 进入 placement_str")
    mos_body = mos_ary_str(pmos_ary, nmos_ary, net_ary)
    body = remove_last_char(mos_body)
    json_text = "{\n    \"placement\": {\n" + body + "\n    }\n}\n"
    return json_text



## 从 .SUBCKT 里提取 pin/net 和 MOS 列表
def pro_head(arr: List[List[str]]) -> List[str]:
    head = arr[0]
    lst: List[str] = []
    for i in range(2, len(head)):
        lst.append(head[i])
    print("[pro_head] pins:", lst)
    return lst

# 用一行器件描述，补充 net 名列表
def pro_row(arr: List[str], lst: List[str]) -> List[str]:
    print("[pro_row] 输入行:", arr)
    print("[pro_row] 进入前 nets 列表:", lst)
    res = lst[:]
    for j in range(1, min(5, len(arr))):
        if arr[j] not in res:
            res.append(arr[j])
    print("[pro_row] 处理后 nets 列表:", res)
    return res

# 对 .SUBCKT 到 .ENDS 之间的每一行调用 pro_row
def pro_middle(arr: List[List[str]], lst: List[str]) -> List[str]:
    res = lst[:]
    for i in range(1, len(arr) - 1):
        res = pro_row(arr[i], res)
    print("[pro_middle] nets:", res)
    return res

# 在 nets 里找名字为 net 的索引
def find_net(nets: Nets, net: str) -> int:
    try:
        return nets.index(net)
    except ValueError:
        return -1

# 把一个总宽度拆成几个 finger 的宽度
def split_width(width: int) -> List[int]:
    res: List[int] = []
    while True:
        if width <= 440:
            if width % 2 == 0:
                if (width // 2) % 5 == 0:
                    res.append(width // 2)
                    res.append(width // 2)
                else:
                    res.append(width // 2 + 3)
                    res.append(width // 2 - 2)
            else:
                res.append(width // 2 + 3)
                res.append(width // 2 - 2)
            break
        else:
            res.append(200)
            width -= 200
    print("[split_width] 拆分结果:", res)
    return res

# 重新给 MOS 列表中的 id 从 0 排到 len(lst)-1
def order_moslst(lst: List[Mos]) -> List[Mos]:
    res: List[Mos] = []
    for i, m in enumerate(lst):
        res.append(Mos(name=m.name, id=i, x=m.x, s=m.s, g=m.g, d=m.d, w=m.w))
    print("[order_moslst] 重新编号后数量:", len(res))
    return res

# 网表初始化函数
def init(s: List[List[str]]) -> Tuple[Pins, List[str], List[Mos], List[Mos], str, int]:
    ss = s
    arr = ss
    filename = arr[0][1]
    print("[init] 处理 cell:", filename)
    pins = pro_head(arr)
    nets = pro_middle(arr, pins)
    print("[init] pins:", pins)
    print("[init] nets:", nets)
    nets_prime = nets[:]
    pins_idx = [find_net(nets_prime, p) for p in pins]

    nlst: List[Mos] = []
    plst: List[Mos] = []
    w_ref = 0

    for i in range(1, len(arr) - 1):
        r = arr[i]
        name = r[0]
        s_net = r[1]
        g_net = r[2]
        d_net = r[3]
        tp = r[5]
        width_field = r[6] if r[6][0] in ("w", "W") else r[7]
        name_clean = name[1:]
        x = -1
        s_idx = find_net(nets_prime, s_net)
        g_idx = find_net(nets_prime, g_net)
        d_idx = find_net(nets_prime, d_net)
        tp_bool = False if tp[0] == "n" else True

        float_num = float(width_field[2:-1])
        if width_field[-1] == "u":
            int_num = int(float_num * 1000.0)
        else:
            int_num = int(float_num)

        mos_split = split_width(int_num) if int_num >= 240 else [int_num]

        mos_list: List[Mos] = []
        for idx, w in enumerate(mos_split):
            if idx == 0:
                mname = name_clean
            else:
                mname = f"{name_clean}_finger{idx}"
            mos_list.append(Mos(name=mname, id=-1, x=x, s=s_idx, g=g_idx, d=d_idx, w=w))

        if not tp_bool:
            nlst.extend(mos_list)
        else:
            plst.extend(mos_list)

        w_ref += (int_num + 199) // 220
        print("[init] 行", i, "name=", name, "tp_bool=", tp_bool, "int_num=", int_num, "拆分个数=", len(mos_list))

    nmos_ordered = order_moslst(nlst)
    pmos_ordered = order_moslst(plst)
    print("[init] 最终 NMOS 数量:", len(nmos_ordered))
    print("[init] 最终 PMOS 数量:", len(pmos_ordered))
    print("[init] w_ref =", w_ref)
    return pins_idx, nets, nmos_ordered, pmos_ordered, filename, w_ref



## 布置前的辅助函数（init_layout 用）
def convert_to_mos(mos_op: Optional[Mos]) -> Mos:
    if mos_op is not None:
        return mos_op
    return Mos(name="NULL", id=-1, x=-1, s=-1, g=-1, d=-1, w=0)

# 用在布置时，避免一开始就形成notch
def check_notch_init(mos_place: List[Optional[Mos]], new_mos: Mos) -> bool:
    if len(mos_place) < 2:
        return False
    mos1 = mos_place[-2]
    mos2 = mos_place[-1]
    if mos1 is not None and mos2 is not None:
        if convert_to_mos(mos1).w > convert_to_mos(mos2).w and new_mos.w > convert_to_mos(mos2).w:
                print("[check_notch_init] 发现 notch 风险, new_mos=", new_mos.name)
                return True
    return False

# 根据一行的 place 阵列（包含 None 和 Mos），更新 mos_ary 中每个 MOS 的 x
def update_mos_ary(mos_ary: List[Mos], mos_place: List[Optional[Mos]]) -> None:
    for i, maybe_m in enumerate(mos_place):
        if maybe_m is not None:
            mos = convert_to_mos(maybe_m)
            mos_ary[mos.id] = Mos(
                name=mos.name,
                id=mos.id,
                x=i,
                s=mos.s,
                g=mos.g,
                d=mos.d,
                w=mos.w,
            )
    print("[update_mos_ary] 已根据 place 更新 mos_ary")

# 在列表前面插 None，直到总长度等于 length
def complete_lst(lst: List[Optional[Mos]], length: int) -> List[Optional[Mos]]:
    none_lst: List[Optional[Mos]] = []
    while len(none_lst) + len(lst) < length:
        none_lst.insert(0, None)
    res = lst + none_lst
    print("[complete_lst] 原长度:", len(lst), "目标长度:", length, "结果长度:", len(res))
    return res

# 删除数组中索引 pos 这一列，返回新列表
def ary_drop(ary: List[Optional[Mos]], pos: int) -> List[Optional[Mos]]:
    res = ary[:pos] + ary[pos + 1 :]
    print("[ary_drop] 删除位置:", pos, "原长度:", len(ary), "新长度:", len(res))
    return res

# 在一整行里检查是否有 notch 形状
def check_notch(place_ary: List[Optional[Mos]]) -> bool:
    pre_width = 0
    for i in range(len(place_ary) - 1):
        cur = place_ary[i]
        if cur is None:
            pre_width = 0
            continue
        cur_w = convert_to_mos(cur).w
        next_w = convert_to_mos(place_ary[i + 1]).w if place_ary[i + 1] is not None else 0
        if pre_width > cur_w and cur_w < next_w:
            print("[check_notch] 检测到 notch 违例, 位置:", i)
            return False
        pre_width = cur_w
    return True

# 尝试删掉左右电连接都安全的“全空列
def update_place_ary(pp_ary: List[Optional[Mos]], np_ary: List[Optional[Mos]]) -> Tuple[List[Optional[Mos]], List[Optional[Mos]]]:
    i = 0
    while i < len(pp_ary):
        pmos = pp_ary[i]
        nmos = np_ary[i]
        left_pmos = pp_ary[i - 1] if i > 0 else None
        left_nmos = np_ary[i - 1] if i > 0 else None
        right_pmos = pp_ary[i + 1] if i + 1 < len(pp_ary) else None
        right_nmos = np_ary[i + 1] if i + 1 < len(np_ary) else None

        if (
            pmos is None
            and nmos is None
            and (left_pmos is None or right_pmos is None or convert_to_mos(left_pmos).d == convert_to_mos(right_pmos).s)
            and (left_nmos is None or right_nmos is None or convert_to_mos(left_nmos).d == convert_to_mos(right_nmos).s)
        ):
            new_pp = ary_drop(pp_ary, i)
            new_np = ary_drop(np_ary, i)
            if check_notch(new_pp) and check_notch(new_np):
                pp_ary = new_pp
                np_ary = new_np
                continue
        i += 1
    print("[update_place_ary] 处理完空列, 最终长度:", len(pp_ary))
    return pp_ary, np_ary



## 初始布局生成
# 根据 PMOS/NMOS 列表生成一个合法的初始两行布局
def init_layout(pmos: List[Mos], nmos: List[Mos]) -> Tuple[List[Mos], List[Mos], List[Optional[Mos]], List[Optional[Mos]]]:
    pmos_ary = list(pmos)
    nmos_ary = list(nmos)
    mos_num = 2 * max(len(pmos), len(nmos))
    print("[init_layout] 输入 PMOS 数量:", len(pmos), "NMOS 数量:", len(nmos), "mos_num =", mos_num)

    def is_empty(lst: List[Mos]) -> bool:
        return len(lst) == 0

    def place(plst, nlst, pp, np, st):
        nonlocal pmos_ary, nmos_ary
        pp_len = len(pp)
        np_len = len(np)
        pp_ary = list(reversed(pp))
        np_ary = list(reversed(np))

        if not is_empty(plst) or not is_empty(nlst):
            if st:  # place pmos
                pmos_hd = plst[0]
                pre_pmos = convert_to_mos(pp[0])
                if pp[0] is None or pre_pmos.d == pmos_hd.s:
                    if (
                        pp_len >= np_len
                        or (np_len - pp_len == 2 and np_ary[pp_len] is None)
                        or (np_len - pp_len == 1 and pmos_hd.g == convert_to_mos(np_ary[pp_len]).g)
                    ):
                        if not check_notch_init(pp_ary, pmos_hd):
                            return place(plst[1:], nlst, [pmos_hd] + pp, np, st if is_empty(nlst) else (not st))
                        else:
                            return place(plst[1:], nlst, [pmos_hd, None] + pp, np, st if is_empty(nlst) else (not st))
                    else:
                        if np_len - pp_len == 2:
                            return place(plst[1:], nlst, [pmos_hd, None, None] + pp, np, st if is_empty(nlst) else (not st))
                        else:
                            return place(plst[1:], nlst, [pmos_hd, None] + pp, np, st if is_empty(nlst) else (not st))
                else:
                    if pp_len >= np_len or np_len - pp_len == 1:
                        return place(plst[1:], nlst, [pmos_hd, None] + pp, np, st if is_empty(nlst) else (not st))
                    else:
                        if pmos_hd.g == convert_to_mos(np[0]).g:
                            return place(plst[1:], nlst, [pmos_hd, None] + pp, np, st if is_empty(nlst) else (not st))
                        else:
                            return place(plst[1:], nlst, [pmos_hd, None, None] + pp, np, st if is_empty(nlst) else (not st))
            else:  # place nmos
                nmos_hd = nlst[0]
                pre_nmos = convert_to_mos(np[0])
                if np[0] is None or pre_nmos.d == nmos_hd.s:
                    if (
                        np_len >= pp_len
                        or (pp_len - np_len == 2 and pp_ary[np_len] is None)
                        or (pp_len - np_len == 1 and nmos_hd.g == convert_to_mos(pp_ary[np_len]).g)
                    ):
                        if not check_notch_init(np_ary, nmos_hd):
                            return place(plst, nlst[1:], pp, [nmos_hd] + np, st if is_empty(plst) else (not st))
                        else:
                            return place(plst, nlst[1:], pp, [nmos_hd, None] + np, st if is_empty(plst) else (not st))
                    else:
                        if pp_len - np_len == 2:
                            return place(plst, nlst[1:], pp, [nmos_hd, None, None] + np, st if is_empty(plst) else (not st))
                        else:
                            return place(plst, nlst[1:], pp, [nmos_hd, None] + np, st if is_empty(plst) else (not st))
                else:
                    if np_len >= pp_len or pp_len - np_len == 1:
                        return place(plst, nlst[1:], pp, [nmos_hd, None] + np, st if is_empty(plst) else (not st))
                    else:
                        if nmos_hd.g == convert_to_mos(pp[0]).g:
                            return place(plst, nlst[1:], pp, [nmos_hd, None] + np, st if is_empty(plst) else (not st))
                        else:
                            return place(plst, nlst[1:], pp, [nmos_hd, None, None] + np, st if is_empty(plst) else (not st))
        else:
            pmos_place = complete_lst(list(reversed(pp))[1:], mos_num)
            nmos_place = complete_lst(list(reversed(np))[1:], mos_num)
            print("[init_layout] 初始 pmos_place 长度:", len(pmos_place))
            print("[init_layout] 初始 nmos_place 长度:", len(nmos_place))
            pplace_ary, nplace_ary = update_place_ary(pmos_place, nmos_place)
            print("[init_layout] 压缩后 pplace_ary 长度:", len(pplace_ary))
            print("[init_layout] 压缩后 nplace_ary 长度:", len(nplace_ary))
            update_mos_ary(pmos_ary, pmos_place)
            update_mos_ary(nmos_ary, nmos_place)
            print("[init_layout] 完成布局, 返回")
            return pmos_ary, nmos_ary, pplace_ary, nplace_ary

    return place(pmos, nmos, [None], [None], True)


def main() -> None:
    # fj_pro: 将sys.argv修改为更方便的argparse处理，同时加入数据文件
    parser = argparse.ArgumentParser(description="Simulated Annealing Placement Tool")
    parser.add_argument("netlist", help="Path of the netlist file")
    parser.add_argument("cell_name", help="Name of the cell to process")
    parser.add_argument("data_file", help="File to log annealing data")
    parser.add_argument("x_t0", type=int)
    parser.add_argument("z_decrease", type=float)
    parser.add_argument("w_times", type=int)
    args = parser.parse_args()
    cells = args.netlist
    cell = args.cell_name
    data_file = args.data_file
    x_t0 = args.x_t0
    z_decrease = args.z_decrease
    w_times = args.w_times

    # args = sys.argv[1:]
    # if len(args) < 2 or len(args) > 3: # fj_pro: 支持可选的第三个参数 data_file, 且该参数可选。用于记录退火过程分数数据
    #     print("Usage: python eda.py <netlist> <cell_name> [data_file]")
    #     return
    # cells, cell = args[0], args[1]
    # data_file = args[2] if len(args) == 3 else "sa_data.csv"  # fj_pro: 如果提供了第三个参数就用它，否则默认文件名

    print("[main] netlist =", cells, "cell =", cell)
    print("[main] data_file =", data_file)
    s = read_cell(cells, cell)
    print("[main] read_cell 返回行数:", len(s))
    pins, nets, nmos, pmos, filename, w_ref = init(s)
    print("[main] pins_idx:", pins)
    print("[main] nets:", nets)
    print("[main] 初始 NMOS 数量:", len(nmos), "PMOS 数量:", len(pmos))
    print("[main] w_ref =", w_ref)
    mos_num = len(pmos) + len(nmos)
    print("[main] mos_num =", mos_num)
    pmos_ary, nmos_ary, pp_ary, np_ary = init_layout(pmos, nmos)
    print("[main] init_layout 返回的 pmos_ary 长度:", len(pmos_ary))
    print("[main] init_layout 返回的 nmos_ary 长度:", len(nmos_ary))
    print("[main] init_layout 返回的 pp_ary 长度:", len(pp_ary))
    print("[main] init_layout 返回的 np_ary 长度:", len(np_ary))

    # Python Mos -> sa_core.Mos
    def to_sa_mos(m: Mos) -> sa_core.Mos:
        mos = sa_core.Mos()
        mos.name = m.name
        mos.id = int(m.id)
        mos.x = int(m.x)
        mos.s = int(m.s)
        mos.g = int(m.g)
        mos.d = int(m.d)
        mos.w = int(m.w)
        return mos

    pmos_ary_sa = [to_sa_mos(m) for m in pmos_ary]
    nmos_ary_sa = [to_sa_mos(m) for m in nmos_ary]
    pp_ary_sa = [None if m is None else to_sa_mos(m) for m in pp_ary]
    np_ary_sa = [None if m is None else to_sa_mos(m) for m in np_ary]

    print("[main] fj: mos_num =", mos_num)
    t0 = float(mos_num) * x_t0  # fj: 调整初始温度参数
    tt = 0.1                     # fj: 调整终止温度参数
    decrease = z_decrease                # fj: 调整降温速率参数
    times = mos_num * w_times        # fj: 调整每个温度的move次数
    print("[main] 退火参数 t0=", t0, "tt=", tt, "decrease=", decrease, "times=", times)

    new_pary_sa, new_nary_sa, new_pp_sa, new_np_sa = sa_core.run_sa(
        w_ref,
        nets,
        pins,
        pmos_ary_sa,
        nmos_ary_sa,
        pp_ary_sa,
        np_ary_sa,
        t0,
        tt,
        decrease,
        times,
        data_file # fj_pro: 传入数据文件名字
    )

    print("[main] sa_core.run_sa 返回 PMOS 数量:", len(new_pary_sa))
    print("[main] sa_core.run_sa 返回 NMOS 数量:", len(new_nary_sa))

    # sa_core.Mos -> Python Mos
    def from_sa_mos(m: sa_core.Mos) -> Mos:
        return Mos(
            name=m.name,
            id=int(m.id),
            x=int(m.x),
            s=int(m.s),
            g=int(m.g),
            d=int(m.d),
            w=int(m.w),
        )

    new_pary = [from_sa_mos(m) for m in new_pary_sa]
    new_nary = [from_sa_mos(m) for m in new_nary_sa]


    content = placement_str(new_pary, new_nary, nets)
    out_name = f"{filename}.json"
    write_to_file(out_name, content)
    print(f"Placement written to {out_name}")


if __name__ == "__main__":
    main()

