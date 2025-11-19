# Equation temp file

## 组合逻辑门中的性能优化
$$
\begin{aligned}
t_{p(\text{Gate})} & = 0.69R_{\text{eq(Gate)}}(C_{\text{int(Gate)}}+C_{\text{ext(Gate)}}) \\
& = 0.69R_{\text{eq(Gate)}}C_{\text{int(Gate)}}(1+\frac{C_{\text{ext(Gate)}}}{C_{\text{int(Gate)}}})\\
& = 0.69R_{\text{eq(inv)}}[pC_{\text{int(inv)}}][1+\frac{C_{\text{g(Gate)}}}{C_{\text{g(inv)}}}\frac{C_{\text{ext(Gate)}}/C_{\text{g(Gate)}}}{C_{\text{int(Gate)}}/C_{\text{g(inv)}}}]\\
&=(0.69R_{\text{eq(inv)}}C_{\text{int(inv)}})p[1+\frac{C_{\text{g(Gate)}}}{C_{\text{g(inv)}}}\frac{C_{\text{ext(Gate)}}/C_{\text{g(Gate)}}}{p\cdot C_{\text{int(inv)}}/C_{\text{g(inv)}}}]\\
&=t_{p0}p(1+g\frac{f}{p\cdot \gamma})\\
&=t_{p0}(p+g\frac{f}{\gamma})
\end{aligned}
$$

$p=\frac{C_{\text{int(Gate)}}}{C_{\text{int(inv)}}}$

$h=gf=\frac{C_{\text{g(Gate)}}}{C_{\text{g(inv)}}}\cdot\frac{C_{\text{ext(Gate)}}}{C_{\text{g(Gate)}}}$

$g=\frac{C_{\text{g(Gate)}}}{C_{\text{g(inv)}}}$