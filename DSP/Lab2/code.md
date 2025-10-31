### 3-31
```matlab
%% 3-31 有限长序列的 DTFT 幅度与相位
%% 采用freqz(b, a, w)函数的方法求解DTFT
%% b分子系数，a分母系数，w采样的频率点个数
clear; clc; close all;
seqs = {
    [4 3 2 1 2 3 4],              '3-31(a)';
    [4 3 2 1 0 -1 -2 -3 -4],      '3-31(b)';
};

for i = 1:size(seqs,1)
    x = seqs{i,1}; 
    label = seqs{i,2};
    [X, w] = freqz(x, 1, 4096, 'whole');   % 用 freqz 计算"以 x 为 FIR 系数（分子），分母为 1"的频响。

    figure('Name', label, 'NumberTitle','off');                         % 新建图窗，名称用 label，且不显示默认编号。
    t = tiledlayout(2,1, 'Padding','compact','TileSpacing','compact');  % 创建 2 行 1 列的网格布局，压缩边距与间距，便于紧凑显示两幅图。
    % figure 1
    nexttile; 
    plot(w, abs(X)); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    ylabel('|X(e^{j\omega})|');
    title([label ' 幅度']);

    % figure 2
    nexttile; 
    plot(w, unwrap(angle(X)));   % unwrap 去除 2π 跳变，使相位连续
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    ylabel('\angle X(e^{j\omega})'); 
    title([label ' 相位']);
end

```

---

### 3-34
```matlab
%% 3-34 周期序列的 DFS 与傅里叶变换(冲激谱)
% 说明：DFS 系数 X[k] = (1/N) * DFT{x[0..N-1]}。
% 周期序列的 DTFT 为在 ω_k=2πk/N 处的冲激，权重 2π X[k]。
clear; clc; close all;
cases = {
    20, @(n) cos(0.8*pi*n) + cos(0.1*pi*n), '3-34(a) N=20';
    5,  @(n) [0 0 1 0 0],                   '3-34(b) N=5';
    4,  @(n) [3 -3 3 -3],                   '3-34(c) N=4';
};

for i = 1:size(cases,1)
    N = cases{i,1};   % 周期
    f = cases{i,2};   % 序列
    name = cases{i,3}; % 序列名称
    n = 0:N-1; 
    x = f(n);            % 取出一段周期样本
    x = x(1:N);          % 一段周期样本
    Xk = fft(x);         % FFT(x)计算出一段周期样本信号的DFT系数，等效为该周期信号的傅里叶级数系数
    wk = 2*pi*(0:N-1)/N;

    figure('Name', name, 'NumberTitle','off');
    % DFS幅度
    t = tiledlayout(2,2, 'Padding','compact','TileSpacing','compact');
    nexttile; 
    stem(0:N-1, abs(Xk), 'filled'); 
    grid on;
    xlabel('k'); 
    title('|X[k]| (DFS)');

    % DFS 相位
    nexttile; 
    stem(0:N-1, angle(Xk), 'filled'); 
    grid on;
    xlabel('k'); 
    title('\angle X[k] (DFS)');

    % DTFT 幅度
    nexttile; 
    stem(wk, 2*pi/N*abs(Xk), 'filled'); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    title('|X(e^{j\omega})|');

    % DTFT 相位
    nexttile; 
    stem(wk, angle(Xk), 'filled'); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omeg a'); 
    title('\angle X(e^{j\omega})');
end

```
---

### 4-38
```matlab
%% 4-38 回声系统 y[n] = x[n] + 0.5 x[n-10]
clear; clc; close all;

b = [1, zeros(1,9), 0.5];  % 分子系数
a = 1;   % 分母系数

[H, w] = freqz(b, a, 2048, 'whole');      % freqz求解频率响应
[gd, wg] = grpdelay(b, a, 2048, 'whole'); % grpdelay求解群延迟

figure('Name','4-38 回声系统', 'NumberTitle','off');
t = tiledlayout(2,2, 'Padding','compact','TileSpacing','compact');

nexttile; 
zplane(b,a);   % zplane函数求解零极点图
grid on; 
title('零极点图');

nexttile; 
plot(w, abs(H)); 
grid on; xlim([0 2*pi]);
xlabel('\omega');  
title('幅度响应');

nexttile; 
plot(w, unwrap(angle(H))); 
grid on; 
xlim([0 2*pi]);
xlabel('\omega'); 
title('相位响应');

nexttile; 
plot(wg, gd); 
grid on; 
xlim([0 2*pi]);
xlabel('\omega'); 
ylabel('样点'); 
title('群延迟');

```

---

### 4-39
```matlab
% filepath: d:\MATLABap\Application\DSP\chap_solutions.m
%% 全局设置
clear; clc; close all;

%% 4-39 滑动平均系统与其延迟互补系统
% h_M[n] = (1/M) * rect_M[n]
% g_M[n] = sinc(n-(M-1)/2) - h_M[n]（当 M 为奇数时 g_M 等价于 δ[n-(M-1)/2]-h_M[n]，为 FIR）
Mlist = 2:5;

for M = Mlist
    b = ones(1, M) / M;     % 滑动平均 FIR 系数
    seq = 0 : (M-1);
    disp('seq')
    disp(seq - (M-1)/2)
    b_g = sinc(seq - (M-1)/2) - b;
    disp(b_g)
    a = 1;
    [H, w] = freqz(b, a, 2048, 'whole');   % 0..2π

    [G, ww] = freqz(b_g, a, 2048, 'whole');

    figure('Name', sprintf('4-39_M=%d', M), 'NumberTitle','off');
    t = tiledlayout(2,3, 'Padding','compact','TileSpacing','compact');

    % h_M 零极点
    nexttile; 
    zplane(b, a); 
    grid on; 
    title(sprintf('h_{%d} 零极点',M));

    % h_M 幅度
    nexttile; 
    plot(w, abs(H)); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    title('|H_M(e^{j\omega})|');

    % h_M 相位
    nexttile; 
    plot(w, unwrap(angle(H))); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    title('\angle H_M(e^{j\omega})');

    % g_M 零极点图
    nexttile; 
    zplane(b_g, a); 
    grid on; 
    title(sprintf('g_{%d} 零极点',M));

    % g_M 幅度
    nexttile; 
    plot(w, abs(G)); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    title('|G_M(e^{j\omega})|');

    % g_M 相位
    nexttile; 
    plot(w, unwrap(angle(G))); 
    grid on; 
    xlim([0 2*pi]);
    xlabel('\omega'); 
    title('\angle G_M(e^{j\omega})');
end

%% 工具函数：归一化 sinc
function y = sincn(x)
% sin(pi x)/(pi x)，x=0 处定义为 1
y = ones(size(x));
idx = abs(x) > eps;   % 如果x=0，保持该点的初值：1
y(idx) = sin(pi*x(idx))./(pi*x(idx));
end
```