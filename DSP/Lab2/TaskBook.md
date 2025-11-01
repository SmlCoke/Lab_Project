# TaskBook
## 3-31
### 题目内容
画出下列序列傅里叶变换的幅度和相位。
(a) $x[n] = \{4,3,2,1,2,3,4\}$, $n = \{0,1,2,3,4,5,6\}$;
(b) $x[n] = \{4,3,2,1,0,-1,-2,-3,-4\}$, $n = \{0,1,2,3,4,5,6,7,8\}$。
注意观察幅度和相位的对称性。
(提示: 可以调用的函数有 `fplot()`、`abs()`、`angle()` 或 `freqz()`、`exp()` 等)

### 实验结果
3-31(a)的MATLAB仿真图像见：
![alt text](3-31(a).png)
3-31(b)的MATLAB仿真图像见：
![alt text](3-31(b).png)

### 实验分析
这两个序列都是实值序列：
##### 幅度对称性
$y[n]=x[n+3]$是实值序列，则$Y(e^{j\omega})$满足：
$$Y(e^{j\omega})=Y(e^{-j\omega})$$
因此$$|Y(e^{j\omega})|=|Y(e^{-j\omega})|$$
因此$$|e^{j3\omega}X(e^{j\omega})|=|e^{-j3\omega}X(e^{-j\omega})|$$
因此：$$|X(e^{j\omega})|=|X(e^{-j\omega})|$$
因此$|X(e^{j\omega})|$关于$x=0(+2k\pi)$偶对称，又：
$$|X(e^{j(\pi-\omega)})|=|X(e^{j(-\pi-\omega)})|=|X(e^{j(\pi+\omega)})|$$
因此$|X(e^{j\omega})|$关于$x=\pi(+2k\pi)$偶对称
综上所述：$|X(e^{j\omega})|$关于$x=k\pi$**偶对称**

##### 相位对称性
$Y(e^{j\omega})$满足：
$$\angle [Y(e^{j\omega})]=-\angle [Y(e^{-j\omega})]$$
即：
$$ 3\omega + \angle[X(e^{j\omega})]=-\angle[X(e^{-j\omega})]-(-3\omega)$$
即：
$$\angle [X(e^{j\omega})]=-\angle [X(e^{-j\omega})]$$
因此，与幅度对称性的分析相同，很容易发现：
$\angle[X(e^{j\omega})]$关于$x=k\pi$**奇对称**

##### 广义线性相位序列
此外，我们发现，这两个序列分别关于$x=3$和$x=4$呈偶对称和奇对称，其代表的系统分别是I类系统和III类系统，其频率响应分别是：
$$3-31(a): X(e^{j\omega})=e^{-j\omega\frac{M}{2}}\sum_{n=0}^{M}x[n]\cos[\omega(n-\frac{M}{2})]$$
和：
$$3-31(b): X(e^{j\omega})=e^{-j\omega\frac{M}{2}+j\frac{\pi}{2}}\sum_{n=0}^{M}x[n]\cos[\omega(n-\frac{M}{2})+\frac{\pi}{2}]$$
，可以发现，则两个序列的傅里叶变换的相位响应的斜率一定是：-3和-4，与图中相同。

---
## 3-34
### 题目内容
画出以下周期序列的 DFS 和傅里叶变换，其中 $N$ 为周期。
(a) $\tilde{x}[n] = \cos(0.8\pi n) + \cos(0.1\pi n)$
(b) $\tilde{x}[n] = \{0,0,1,0,0\}$, $N=5$
(c) $\tilde{x}[n] = \{3,-3,3,-3\}$, $N=4$

### 实验结果
3-34(a)的MATLAB仿真图像（DFS的幅度和相位以及DTFT的幅度和相位）见：
![alt text](<3-34(a) N=20.png>)

3-34(b)的MATLAB仿真图像（DFS的幅度和相位以及DTFT的幅度和相位）见：
![alt text](<3-34(b) N=5.png>)

3-34(c)的MATLAB仿真图像（DFS的幅度和相位以及DTFT的幅度和相位）见：
![alt text](<3-34(c) N=4.png>)

### 实验分析
本节主要分析周期离散时间信号的DFS与DTFT的计算及其关系：
#### DFS的理论值
1. 3-34(a)：
$\tilde{x}[n] = \cos(0.8\pi n) + \cos(0.1\pi n)=\frac{1}{2}(e^{j0.8\pi n}+e^{-j0.8\pi n}+e^{j0.1\pi n}+e^{-j0.1\pi n}) = \frac{1}{N}\times 10 (e^{j\frac{2\pi}{N} 8n}+e^{-j\frac{2\pi}{N} 8 n}+e^{j\frac{2\pi}{N}  n}+e^{-j\frac{2\pi}{N} n})$
因此可以发现：
$$\tilde{X}[k]=\sum_{k=-\infty}^{+\infty}\delta[k-8-20k]+\delta[k+8-20k]+\delta[k-1-20k]+\delta[k+1-20k]$$
对应图3-34(a)，DFS的幅度在0~19范围内只在1，8，12，19这四个离散点出现。
2. 3-34(b)
$$\tilde{X}[k]=\sum_{n=0}^{N}\tilde{x}[n]e^{-j\frac{2\pi}{N}kn}=e^{-j0.8\pi k}$$
对应图3-34(b)，DFS的幅度在0~4范围内全为1
3. 3-34(c)
$$\tilde{X}[k]=\sum_{n=0}^{N}\tilde{x}[n]e^{-j\frac{2\pi}{N}kn}=3(1-j^{-k}+(-1)^k-j^k)$$
满足在$k \in [0,3]$范围内，$\tilde{X}[k]$只在$k=3$处取$\tilde{X}[3]=12$，其余点全为0。此外，我们可以发现对于任意$k$，$\tilde{X}[k]$恒为非负实数，因此相位恒为0。符合图3-34(c)中的情况

#### 周期离散时间信号的DTFT与DFS的关系
我们假设周期离散时间信号$\tilde{x}[n]$的DFS为: $\tilde{X}[k]$，则其DTFT为：
$$\mathcal{F}\{\tilde{x}[n]\}=\frac{2\pi}{N}\sum_{k=-\infty}^{\infty}\tilde{X}[k]\delta(\omega-k\cdot\frac{2\pi}{N})$$
可见，周期离散时间信号的DTFT相当于是在其DFS频谱上幅度倍乘了$\frac{2\pi}{N}$倍，而相位保持不变，这与3-34的三张图中的情况完全一致。

---

## 4-38
回声系统的差分方程是 $y[n] = x[n] + 0.5x[n-10]$，画出其零极点图、幅度响应和群延迟。
(提示: 可以调用的函数有 `zplane()`，`freqz()`，`grpdelay()` 等)
### 实验结果
![alt text](<4-38 回声系统.png>)
### 实验分析
原系统的系统函数：
$$H(z)=1+\frac{1}{2}z^{-10}$$
令$H(z)=0: z^{10}=-\frac{1}{2}$
解的：
$$z_k=(\frac{1}{2})^{1/10}e^{j(\pi + k\cdot 2\pi)/N}, k=0,1,2,...,9$$
因此零点必然环绕在圆: $r=(\frac{1}{2})^{1/10}$附近，这与图4-38中的零极点图相同。

频率响应为：$$H(e^{j\omega})=1+\frac{1}{2}e^{-j10\omega}$$
幅度响应：$$|H(e^{j\omega})|=\sqrt{(1+\frac{1}{2}\cos{10\omega})^2+\frac{1}{4}\sin^2{10\omega}}$$
相位响应：$$\angle [H(e^{j\omega})] = \arctan \frac{-1/2\sin{10\omega}}{1+1/2\cos{10\omega}}$$
群延迟：$$\text{grd} [H(e^{j\omega})] = ...$$

---

## 4-39
### 题目内容
已知滑动平均系统的单位脉冲响应是 $h_M[n] = \frac{1}{M}R_M[n]$，其延迟互补系统的单位脉冲响应是
$$
g_M[n] = \frac{\sin\left[\pi\left(n - \frac{M-1}{2}\right)\right]}{\pi\left(n - \frac{M-1}{2}\right)} - h_M[n]
$$
分别画出当 $M=2$、$3$、$4$ 和 $5$ 时两个系统的零极点图、幅度响应和相位响应。分别是哪类广义线性相位 FIR 系统？
(提示: 可以调用的函数有 `zplane()` 和 `freqz()` 等)

### 实验结果


### 实验分析
已知对于任意: $M \geq 1$，序列: $\text{sinc}[\pi(n - \frac{M-1}{2})]$和$h_{M}[n]$均关于$n=\frac{M-1}{2}$偶对称，因此序列$g_{M}[n]$也关于$n=\frac{M-1}{2}$偶对称。并且：
1. 当 $M$ 为偶数，即$M=2,4$时，满足$x[n] = x[M-1-n]$，$M-1$是奇数，因此两个系统都是II类系统
2. 当 $M$ 为奇数，即$M=3,5$时，满足$x[n] = x[M-1-n]$，$M-1$是偶数，因此两个系统都是I类系统
