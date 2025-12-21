## 计算
### 1.1 第一根钉子：补偿电容$C_c$
$C_c \geq 0.22 C_L \geq 2.2pF$
我们直接取$C_c = 3pF$

### 1.2 第二根钉子：由GBW确定$g_{m1} = g_{m2} = g_{mI}$
$g_{mI} = 2\pi f_u C_c \geq \times 2\pi 40MHz \times 2.2pF = 552.92\mu S$
我们直接取$C_c = 3pF, f_u = 50MHz$
得到$g_{mI} = 942.47 \mu S$

### 1.3 根据$g_m/I_D$关系确定M1, M2晶体管电流量级
$g_{mI}/I_D \geq 15$
我们取$g_{mI}/I_{D} = 18$
$I_D = 942.47/18 = 52.35 \mu A$
> 极限值：$552.92\mu S / 15 = 36.86\mu A$

### 1.4 确定尾电流
$I_{tail} = 2I_{D} = 104.7 \mu A$
> 极限值：$I_{tail} = 73.72\mu A$

### 1.5 检查压摆率
$SR = I_{tail}/C_c = 34.9 V/\mu S > 10\mu S$

### 1.6 $g_{m6}$

$g_{m6} \ge 2.2 \cdot g_{m1} \cdot \frac{C_L}{C_c} = 2.2\times 942.47\mu S \times 10/3 = 6.22m S$
我们取：$g_{m6} = 2.2\times 1.03\times 10/3 = 7.5m S$
### 1.7 第二级电路的尾电流
$I_D \geq 6.22m S/15 = 414.7 \mu A$
我们取$I_{D} = 7.5 mS/ 18 = 416.7\mu A$