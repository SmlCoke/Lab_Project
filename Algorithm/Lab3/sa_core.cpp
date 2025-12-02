#include <vector>
#include <string>
#include <optional>
#include <tuple>
#include <cmath>
#include <random>
#include <algorithm>
#include <iostream>

using std::vector;
using std::string;
using std::optional;
using std::tuple;
using std::make_tuple;

// Pins: 记录管脚在 nets 数组中的索引，例如某个逻辑管脚对应哪个 net
using Pins = vector<int>;
// Nets: 记录所有 net 的名字，例如 VDD/VSS/内部信号名
using Nets = vector<string>;

// Mos: 描述一颗晶体管的逻辑/几何属性
// name: 器件名（例如 M1）
// id  : 在数组里的编号，用来在 place 数组和 mos 数组之间对应
// x   : 在一维布局中的列坐标
// s/g/d: 源极(Source)/栅极(Gate)/漏极(Drain) 所连接的 net 索引
// w   : 版图宽度，用于 notch 检查等
struct Mos {
    string name;
    int id;
    int x;
    int s;
    int g;
    int d;
    int w;
};

// 把一个 optional<Mos> 安全地“解包”为一个普通的 Mos，如果里面是空，就返回一个“占位的假 MOS”
inline Mos convert_to_mos(const optional<Mos>& mos_op) {
    if (mos_op.has_value()) return mos_op.value();
    return Mos{"NULL", -1, -1, -1, -1, -1, 0};
}

// Pair: 记录一个 net 在一维布局上的最左/最右坐标
struct Pair {
    double pmin;
    double pmax;
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 用来评分的函数
//      routing: 估算布线 bbox 长度之和（不含 VDD/VSS），作为布线拥挤度的一项指标 bbox 是 “bounding box” 的缩写
double routing(const Nets& net_ary,
               const vector<optional<Mos>>& pp_ary,
               const vector<optional<Mos>>& np_ary) {
    vector<Pair> nets_routing(net_ary.size(), Pair{INFINITY, -INFINITY});

    // traverse: 扫描一行（PMOS 或 NMOS），更新 nets_routing 中每个 net 的 pmin/pmax
    auto traverse = [&](const vector<optional<Mos>>& ary) {
        for (size_t i = 0; i < ary.size(); ++i) {
            if (!ary[i].has_value()) continue;
            Mos mos = convert_to_mos(ary[i]);
            int s = mos.s;
            int g = mos.g;
            int d = mos.d;
            nets_routing[s].pmin = std::min(nets_routing[s].pmin, static_cast<double>(i) - 0.5);
            nets_routing[s].pmax = std::max(nets_routing[s].pmax, static_cast<double>(i) - 0.5);
            nets_routing[g].pmin = std::min(nets_routing[g].pmin, static_cast<double>(i));
            nets_routing[g].pmax = std::max(nets_routing[g].pmax, static_cast<double>(i));
            nets_routing[d].pmin = std::min(nets_routing[d].pmin, static_cast<double>(i) + 0.5);
            nets_routing[d].pmax = std::max(nets_routing[d].pmax, static_cast<double>(i) + 0.5);
        }
    };

    traverse(pp_ary);
    traverse(np_ary);

    double res = 0.0;
    for (size_t i = 0; i < nets_routing.size(); ++i) {
        if (net_ary[i] == "VDD" || net_ary[i] == "VSS") continue;
        res += nets_routing[i].pmax - nets_routing[i].pmin;
    }
    return res;
}
//      calc_symmetric: 统计上下两行在同一列“一个有器件一个没有”的不对称列数
int calc_symmetric(const vector<optional<Mos>>& pp_ary,
                   const vector<optional<Mos>>& np_ary) {
    int res = 0;
    size_t n = std::min(pp_ary.size(), np_ary.size());
    for (size_t i = 0; i < n; ++i) {
        bool p_none = !pp_ary[i].has_value();
        bool n_none = !np_ary[i].has_value();
        if ((p_none && !n_none) || (!p_none && n_none)) res++;
    }
    return res;
}
//      calc_pin_access 给当前布局算一个“IO 管脚好不好接线”的指标，值越大表示越难接（越差），最后返回的是这些管脚间距的标准差
//          remove_duplicates: 保留出现顺序的同时去除重复元素
vector<double> remove_duplicates(const vector<double>& lst) {
    vector<double> res;
    for (double x : lst) {
        bool exists = false;
        for (double y : res) {
            if (y == x) { exists = true; break; }
        }
        if (!exists) res.push_back(x);
    }
    return res;
}
//          standard_deviation: 计算一组 double 数据的标准差
double standard_deviation(const vector<double>& lst) {
    if (lst.empty()) return 0.0;
    double length = static_cast<double>(lst.size());
    double sum = 0.0;
    for (double x : lst) sum += x;
    double mean_val = sum / length;
    double acc = 0.0;
    for (double x : lst) {
        double d = x - mean_val;
        acc += d * d;
    }
    return std::sqrt(acc / length);
}
//          calc_pin_access主函数
double calc_pin_access(const Nets& nets,
                       const Pins& pins,
                       const vector<optional<Mos>>& pp_ary,
                       const vector<optional<Mos>>& np_ary) {
    double width = static_cast<double>(pp_ary.size());

    // mv_pins: 过滤掉 VDD/VSS，只保留普通信号管脚
    auto mv_pins = [&](const Pins& lst) {
        Pins res;
        for (int hd : lst) {
            const string& name = nets[hd];
            if (name != "VSS" && name != "VDD") res.push_back(hd);
        }
        return res;
    };

    Pins pins_mv = mv_pins(pins);

    // create_lst: 针对某一行，返回
    //  r: 该 pin 直接连接到的 s/g/d 的坐标
    //  another_pos: 与该 pin 同网但属于其他管脚集合的坐标
    auto create_lst = [&](const vector<optional<Mos>>& place_ary, int pin) {
        vector<double> r;
        vector<double> another_pos;
        for (size_t i = 0; i < place_ary.size(); ++i) {
            if (!place_ary[i].has_value()) continue;
            Mos mos = convert_to_mos(place_ary[i]);
            if (mos.s == pin) r.push_back(static_cast<double>(i) - 0.5);
            else {
                bool in_mv = false;
                for (int v : pins_mv) if (v == mos.s) { in_mv = true; break; }
                if (mos.s != pin && in_mv) another_pos.push_back(static_cast<double>(i) - 0.5);
            }
            if (mos.g == pin) r.push_back(static_cast<double>(i));
            else {
                bool in_mv = false;
                for (int v : pins_mv) if (v == mos.g) { in_mv = true; break; }
                if (mos.g != pin && in_mv) another_pos.push_back(static_cast<double>(i));
            }
            if (mos.d == pin) r.push_back(static_cast<double>(i) + 0.5);
            else {
                bool in_mv = false;
                for (int v : pins_mv) if (v == mos.d) { in_mv = true; break; }
                if (mos.d != pin && in_mv) another_pos.push_back(static_cast<double>(i) + 0.5);
            }
        }
        return std::make_pair(r, another_pos);
    };

    // create: 合并上下两行的信息，得到 pin 的候选位置及其“对手”位置
    auto create = [&](int pin) {
        auto pl = create_lst(pp_ary, pin);
        auto nl = create_lst(np_ary, pin);
        vector<double> pos1 = remove_duplicates(pl.first);
        vector<double> tmp = remove_duplicates(nl.first);
        pos1.insert(pos1.end(), tmp.begin(), tmp.end());
        std::sort(pos1.begin(), pos1.end());
        vector<double> pos2 = remove_duplicates(pl.second);
        tmp = remove_duplicates(nl.second);
        pos2.insert(pos2.end(), tmp.begin(), tmp.end());
        std::sort(pos2.begin(), pos2.end());
        return std::make_pair(pos1, pos2);
    };

    // distance: 计算 pos 到 lst 中最近点的距离
    auto distance = [](double pos, const vector<double>& lst) {
        if (lst.empty()) return -1.0;
        if (pos < lst.front()) return lst.front() - pos;
        if (pos > lst.back()) return pos - lst.back();
        for (size_t i = 0; i + 1 < lst.size(); ++i) {
            if (lst[i] <= pos && pos <= lst[i + 1]) {
                double d1 = pos - lst[i];
                double d2 = lst[i + 1] - pos;
                return d1 < d2 ? d1 : d2;
            }
        }
        return -1.0;
    };

    // pin_coord: 为某个 pin 选择一个“最容易接线”的横坐标
    auto pin_coord = [&](int pin) {
        auto cr = create(pin);
        const vector<double>& r = cr.first;
        const vector<double>& another_pos = cr.second;
        double max_dis = -INFINITY;
        double res = 0.0;
        for (double hd : r) {
            double dis = distance(hd, another_pos);
            if (dis > max_dis) { max_dis = dis; res = hd; }
        }
        return res;
    };

    vector<double> pin_coords;
    for (int p : pins_mv) pin_coords.push_back(pin_coord(p));
    std::sort(pin_coords.begin(), pin_coords.end());

    size_t length = pin_coords.size();
    if (length < 2) return 1.0;

    double left_spacing = pin_coords.front() + 0.5;
    double right_spacing = width - 0.5 - pin_coords.back();
    vector<double> pin_spacing;
    if (left_spacing > 1.0) pin_spacing.push_back(left_spacing / width);
    if (right_spacing > 1.0) pin_spacing.push_back(right_spacing / width);
    for (size_t i = 0; i + 1 < length; ++i) {
        pin_spacing.push_back((pin_coords[i + 1] - pin_coords[i]) / width);
    }
    return standard_deviation(pin_spacing);
}
//      evaluator: 根据当前布局计算综合评分和若干子指标
tuple<double,double,double,double,double> evaluator(
    int w_ref,
    const Nets& nets,
    const Pins& pins,
    const vector<Mos>& pmos_ary,
    const vector<Mos>& nmos_ary,
    const vector<optional<Mos>>& pmos_place,
    const vector<optional<Mos>>& nmos_place
) {
    double w_ref_f = static_cast<double>(w_ref);

    vector<Mos> pmos_lst = pmos_ary;
    vector<Mos> nmos_lst = nmos_ary;
    vector<int> x_lst;
    x_lst.reserve(pmos_lst.size() + nmos_lst.size());
    for (const auto& m : pmos_lst) x_lst.push_back(m.x);
    for (const auto& m : nmos_lst) x_lst.push_back(m.x);

    int max_x = 0;
    for (int x : x_lst) if (x > max_x) max_x = x;
    double width = static_cast<double>(max_x + 1);
    // width 越接近参考宽度 w_ref_f，这个值越高（最多 40 分）；如果比参考宽度宽很多，就扣分
    double ws = 40.0 * (1.0 - (width - w_ref_f) / (w_ref_f + 20.0));

    // 调用 routing(...) 算出来的总 bbox 长度（非 VDD/VSS net 的水平跨距总和）
    double bbox = routing(nets, pmos_place, nmos_place);
    // 先根据 bbox 和期望值做一个线性打分，再限制在 ± 一定范围
    double y = 20.0 * (1.0 - (bbox - w_ref_f * static_cast<double>(pins.size() - 1)) / 60.0);
    // min(20, y)，布线拥挤度的得分，最高 20 分，bbox 越小越好
    double bs = std::min(20.0, y);

    // 不对称列越少，分数越高，最多 10 分
    double ss = 10.0 - static_cast<double>(calc_symmetric(pmos_place, nmos_place));

    // 调用 calc_pin_access 得到的“管脚可接性差程度”（标准差），越大越差
    double pin_access = calc_pin_access(nets, pins, pmos_place, nmos_place);
    double ps = 10.0 * (1.0 - pin_access);

    double total = ws + bs + ss + ps;
    return make_tuple(total, width, bbox, pin_access, ss);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// check_notch: 沿着一行检查是否产生“凹槽(notch)”形状的宽度序列
bool check_notch(const vector<optional<Mos>>& place_ary) {
    int pre_width = 0;
    if (place_ary.empty()) return true;
    for (size_t i = 0; i + 1 < place_ary.size(); ++i) {
        if (!place_ary[i].has_value()) {
            pre_width = 0;
            continue;
        }
        int cur_w = convert_to_mos(place_ary[i]).w;
        int next_w = place_ary[i + 1].has_value() ? convert_to_mos(place_ary[i + 1]).w : 0;
        if (pre_width > cur_w && cur_w < next_w) return false;
        pre_width = cur_w;
    }
    return true;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// 两个用来更新扰动后坐标的函数 update_place_ary 和 update_mos_ary
//      update_place_ary:在上下两行同时尝试删除“安全空列”（上下都是空，且两边连线可直接相接且不会造成 notch）
//          ary_drop: 删除数组中指定位置的元素（用于删掉一列空位）
vector<optional<Mos>> ary_drop(const vector<optional<Mos>>& ary, size_t pos) {
    vector<optional<Mos>> res;
    res.reserve(ary.size() ? ary.size() - 1 : 0);
    for (size_t i = 0; i < ary.size(); ++i) {
        if (i == pos) continue;
        res.push_back(ary[i]);
    }
    return res;
}
//          update_place_ary主函数
std::pair<vector<optional<Mos>>, vector<optional<Mos>>> update_place_ary(
    const vector<optional<Mos>>& pp_in,
    const vector<optional<Mos>>& np_in
) {
    vector<optional<Mos>> pp_ary = pp_in;
    vector<optional<Mos>> np_ary = np_in;
    size_t i = 0;
    while (i < pp_ary.size()) {
        // 当前列上的 PMOS/NMOS（可能为空）
        optional<Mos> pmos = pp_ary[i];
        optional<Mos> nmos = np_ary[i];
        // left_* / right_*：左右一列的器件，如果越界就给一个空的 optional<Mos>{}
        optional<Mos> left_pmos = (i > 0) ? pp_ary[i - 1] : optional<Mos>{};
        optional<Mos> left_nmos = (i > 0) ? np_ary[i - 1] : optional<Mos>{};
        optional<Mos> right_pmos = (i + 1 < pp_ary.size()) ? pp_ary[i + 1] : optional<Mos>{};
        optional<Mos> right_nmos = (i + 1 < np_ary.size()) ? np_ary[i + 1] : optional<Mos>{};

        // cond 为真表示这一列上下都没器件，是空列，有资格考虑删掉
        bool cond = !pmos.has_value() && !nmos.has_value();
        if (cond) {
            bool p_ok = !left_pmos.has_value() || !right_pmos.has_value() ||      // 如果左边或右边本来就没有 PMOS（有一侧为空，或者两侧都空），那删掉这列没问题；
                (convert_to_mos(left_pmos).d == convert_to_mos(right_pmos).s);    // 否则，两侧都有 PMOS，就要求左边 MOS 的 d 和右边 MOS 的 s 相同 net，说明它们串在同一条 net 上，这样中间空列删掉后还能直接接上
            bool n_ok = !left_nmos.has_value() || !right_nmos.has_value() ||
                (convert_to_mos(left_nmos).d == convert_to_mos(right_nmos).s);
            if (p_ok && n_ok) {
                vector<optional<Mos>> new_pp = ary_drop(pp_ary, i);
                vector<optional<Mos>> new_np = ary_drop(np_ary, i);
                if (check_notch(new_pp) && check_notch(new_np)) {        // 检查删除这一列后，上/下行是否出现禁止的 notch 形状
                    pp_ary.swap(new_pp);
                    np_ary.swap(new_np);
                    continue;
                }
            }
        }
        ++i;
    }
    return {pp_ary, np_ary};
}
//      update_mos_ary: 根据新的 place 阵列，把 mos_ary 中每个器件的 x 坐标同步更新到和mos_place一致
void update_mos_ary(vector<Mos>& mos_ary, const vector<optional<Mos>>& mos_place) {
    for (size_t i = 0; i < mos_place.size(); ++i) {
        if (!mos_place[i].has_value()) continue;
        Mos mos = convert_to_mos(mos_place[i]);
        if (mos.id >= 0 && static_cast<size_t>(mos.id) < mos_ary.size()) {
            mos_ary[mos.id] = Mos{mos.name, mos.id, static_cast<int>(i), mos.s, mos.g, mos.d, mos.w};
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// pre_MOS 和 beh_MOS 函数：用来找可以动的空位置 empty 之前已经产生源漏共用的 MOS 管集合 preMOS，空位置 mv_emp 之后已经产生源漏共用的 MOS 管集合 behMOS
//      pre_MOS: 取 pos 左边“连续非空”的 MOS 段，遇到空位就停止
vector<optional<Mos>> pre_MOS(const vector<optional<Mos>>& place_ary, int pos) {
    vector<optional<Mos>> res;
    for (int i = pos - 1; i >= 0; --i) {
        if (place_ary[static_cast<size_t>(i)].has_value()) {
            res.push_back(place_ary[static_cast<size_t>(i)]);
        } else {
            break;
        }
    }
    std::reverse(res.begin(), res.end());
    return res;
}
//      beh_MOS: 取 pos 右边“连续非空”的 MOS 段，遇到空位就停止
vector<optional<Mos>> beh_MOS(const vector<optional<Mos>>& place_ary, int pos) {
    vector<optional<Mos>> res;
    for (size_t i = static_cast<size_t>(pos + 1); i < place_ary.size(); ++i) {
        if (place_ary[i].has_value()) {
            res.push_back(place_ary[i]);
        } else {
            break;
        }
    }
    return res;
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// select_some: 从 optional<Mos> 列表中过滤出真实存在的 MOS
vector<Mos> select_some(const vector<optional<Mos>>& ary) {
    vector<Mos> res;
    for (const auto& m : ary) {
        if (m.has_value()) res.push_back(convert_to_mos(m));
    }
    return res;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//---------------------------------------------------------------------------------------------------------------------//
// 一组“翻转/镜像”相关的辅助函数, 是 is_legal 的底层动作库
//   - flip_preMOS_prime / flip_behMOS_prime：
//       针对 PMOS 行左/右侧的一串连续 MOS，在 NMOS 行上找到对应的“prime 串”，
//       判定这条 prime 串要不要翻、能不能翻（是否还能与边界 MOS / 移动 MOS 对上 net）。
//   - record_flip：
//       把若干段待翻转的 MOS 串（vector<vector<optional<Mos>>>）拍扁成一个列表，
//       过滤掉空位，只保留真实 MOS，并记录它们的 id，作为翻转操作的目标集合。
//   - set_mos_flip：
//       根据记录的 id，在 mos_ary（真实数据）和 place_ary（布局棋盘）中同步翻转这些 MOS 的源/漏，
//       实现源漏对调的逻辑一致性。
//   - set_subary_flip：
//       对布局数组中的一段子区间做顺序反转，用来配合 set_mos_flip 完成“一整段 MOS 串”的镜像操作，
//       从而支持 is_legal 中的各种“翻 pre 串/翻 beh 串/翻 mv 自身”的组合场景。
//---------------------------------------------------------------------------------------------------------------------//
// flip_preMOS_prime:flip_preMOS_prime 只在 is_legal 中、在“打算翻左边那串 pre MOS”的分支里被调用，用来判定：这串对应的 NMOS prime 串要不要翻、能不能翻；如果返回 -1，就说明这条布局变换在 NMOS 侧接线不可能合法，这个 move 方案被否掉。
//   针对“左边连续 NMOS 串”(mos_set_prime)，判断是否需要/可以翻转它们
//   bound_mos    : 更远一侧与 mos_set_prime 相接的 NMOS（边界）
//   mv_mos_prime : 与正在移动的 PMOS 对应的“影子 NMOS”
// 返回值:
//   1: 不需要翻 prime 串
//   0: 需要翻 prime 串
//  -1: 无论怎么翻都接不上，非法
int flip_preMOS_prime(const vector<optional<Mos>>& mos_set_prime,
            const optional<Mos>& bound_mos,
            const optional<Mos>& mv_mos_prime) {
    size_t len = mos_set_prime.size();
    if (len == 0 || len == 1) return 1;

    optional<Mos> fMOS_prime = mos_set_prime.front();
    optional<Mos> lMOS_prime = mos_set_prime.back();

    // 保证翻完 prime 串后，外侧那一端的 net 方向可以接上 bound_mos
    bool cond1 = !bound_mos.has_value() || !lMOS_prime.has_value() ||
        (convert_to_mos(lMOS_prime).d == convert_to_mos(bound_mos).d);
    // 保证翻完 prime 串后，靠近 mv_mos_prime 这边的 net 方向可以接上 mv_mos_prime
    bool cond2 = !fMOS_prime.has_value() || !mv_mos_prime.has_value() ||
        (convert_to_mos(fMOS_prime).s == convert_to_mos(mv_mos_prime).s);
    if (cond1 && cond2) return 0;
    return -1;
}

// flip_behMOS_prime: 与 flip_preMOS_prime 类似，只是作用在右侧连续 NMOS 串
int flip_behMOS_prime(const vector<optional<Mos>>& mos_set_prime,
            const optional<Mos>& bound_mos,
            const optional<Mos>& mv_mos_prime) {
    size_t len = mos_set_prime.size();
    if (len == 0 || len == 1) return 1;
    optional<Mos> fMOS_prime = mos_set_prime.front();
    optional<Mos> lMOS_prime = mos_set_prime.back();
    bool cond1 = !mv_mos_prime.has_value() || !lMOS_prime.has_value() ||
        (convert_to_mos(lMOS_prime).d == convert_to_mos(mv_mos_prime).d);
    bool cond2 = !fMOS_prime.has_value() || !bound_mos.has_value() ||
        (convert_to_mos(fMOS_prime).s == convert_to_mos(bound_mos).s);
    if (cond1 && cond2) return 0;
    return -1;
}

// record_flip:把若干段要翻转的 MOS 串（vector<vector<optional<Mos>>>）压缩，挑出真实存在的 MOS，再抽取它们的 id，最后得到一个“要翻的 MOS id 列表”。
vector<int> record_flip(const vector<vector<optional<Mos>>>& record) {
    vector<optional<Mos>> flat;
    for (const auto& sub : record) {
        flat.insert(flat.end(), sub.begin(), sub.end());
    }
    vector<Mos> some_lst = select_some(flat);
    vector<int> ids;
    ids.reserve(some_lst.size());
    for (const auto& m : some_lst) ids.push_back(m.id);
    return ids;
}

// set_mos_flip:根据record_flip给的这堆“要翻的 id”，在两个地方里同时翻源极/漏极：
//   在 mos_ary 里翻一次（真正的数据源）。
//   在 place_ary（布局棋盘）里再翻一次（保证布局里那份拷贝一致）
// mos_set_flip：要翻转的 MOS 段集合（比如 {preMOS}, {behMOS}, {mv_m} 的组合）
void set_mos_flip(vector<Mos>& mos_ary,
            vector<optional<Mos>>& place_ary,
            const vector<vector<optional<Mos>>>& mos_set_flip) {
    vector<int> flip_ids = record_flip(mos_set_flip);
    // flip in mos_ary
    for (int mid : flip_ids) {
        if (mid < 0 || static_cast<size_t>(mid) >= mos_ary.size()) continue;
        Mos& mos = mos_ary[static_cast<size_t>(mid)];
        int s = mos.s;
        int d = mos.d;
        mos.s = d;
        mos.d = s;
    }
    // flip in place_ary
    for (size_t i = 0; i < place_ary.size(); ++i) {
        if (!place_ary[i].has_value()) continue;
        Mos mos = convert_to_mos(place_ary[i]);
        bool need_flip = false;
        for (int id : flip_ids) {
            if (id == mos.id) { need_flip = true; break; }
        }
        if (need_flip) {
            int s = mos.s;
            int d = mos.d;
            mos.s = d;
            mos.d = s;
            place_ary[i] = mos;
        }
    }
}

// set_subary_flip:
//   对 place_ary 中从 pos 开始、长度为 length 的子数组做“顺序反转”，
//   用来配合 set_mos_flip 实现一整段 MOS 的镜像
vector<optional<Mos>> set_subary_flip(const vector<optional<Mos>>& place_ary,
                    int pos,
                    int length) {
    if (pos < 0 || length <= 0) return place_ary;
    size_t start = static_cast<size_t>(pos);
    if (start >= place_ary.size()) return place_ary;
    size_t end = std::min(start + static_cast<size_t>(length), place_ary.size());
    vector<optional<Mos>> mid(place_ary.begin() + start, place_ary.begin() + end);
    std::reverse(mid.begin(), mid.end());
    vector<optional<Mos>> res;
    res.reserve(place_ary.size());
    res.insert(res.end(), place_ary.begin(), place_ary.begin() + start);
    res.insert(res.end(), mid.begin(), mid.end());
    res.insert(res.end(), place_ary.begin() + end, place_ary.end());
    return res;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// is_legal:
//   尝试把一颗 MOS 从 mv_occ 列移动到 mv_emp 空列，
//   通过局部翻转/镜像左右邻居以及对侧行对应串，判断是否能得到合法无 notch 的新布局。
// 返回:
//   bool             : 是否存在合法变换
//   vector<Mos>      : 变换后的 PMOS 阵列
//   vector<Mos>      : 变换后的 NMOS 阵列
//   vector<optional<Mos>>: 变换后的 PMOS 布局行
//   vector<optional<Mos>>: 变换后的 NMOS 布局行
tuple<bool, vector<Mos>, vector<Mos>, vector<optional<Mos>>, vector<optional<Mos>>>
is_legal(
    const vector<Mos>& pary,
    const vector<Mos>& nary,
    const vector<optional<Mos>>& pplace_ary,
    const vector<optional<Mos>>& nplace_ary,
    int mv_occ,
    int mv_emp
) {
    vector<Mos> pmos_ary = pary;
    vector<Mos> nmos_ary = nary;
    vector<optional<Mos>> pp_ary = pplace_ary;
    vector<optional<Mos>> np_ary = nplace_ary;

    optional<Mos> mv_mos = pp_ary[static_cast<size_t>(mv_occ)];
    pp_ary[static_cast<size_t>(mv_occ)] = std::nullopt;

    vector<optional<Mos>> preMOS = pre_MOS(pp_ary, mv_emp);
    vector<optional<Mos>> behMOS = beh_MOS(pp_ary, mv_emp);

    int pre_len = static_cast<int>(preMOS.size());
    int beh_len = static_cast<int>(behMOS.size());

    vector<optional<Mos>> preMOS_prime;
    if (pre_len > 0 && mv_emp - pre_len >= 0) {
        for (int i = mv_emp - pre_len; i < mv_emp; ++i)
            preMOS_prime.push_back(np_ary[static_cast<size_t>(i)]);
    }
    vector<optional<Mos>> behMOS_prime;
    if (beh_len > 0) {
        for (int i = mv_emp + 1; i < mv_emp + 1 + beh_len && i < static_cast<int>(np_ary.size()); ++i)
            behMOS_prime.push_back(np_ary[static_cast<size_t>(i)]);
    }

    optional<Mos> fpreMOS = pre_len > 0 ? preMOS.front() : optional<Mos>{};
    optional<Mos> lpreMOS = pre_len > 0 ? preMOS.back() : optional<Mos>{};
    optional<Mos> fbehMOS = beh_len > 0 ? behMOS.front() : optional<Mos>{};
    optional<Mos> lbehMOS = beh_len > 0 ? behMOS.back() : optional<Mos>{};

    optional<Mos> left_preMOS_prime;
    if (mv_emp - pre_len - 1 >= 0)
        left_preMOS_prime = np_ary[static_cast<size_t>(mv_emp - pre_len - 1)];
    optional<Mos> right_behMOS_prime;
    if (mv_emp + beh_len + 1 < static_cast<int>(np_ary.size()))
        right_behMOS_prime = np_ary[static_cast<size_t>(mv_emp + beh_len + 1)];

    Mos mv_m = convert_to_mos(mv_mos);

    // restore: 如果当前尝试失败，把被挪走的 MOS 放回原位并返回非法结果
    auto restore = [&]() {
        pp_ary[static_cast<size_t>(mv_occ)] = mv_mos;
        return make_tuple(false, pmos_ary, nmos_ary, pp_ary, np_ary);
    };

    // 0 0 0: 不翻 pre、不翻 mv、不翻 beh，直接尝试把 mv 放进去
    if (( !lpreMOS.has_value() || convert_to_mos(lpreMOS).d == mv_m.s ) &&
        ( !fbehMOS.has_value() || mv_m.d == convert_to_mos(fbehMOS).s ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
        return make_tuple(true, pmos_ary, nmos_ary, pp_ary, np_ary);
    }

    // 0 0 1: 不翻 pre、不翻 mv，翻 beh 串（以及必要时对应的 NMOS 串）
    if (( !lpreMOS.has_value() || convert_to_mos(lpreMOS).d == mv_m.s ) &&
        ( !lbehMOS.has_value() || mv_m.d == convert_to_mos(lbehMOS).d ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res = flip_behMOS_prime(behMOS_prime, right_behMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        if (res == 1) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {behMOS});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp + 1, beh_len);
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
        }
        if (res == 0) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {behMOS});
            set_mos_flip(nmos_ary, np_ary, {behMOS_prime});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp + 1, beh_len);
            vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
        }
        return restore();
    }

    // 0 1 0: 不翻 pre，翻 mv，本身方向互补即可
    if (( !lpreMOS.has_value() || convert_to_mos(lpreMOS).d == mv_m.d ) &&
        ( !fbehMOS.has_value() || mv_m.s == convert_to_mos(fbehMOS).s ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
        set_mos_flip(pmos_ary, pp_ary, {{mv_m}});
        return make_tuple(true, pmos_ary, nmos_ary, pp_ary, np_ary);
    }

    // 0 1 1: 不翻 pre，翻 mv 和 beh
    if (( !lpreMOS.has_value() || convert_to_mos(lpreMOS).d == mv_m.d ) &&
        ( !lbehMOS.has_value() || mv_m.s == convert_to_mos(lbehMOS).d ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res = flip_behMOS_prime(behMOS_prime, right_behMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        if (res == 1) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {behMOS, {mv_m}});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp + 1, beh_len);
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
        }
        if (res == 0) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {behMOS, {mv_m}});
            set_mos_flip(nmos_ary, np_ary, {behMOS_prime});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp + 1, beh_len);
            vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
        }
        return restore();
    }

    // 1 0 0: 翻 pre，不翻 mv
    if (( !fpreMOS.has_value() || convert_to_mos(fpreMOS).s == mv_m.s ) &&
        ( !fbehMOS.has_value() || mv_m.d == convert_to_mos(fbehMOS).s ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res = flip_preMOS_prime(preMOS_prime, left_preMOS_prime,
                       np_ary[static_cast<size_t>(mv_emp)]);
        if (res == 1) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {preMOS});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
        }
        if (res == 0) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {preMOS});
            set_mos_flip(nmos_ary, np_ary, {preMOS_prime});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
            vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
        }
        return restore();
    }

    // 1 0 1: 翻 pre，不翻 mv，翻 beh
    if (( !fpreMOS.has_value() || convert_to_mos(fpreMOS).s == mv_m.s ) &&
        ( !lbehMOS.has_value() || mv_m.d == convert_to_mos(lbehMOS).d ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res1 = flip_preMOS_prime(preMOS_prime, left_preMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        int res2 = flip_behMOS_prime(behMOS_prime, right_behMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        if (res1 == 1) {
            if (res2 == 1) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, behMOS});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
            }
            if (res2 == 0) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, behMOS});
                set_mos_flip(nmos_ary, np_ary, {behMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            return restore();
        }
        if (res1 == 0) {
            if (res2 == 1) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, behMOS});
                set_mos_flip(nmos_ary, np_ary, {preMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            if (res2 == 0) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, behMOS});
                set_mos_flip(nmos_ary, np_ary, {preMOS_prime, behMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                np_ary2 = set_subary_flip(np_ary2, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            return restore();
        }
        return restore();
    }

    // 1 1 0: 翻 pre 和 mv，不翻 beh
    if (( !fpreMOS.has_value() || convert_to_mos(fpreMOS).s == mv_m.d ) &&
        ( !fbehMOS.has_value() || mv_m.s == convert_to_mos(fbehMOS).s ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res = flip_preMOS_prime(preMOS_prime, left_preMOS_prime,
                       np_ary[static_cast<size_t>(mv_emp)]);
        if (res == 1) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
        }
        if (res == 0) {
            pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
            set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}});
            set_mos_flip(nmos_ary, np_ary, {preMOS_prime});
            vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
            vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
            return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
        }
        return restore();
    }

    // 1 1 1: 翻 pre、mv、beh，全都翻
    if (( !fpreMOS.has_value() || convert_to_mos(fpreMOS).s == mv_m.d ) &&
        ( !lbehMOS.has_value() || mv_m.s == convert_to_mos(lbehMOS).d ) &&
        ( !np_ary[static_cast<size_t>(mv_emp)].has_value() ||
          mv_m.g == convert_to_mos(np_ary[static_cast<size_t>(mv_emp)]).g )) {
        int res1 = flip_preMOS_prime(preMOS_prime, left_preMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        int res2 = flip_behMOS_prime(behMOS_prime, right_behMOS_prime,
                        np_ary[static_cast<size_t>(mv_emp)]);
        if (res1 == 1) {
            if (res2 == 1) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}, behMOS});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary);
            }
            if (res2 == 0) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}, behMOS});
                set_mos_flip(nmos_ary, np_ary, {behMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            return restore();
        }
        if (res1 == 0) {
            if (res2 == 1) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}, behMOS});
                set_mos_flip(nmos_ary, np_ary, {preMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            if (res2 == 0) {
                pp_ary[static_cast<size_t>(mv_emp)] = mv_m;
                set_mos_flip(pmos_ary, pp_ary, {preMOS, {mv_m}, behMOS});
                set_mos_flip(nmos_ary, np_ary, {preMOS_prime, behMOS_prime});
                vector<optional<Mos>> pp_ary2 = set_subary_flip(pp_ary, mv_emp - pre_len, pre_len);
                vector<optional<Mos>> np_ary2 = set_subary_flip(np_ary,
                                 mv_emp - static_cast<int>(preMOS_prime.size()),
                                 static_cast<int>(preMOS_prime.size()));
                pp_ary2 = set_subary_flip(pp_ary2, mv_emp + 1, beh_len);
                np_ary2 = set_subary_flip(np_ary2, mv_emp + 1,
                                 static_cast<int>(behMOS_prime.size()));
                return make_tuple(true, pmos_ary, nmos_ary, pp_ary2, np_ary2);
            }
            return restore();
        }
        return restore();
    }

    return restore();
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// compute: 把一行拆成“有 MOS 的列索引”和“空列索引”两组
std::pair<vector<int>, vector<int>> compute(const vector<optional<Mos>>& ary) {
    vector<int> some_lst;
    vector<int> none_lst;
    for (size_t i = 0; i < ary.size(); ++i) {
        if (ary[i].has_value()) some_lst.push_back(static_cast<int>(i));
        else none_lst.push_back(static_cast<int>(i));
    }
    return {some_lst, none_lst};
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// rng: 全局随机数引擎，用于退火中的随机扰动和接受判断
static std::mt19937 rng{std::random_device{}()};

// simulated_annealing_cpp:
//   对给定的初始 PMOS/NMOS 布局做模拟退火优化，
//   随机在两行中选择一颗 MOS 挪到空列，如果 is_legal 判断合法且
//   通过能量差和温度决定接受，则更新当前解，直到温度降到阈值。
// 返回: 优化后的 PMOS/NMOS 数组及对应的布局阵列
// 扰动方法,换行方法
tuple<vector<Mos>, vector<Mos>, vector<optional<Mos>>, vector<optional<Mos>>>
simulated_annealing_cpp(
    int w_ref,
    const Nets& nets,
    const Pins& pins,
    const vector<Mos>& pmos_ary,
    const vector<Mos>& nmos_ary,
    const vector<optional<Mos>>& pp_ary,
    const vector<optional<Mos>>& np_ary,
    double t0,        // 起始温度
    double tt,        // 终止温度（停止条件：t <= tt）
    double decrease,  // 降温因子，例如 0.95，每轮 t *= decrease
    int times         // 每个温度下尝试的 move 次数
) {
    // 当前解：从初始布局拷贝一份出来，在此基础上做扰动
    vector<Mos> cur_pmos = pmos_ary;
    vector<Mos> cur_nmos = nmos_ary;
    vector<optional<Mos>> cur_pp = pp_ary;
    vector<optional<Mos>> cur_np = np_ary;

    // 在两行末尾各加两个空位，预留“腾挪空间”，后续每次接受新解也会再追加
    cur_pp.push_back(std::nullopt);
    cur_pp.push_back(std::nullopt);
    cur_np.push_back(std::nullopt);
    cur_np.push_back(std::nullopt);

    std::uniform_real_distribution<double> dist01(0.0, 1.0);

    double t = t0;
    while (t > tt) {
        bool tp = true; // tp 表示本轮在那一行上做 move：true=PMOS 行，false=NMOS 行,每个温度起点先从 PMOS 行开始

        for (int turn = 0; turn < times; ++turn) {
            // 找到两行中当前可用的 occupy 列和 empty 列(compute函数),以及提前结束本次温度循环的条件
            vector<int> occupy;         // occupy：当前行中被 MOS 占据的列索引
            vector<int> empty;          // empty：当前行中空列索引
            if (tp) {
                auto ce = compute(cur_pp); // fj: curr_pp: 表示当前行的 PMOS 布局
                // fj: compute 函数返回一个 pair，第一个元素是有 MOS 的列索引列表，第二个元素是空列索引列表
                occupy = std::move(ce.first); // fj: 有 MOS 的列索引列表
                empty = std::move(ce.second); // fj: 空列索引列表
            } else {
                auto ce = compute(cur_np);
                occupy = std::move(ce.first);
                empty = std::move(ce.second);
            }
            if (occupy.empty() || empty.empty()) break;

            // TODO : 在occupy列和empty列中各随机选一个位置,进行 move 尝试,并判断操作是否合法(提示:使用is_legal函数)
            std::uniform_int_distribution<int> dist_occ(0, static_cast<int>(occupy.size()) - 1);
            // fj: 创建一个均匀整数分布，范围是 [0, N-1]，其中 N = occupy.size()。
            // fj: 这样 dist_occ(rng) 就能生成 0 到 N-1 的等概率整数，正好作为 occupy 的合法索引
            std::uniform_int_distribution<int> dist_emp(0, static_cast<int>(empty.size()) - 1);
            int i = dist_occ(rng);
            int j = dist_emp(rng);
            bool legal;
            vector<Mos> pary, nary;
            vector<optional<Mos>> pplace, nplace;
            if (tp) {
                // 待补充 
                
            } else {
                // 待补充 
            }

            vector<Mos> new_pary = tp ? pary : nary;
            vector<Mos> new_nary = tp ? nary : pary;
            vector<optional<Mos>> new_pp = tp ? pplace : nplace;
            vector<optional<Mos>> new_np = tp ? nplace : pplace;

            // 模拟退火判断是否接受新的解 : 如果 move 合法且不会产生 notch，再尝试删除安全空列并更新坐标
            if (legal && check_notch(new_pp) && check_notch(new_np)) {
                auto upd = update_place_ary(new_pp, new_np);
                vector<optional<Mos>> new_pp2 = std::move(upd.first);
                vector<optional<Mos>> new_np2 = std::move(upd.second);
                update_mos_ary(new_pary, new_pp2);
                update_mos_ary(new_nary, new_np2);

                // TODO : 核心模拟退火判断部分,计算当前解和候选解的分数(使用 evaluator 函数),并判断是否采纳新解
                // 待补充

                // delta>0 表示新解更好；delta<0 表示新解更差
                double delta = s1 - s0;   // s: 分数，越大越好
                bool accept = false;
                
                // TODO: 接收准则
                // 待补充

                // TODO : 接受后更新当前解,行末尾追加空位,行切换逻辑
                if (accept) {
                    // 待补充
                    
                    cur_pp.push_back(std::nullopt);
                    cur_pp.push_back(std::nullopt);
                    cur_np.push_back(std::nullopt);
                    cur_np.push_back(std::nullopt);
                    
                    if (tp) {
                        if (!cur_nmos.empty()) tp = !tp;
                    } else {
                        if (!cur_pmos.empty()) tp = !tp;
                    }
                }
            }
        }

        // TODO : 降温
        // 待补充

    }

    return make_tuple(cur_pmos, cur_nmos, cur_pp, cur_np);
}

