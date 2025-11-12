## T_5_30
```matlab
% 5-30 连续时间信号的采样
clear; close all; clc;

fc = 10; % 原信号频率为10Hz
t_continuous = linspace(0, 1, 1000); 
xc_continuous = cos(2*pi*fc*t_continuous);

% (a) 采样频率 Fs = 40 Hz
Fs_a = 40; 
n_a = 0:39;
t_a = n_a/Fs_a;
x_a = cos(2*pi*fc*t_a);

% (b) 采样频率 Fs = 100Hz
Fs_b = 100;
n_b = 0:99;
t_b = n_b/Fs_b;
x_b = cos(2*pi*fc*t_b);

% (c) 采样频率 Fs = 4Hz
Fs_c = 4;
n_c = 0:3;
t_c = n_c / Fs_c;
x_c = cos(2*pi*fc*t_c);

t = tiledlayout(4,1, 'Padding','compact','TileSpacing','compact');

nexttile; 
plot(t_continuous, xc_continuous, 'k-', 'LineWidth', 0.5); 
grid on;
legend('原始信号');
title('原始连续信号');

nexttile; 
plot(t_continuous, xc_continuous, 'k-', 'LineWidth', 0.5); hold on;
stem(t_a, x_a, 'r', 'LineWidth', 1.5, 'MarkerSize', 4.5);
grid on;
legend('原始信号', '采样点');
title('(a) 采样频率 Fs = 40 Hz');


nexttile; 
plot(t_continuous, xc_continuous, 'k-', 'LineWidth', 0.5); hold on;
stem(t_b, x_b, 'g', 'LineWidth', 1.5, 'MarkerSize', 4.5);
grid on;
legend('原始信号', '采样点');
title('(b) 采样频率 Fs = 100 Hz');

nexttile; 
plot(t_continuous, xc_continuous, 'k-', 'LineWidth', 0.5); hold on;
stem(t_c, x_c, 'b', 'LineWidth', 1.5, 'MarkerSize', 4.5);
grid on;
legend('原始信号', '采样点');
title('(c) 采样频率 Fs = 4 Hz');
```

## T_5_32
```matlab
% 5-32 序列抽取与三次样条插值重构
clear; close all; clc;

% 原始序列
n = 0:39;
x = cos(0.2*pi*n);

% (a) x1[n] = x[2n] - 抽取因子为2
n1 = 0:19;
x1 = x(2*n1 + 1);

% (b) x2[n] = x[4n] - 抽取因子为4
n2 = 0:9;
x2 = x(4*n2 + 1);

% (c) x3[n] = x[8n] - 抽取因子为8
n3 = 0:4;
x3 = x(8*n3 + 1);

% 样条插值 \delta t
t_inter = linspace(0, 39, 1000);
y = spline(n,x,t_inter);

t_inter1 = linspace(0, 19, 1000);
y1 = spline(n1,x1,t_inter1);

t_inter2 = linspace(0, 9, 1000);
y2 = spline(n2,x2,t_inter2);

t_inter3 = linspace(0, 4, 1000);
y3 = spline(n3,x3,t_inter3);

fig1 = tiledlayout(4,1, 'Padding','compact','TileSpacing','compact');

nexttile; 
stem(n, x, 'k', 'LineWidth', 1, 'MarkerSize', 4.5); hold on;
plot(t_inter, y, 'r-', 'LineWidth', 0.5);
grid on;
legend('原始信号', '插值重构信号');
title('x[n]');

nexttile; 
stem(n1, x1, 'k', 'LineWidth', 1, 'MarkerSize', 4.5); hold on;
plot(t_inter1, y1, 'r-', 'LineWidth', 0.5);
grid on;
legend('原始信号', '插值重构信号');
title('x_{1}[n]');

nexttile; 
stem(n2, x2, 'k', 'LineWidth', 1, 'MarkerSize', 4.5); hold on;
plot(t_inter2, y2, 'r-', 'LineWidth', 0.5);
grid on;
legend('原始信号', '插值重构信号');
title('x_{2}[n]');

nexttile; 
stem(n3, x3, 'k', 'LineWidth', 1, 'MarkerSize', 4.5); hold on;
plot(t_inter3, y3, 'r-', 'LineWidth', 0.5);
grid on;
legend('原始信号', '插值重构信号');
title('x_{3}[n]');
```

## T_6_41
```matlab
% 6-41 DFT与频域采样关系验证
clear; close all; clc;

% 已知序列
x = [4, 3, 2, 1, 2, 3, 4];
n = 0:6;
N = length(x);

% (a) 利用频率响应求解傅里叶变换
[X,w] = freqz(x, 1, 2048, 'whole');

% (b) 计算32点DFT，并验证频域取样关系
N_dft = 32;
X_dft = fft(x, N_dft);
k = 0:N_dft-1;
w_dft = 2*pi*k/N_dft; % DFT对应的频率点

figure('Position', [100, 100, 1200, 400]);
figab = tiledlayout(1,2, 'Padding','compact','TileSpacing','compact');  % 创建 2 行 1 列的网格布局，压缩边距与间距，便于紧凑显示两幅图。
% figure 1
nexttile; 
plot(w, abs(X)); hold on;
% stem(w_dft, abs(X_dft));
grid on; 
xlim([0 2*pi]);
xticks(0:0.5*pi:2*pi);
xticklabels(string(0:0.5:2) + "\pi");
xlabel('\omega'); 
legend('|X(e^{j\omega)}|','|X[k]|')
title(['幅度曲线']);

% figure 2
nexttile; 
plot(w, unwrap(angle(X)));   % unwrap 去除 2π 跳变，使相位连续
hold on;
% stem(w_dft, angle(X_dft));
grid on; 
xlim([0 2*pi]);
xticks(0:0.5*pi:2*pi);
xticklabels(string(0:0.5:2) + "\pi");
xlabel('\omega'); 
legend('\angle X(e^{j\omega})', '\angle X[k]'); 
title(['相位曲线']);

% (c) 利用IDFT计算重构后的信号，验证验证DFT和IDFT的唯一性
x_reconstructed = ifft(X_dft, N_dft);

figure('Position', [100, 100, 1200, 400]);
figc = tiledlayout(1,1, 'Padding','compact','TileSpacing','compact');
nexttile; 
stem(n,x, 'b', 'LineWidth', 2, 'MarkerSize', 6); hold on;
stem(0:N_dft - 1, x_reconstructed, 'r', 'LineWidth', 1, 'MarkerSize', 4.5);
xlabel('n');
legend('原始信号', 'IDFT得到的信号');

figure('Position', [100, 100, 1200, 400]);
figc2 = tiledlayout(1,2, 'Padding','compact','TileSpacing','compact');
nexttile; 
stem(n,x, 'b', 'LineWidth', 2, 'MarkerSize', 6);
xlabel('n');
ylabel('x[n]')
legend('原始信号');

nexttile;
stem(0:N_dft - 1, x_reconstructed, 'r', 'LineWidth', 1, 'MarkerSize', 4.5);
xlabel('n');
ylabel('x_{r}[n]');
legend('重构后的信号');
```

## T_6_42
```matlab
% 6-42 DFT的时移和调制性质
clear; close all; clc;

% (a) x1[n] = 0.2^n, 0 ≤ n ≤ 9
n = 0:9;
N_dft = 10;
x1 = 0.2.^n;
disp("x1:");
disp(x1);

% (b) x2[n] = x1[((n-3))_10] - 循环右移3
x2 = circshift(x1, 3);
disp("x2:");
disp(x2);

% (c) x3[n] = x1[n] * exp(j*0.4*pi*n)
x3 = x1 .* exp(1j*0.4*pi*n);
disp("x3:");
disp(x3);

% 计算10点DFT
X1 = fft(x1, N_dft);
X2 = fft(x2, N_dft);
X3 = fft(x3, N_dft);

% x1的10点DFT的幅度曲线和相位曲线
figure('Position', [100, 100, 1200, 400]);
fig1 = tiledlayout(1,2, 'Padding','compact','TileSpacing','compact');
nexttile; 
stem(0:N_dft-1,abs(X1));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('|X1[k]|')
legend('幅度');
nexttile; 
stem(0:N_dft-1,angle(X1));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('\angle X1[k]')
legend('相位');

% x2的10点DFT的幅度曲线和相位曲线
figure('Position', [100, 100, 1200, 400]);
fig2 = tiledlayout(1,2, 'Padding','compact','TileSpacing','compact');
nexttile; 
stem(0:N_dft-1,abs(X2));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('|X2[k]|')
legend('幅度');
nexttile; 
stem(0:N_dft-1,angle(X2));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('\angle X2[k]')
legend('相位');

% x3的10点DFT的幅度曲线和相位曲线
figure('Position', [100, 100, 1200, 400]);
fig3 = tiledlayout(1,2, 'Padding','compact','TileSpacing','compact');
nexttile; 
stem(0:N_dft-1,abs(X3));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('|X3[k]|')
legend('幅度');
nexttile; 
stem(0:N_dft-1,angle(X3));
xlabel('$n/ \frac{2\pi}{10}$','Interpreter', 'latex');
ylabel('\angle X3[k]')
legend('相位');
```