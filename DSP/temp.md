# Equation temp file

## FFT
我们考虑两个等长(N)实序列：$x_1[n], x_2[n]$
$$\begin{aligned}
\textbf{序列合并：} & y[n]  = x_1[n] + jx_2[n] \\
\text{N点DFT：} &Y[k] = \text{FFT}\{y[n]\} \\
\text{周期共轭对称分量：}& X_1[k] = \frac{Y[k]+Y^*[N-k]}{2} \\
\text{周期共轭反对称分量：}& X_2[k] = \frac{Y[k]-Y^*[N-k]}{2j}
\end{aligned}$$

我们考虑一个长度为N的实序列$x[n]$，做何种变换法可以降低计算量？
利用DIF-FFT第一次分解的原理：
$$\begin{aligned}
X[k] & = X_1[k] + W_N^k X_2[k] \\
X[k+N/2] & = X_1[k] - W_N^k X_2[k]
\end{aligned}
$$
其中$X_1[k]$和$X_2[k]$分别是$x[2n], x[2n+1]$的$N/2$点DFT，因此我们不妨构造：
$$
\begin{aligned}
\text{序列合并：} & y[n] = x_1[n] + jx_2[n] = x[2n] + jx[2n+1] \\
\frac{N}{2}\text{点DFT：} & Y[k] = \text{FFT}\{y[n]\} \\
\text{周期共轭对称分量：}&X_1[k] = \frac{Y[k]+Y^*[N/2-k]}{2} \\
\text{周期共轭反对称分量：}&X_2[k] = \frac{Y[k]-Y^*[N/2-k]}{2j} \\
\text{DFT合并：} & X[k] = \{X_1[k], X_2[k]\} 
\end{aligned}
$$

复杂度分析：复数乘法：$N/4\text{log}_2{N/2} + N/2$，复数加法：$N/2\text{log}_2{N/2} + N + N$


分析公式与综合公式：
$$
\begin{aligned}
\text{分析公式：}&X[k] = \sum_{n=0}^{N-1}x[n]W_{N}^{kn} \\
\text{综合公式：}&x[n] = \frac{1}{N}\sum_{k=0}^{N-1}X[k]W_{N}^{-kn}
\end{aligned}
$$

$$
\begin{aligned}
x[n] & = \frac{1}{N}\sum_{l=0}^{N-1}X[k]W_{N}^{-kn} \\
     & = \frac{1}{N}[\sum_{l=0}^{N-1}X^{*}[k]W_{N}^{kn}]^{*} \\
     & = \frac{1}{N}[\text{FFT}\{X^*[k]\}]^{*} \\
\end{aligned}
$$
