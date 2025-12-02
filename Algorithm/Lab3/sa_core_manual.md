# sa_core.cpp 说明书

## 概述

`sa_core.cpp` 是本次实验的核心文件，它使用 **模拟退火算法（Simulated Annealing）** 来优化标准单元版图中晶体管的布局。你不需要理解底层的版图知识，只需要理解模拟退火的框架和如何调用已提供的辅助函数。

---

## 一、数据结构

### 1.1 基本类型别名

```cpp
using Pins = vector<int>;      // 管脚编号列表，每个元素是对应 net 在 nets 数组中的索引
using Nets = vector<string>;   // 所有 net 的名字数组，例如 ["VDD", "VSS", "IN", "OUT", ...]
```

### 1.2 Mos 结构体

`Mos` 是描述单个晶体管的数据结构：

```cpp
struct Mos {
    string name;  // 器件名称，例如 "M1"
    int id;       // 在数组中的编号，用于定位和更新
    int x;        // 在一维布局中的列坐标
    int s;        // 源极(Source)所连接的 net 索引
    int g;        // 栅极(Gate)所连接的 net 索引
    int d;        // 漏极(Drain)所连接的 net 索引
    int w;        // 器件宽度
};
```

**关键理解**：
- `s`, `g`, `d` 是 **整数索引**，对应 `nets` 数组中的位置
- 晶体管可以"翻转"，即交换 `s` 和 `d` 的值
- 布局中使用 `vector<optional<Mos>>` 表示一行，`optional` 为空表示该位置没有晶体管

### 1.3 Pair 结构体

用于记录一个 net 在布局上的最左/最右坐标：

```cpp
struct Pair {
    double pmin;  // 最左坐标
    double pmax;  // 最右坐标
};
```

---

## 二、评分函数（你需要调用）

### 2.1 evaluator 函数 ⭐

这是你在模拟退火中必须调用的**核心评分函数**：

```cpp
tuple<double,double,double,double,double> evaluator(
    int w_ref,                              // 参考宽度
    const Nets& nets,                       // net 名称数组
    const Pins& pins,                       // 管脚索引数组
    const vector<Mos>& pmos_ary,            // PMOS 晶体管数组
    const vector<Mos>& nmos_ary,            // NMOS 晶体管数组
    const vector<optional<Mos>>& pmos_place,// PMOS 布局行
    const vector<optional<Mos>>& nmos_place // NMOS 布局行
);
```

**返回值**（5个值的元组）：
1. `total` - **总分**（你需要用这个来比较解的好坏，越大越好）
2. `width` - 布局宽度
3. `bbox` - 布线 bbox 长度之和
4. `pin_access` - 管脚可接性指标
5. `ss` - 对称性得分

**使用示例**：
```cpp
auto result = evaluator(w_ref, nets, pins, pmos_ary, nmos_ary, pmos_place, nmos_place);
double score = std::get<0>(result);  // 获取总分
```

---

## 三、合法性检查函数（你需要调用）

### 3.1 is_legal 函数 ⭐

判断将某个 MOS 从位置 `mv_occ` 移动到空位置 `mv_emp` 是否合法：

```cpp
tuple<bool, vector<Mos>, vector<Mos>, vector<optional<Mos>>, vector<optional<Mos>>>
is_legal(
    const vector<Mos>& pary,              // 当前 PMOS 数组
    const vector<Mos>& nary,              // 当前 NMOS 数组
    const vector<optional<Mos>>& pplace_ary, // 当前 PMOS 布局
    const vector<optional<Mos>>& nplace_ary, // 当前 NMOS 布局
    int mv_occ,                           // 要移动的 MOS 所在的列索引（占用位置）
    int mv_emp                            // 目标空位置的列索引
);
```

**返回值**（5个值的元组）：
1. `bool` - 是否存在合法变换（`true` 表示合法）
2. `vector<Mos>` - 变换后的 PMOS 数组
3. `vector<Mos>` - 变换后的 NMOS 数组
4. `vector<optional<Mos>>` - 变换后的 PMOS 布局行
5. `vector<optional<Mos>>` - 变换后的 NMOS 布局行

**使用示例**：
```cpp
auto [legal, new_pary, new_nary, new_pplace, new_nplace] = 
    is_legal(cur_pmos, cur_nmos, cur_pp, cur_np, occupy[i], empty[j]);

if (legal) {
    // 移动合法，可以继续进行评分和判断是否接受
}
```

**注意**：
- 该函数内部会自动尝试各种翻转组合来找到合法布局
- 对于 PMOS 行，传入顺序是 `(pary, nary, pplace, nplace, ...)`
- 对于 NMOS 行，需要**交换传入顺序**：`(nary, pary, nplace, pplace, ...)`

### 3.2 check_notch 函数

检查一行布局是否存在 notch（凹槽）违规：

```cpp
bool check_notch(const vector<optional<Mos>>& place_ary);
```

- 返回 `true` 表示**没有** notch 违规（合法）
- 返回 `false` 表示**存在** notch 违规（非法）

---

## 四、布局更新函数（你需要调用）

### 4.1 update_place_ary 函数

删除布局中可以安全删除的空列，压缩布局宽度：

```cpp
std::pair<vector<optional<Mos>>, vector<optional<Mos>>> update_place_ary(
    const vector<optional<Mos>>& pp_in,  // PMOS 布局输入
    const vector<optional<Mos>>& np_in   // NMOS 布局输入
);
```

返回压缩后的 PMOS 和 NMOS 布局。

### 4.2 update_mos_ary 函数

根据新的布局数组，更新 MOS 数组中每个器件的 `x` 坐标：

```cpp
void update_mos_ary(
    vector<Mos>& mos_ary,                    // 要更新的 MOS 数组
    const vector<optional<Mos>>& mos_place   // 新的布局数组
);
```

---

## 五、辅助函数

### 5.1 compute 函数

获取布局中被占用的列索引和空列索引：

```cpp
std::pair<vector<int>, vector<int>> compute(const vector<optional<Mos>>& ary);
```

**返回值**：
- `first` - 有 MOS 的列索引列表（occupy）
- `second` - 空列索引列表（empty）

**使用示例**：
```cpp
auto [occupy, empty] = compute(cur_pp);  // 对于 PMOS 行
// occupy: [0, 2, 3, 5, ...]  // 这些列有晶体管
// empty:  [1, 4, 6, ...]     // 这些列是空的
```

---

## 六、模拟退火主函数 simulated_annealing_cpp

这是你需要补全的核心函数：

```cpp
tuple<vector<Mos>, vector<Mos>, vector<optional<Mos>>, vector<optional<Mos>>>
simulated_annealing_cpp(
    int w_ref,                              // 参考宽度
    const Nets& nets,                       // net 名称数组
    const Pins& pins,                       // 管脚索引数组
    const vector<Mos>& pmos_ary,            // 初始 PMOS 数组
    const vector<Mos>& nmos_ary,            // 初始 NMOS 数组
    const vector<optional<Mos>>& pp_ary,    // 初始 PMOS 布局
    const vector<optional<Mos>>& np_ary,    // 初始 NMOS 布局
    double t0,                              // 起始温度
    double tt,                              // 终止温度
    double decrease,                        // 降温因子 (如 0.88)
    int times                               // 每个温度下的迭代次数
);
```

### 6.1 模拟退火流程概述

```
初始化当前解 cur_* <- 输入的初始布局
设置温度 t = t0

while (t > tt):  // 外层循环：降温
    for turn in range(times):  // 内层循环：每个温度下的迭代
        1. 获取当前布局的占用位置和空位置
        2. 随机选择一个占用位置 i 和一个空位置 j
        3. 调用 is_legal 判断移动是否合法
        4. 如果合法且不产生 notch：
           a. 调用 update_place_ary 压缩空列
           b. 调用 update_mos_ary 更新坐标
           c. 调用 evaluator 计算新解的分数
           d. 根据 Metropolis 准则决定是否接受新解
        5. 如果接受：更新当前解
    
    t = t * decrease  // 降温

返回最终的布局
```

### 6.2 需要补全的部分

#### TODO 1: 随机选择位置并调用 is_legal

```cpp
// 已有：随机分布的定义
std::uniform_int_distribution<int> dist_occ(0, static_cast<int>(occupy.size()) - 1);
std::uniform_int_distribution<int> dist_emp(0, static_cast<int>(empty.size()) - 1);
int i = dist_occ(rng);  // 随机选择占用位置的索引
int j = dist_emp(rng);  // 随机选择空位置的索引

// 待补充：调用 is_legal
if (tp) {  // tp=true 表示处理 PMOS 行
    // 对于 PMOS 行，传入顺序是 (pmos, nmos, pp, np, occupy[i], empty[j])
    std::tie(legal, pary, nary, pplace, nplace) = 
        is_legal(cur_pmos, cur_nmos, cur_pp, cur_np, occupy[i], empty[j]);
} else {  // tp=false 表示处理 NMOS 行
    // 对于 NMOS 行，需要交换顺序 (nmos, pmos, np, pp, occupy[i], empty[j])
    std::tie(legal, nary, pary, nplace, pplace) = 
        is_legal(cur_nmos, cur_pmos, cur_np, cur_pp, occupy[i], empty[j]);
}
```

#### TODO 2: 计算分数

```cpp
// 计算当前解的分数
auto eval0 = evaluator(w_ref, nets, pins, cur_pmos, cur_nmos, cur_pp, cur_np);
double s0 = std::get<0>(eval0);  // 当前解的总分

// 计算新解的分数
auto eval1 = evaluator(w_ref, nets, pins, new_pary, new_nary, new_pp2, new_np2);
double s1 = std::get<0>(eval1);  // 新解的总分
```

#### TODO 3: Metropolis 接受准则

```cpp
double delta = s1 - s0;  // 分数差，正值表示新解更好
bool accept = false;

if (delta > 0) {
    // 新解更好，直接接受
    accept = true;
} else {
    // 新解更差，以一定概率接受
    // 概率 = exp(delta / t)，delta为负数，t越大概率越高
    double prob = std::exp(delta / t);
    if (dist01(rng) < prob) {
        accept = true;
    }
}
```

#### TODO 4: 接受后更新当前解

```cpp
if (accept) {
    cur_pmos = new_pary;
    cur_nmos = new_nary;
    cur_pp = new_pp2;
    cur_np = new_np2;
    
    // 追加空位（已在代码中提供）
    cur_pp.push_back(std::nullopt);
    cur_pp.push_back(std::nullopt);
    cur_np.push_back(std::nullopt);
    cur_np.push_back(std::nullopt);
    
    // 行切换逻辑（已在代码中提供）
    if (tp) {
        if (!cur_nmos.empty()) tp = !tp;
    } else {
        if (!cur_pmos.empty()) tp = !tp;
    }
}
```

#### TODO 5: 降温

```cpp
t = t * decrease;  // 指数降温
```

---

## 七、完整的 simulated_annealing_cpp 补全示例

```cpp
// TODO 1: 调用 is_legal 判断移动是否合法
if (tp) {
    std::tie(legal, pary, nary, pplace, nplace) = 
        is_legal(cur_pmos, cur_nmos, cur_pp, cur_np, occupy[i], empty[j]);
} else {
    std::tie(legal, nary, pary, nplace, pplace) = 
        is_legal(cur_nmos, cur_pmos, cur_np, cur_pp, occupy[i], empty[j]);
}

// ... 中间代码保持不变 ...

// TODO 2: 计算分数
auto eval0 = evaluator(w_ref, nets, pins, cur_pmos, cur_nmos, cur_pp, cur_np);
double s0 = std::get<0>(eval0);

auto eval1 = evaluator(w_ref, nets, pins, new_pary, new_nary, new_pp2, new_np2);
double s1 = std::get<0>(eval1);

// delta 计算已在代码中
double delta = s1 - s0;
bool accept = false;

// TODO 3: Metropolis 接受准则
if (delta > 0) {
    accept = true;
} else {
    double prob = std::exp(delta / t);
    if (dist01(rng) < prob) {
        accept = true;
    }
}

// TODO 4: 接受后更新当前解
if (accept) {
    cur_pmos = new_pary;
    cur_nmos = new_nary;
    cur_pp = new_pp2;
    cur_np = new_np2;
    
    // 后续代码已提供...
}

// ...外层 while 循环末尾...

// TODO 5: 降温
t = t * decrease;
```

---

## 八、编译和运行

### 8.1 编译

```bash
python3 setup.py build
```

### 8.2 运行

```bash
python3 eda.py cells.spi AN2D2
```

### 8.3 评分

```bash
python3 evaluator.py AN2D2.json AN2D2 cells.spi
```

---

## 九、参数说明

在 `eda.py` 中可以调整的参数：

```python
t0 = float(mos_num) * 20000.0  # 起始温度，MOS数量 × 20000
tt = 0.1                        # 终止温度
decrease = 0.88                 # 降温因子
times = mos_num * 2000          # 每个温度下的迭代次数
```

- **t0 (起始温度)**：越高，初期接受差解的概率越大，探索范围越广
- **tt (终止温度)**：达到此温度时停止
- **decrease (降温因子)**：越接近1，降温越慢，搜索越充分但耗时更长
- **times (迭代次数)**：每个温度下尝试的次数，越大搜索越充分

---

## 十、总结

完成此实验，你需要：

1. **理解数据流**：输入布局 → 随机扰动 → 合法性检查 → 评分 → 接受/拒绝 → 降温 → 循环
2. **掌握函数调用**：
   - `is_legal()` - 检查移动合法性
   - `evaluator()` - 计算布局分数
   - `update_place_ary()` / `update_mos_ary()` - 更新布局
   - `compute()` - 获取占用/空位置列表
3. **实现 Metropolis 准则**：
   - 更好的解：直接接受
   - 更差的解：以 exp(Δ/T) 的概率接受
4. **实现降温**：`t = t * decrease`

祝实验顺利！
