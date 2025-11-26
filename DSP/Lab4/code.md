### 7-25
```matlab
%% 7-25 实数序列的FFT运算
% x[n] = n/10 + 0.2^n + 4*cos(0.2*pi*n), 0 <= n <= 31
clear; clc; close all;

n = 0:31;
x = n/10 + 0.2.^n + 4*cos(0.2*pi*n);

%% (a) 采用32点FFT运算，求出并画出其32点DFT的实部和虚部
X_32 = fft(x, 32);

figure('Name', '7-25(a) 32点DFT', 'NumberTitle','off');
t = tiledlayout(2,1, 'Padding','compact','TileSpacing','compact');

nexttile;
stem(0:31, real(X_32), 'filled');
grid on;
xlabel('k');
ylabel('Re\{X[k]\}');
title('32点DFT的实部');

nexttile;
stem(0:31, imag(X_32), 'filled');
grid on;
xlabel('k');
ylabel('Im\{X[k]\}');
title('32点DFT的虚部');

%% (b) 对(a)的结果再采用32点FFT运算，求出并画出x[n]
% IFFT = (1/N) * conj(FFT(conj(X)))，也可以直接用ifft
x_recover = ifft(X_32, 32);

figure('Name', '7-25(b) IFFT恢复x[n]', 'NumberTitle','off');
t = tiledlayout(2,1, 'Padding','compact','TileSpacing','compact');

nexttile;
stem(0:31, x, 'filled');
grid on;
xlabel('n');
ylabel('x[n]');
title('原始信号 x[n]');

nexttile;
stem(0:31, real(x_recover), 'filled');
grid on;
xlabel('n');
ylabel('x_{recover}[n]');
title('IFFT恢复的信号');

%% (c) 采用一次16点FFT运算，求出并画出x[n]的32点DFT的实部和虚部
% 利用实序列DFT的性质：将x[n]分成偶数点和奇数点
% 构造复序列 y[n] = x[2n] + j*x[2n+1]
% 然后用Y[k]恢复X[k]
x_even = x(1:2:32);  % x[0], x[2], ..., x[30]
x_odd = x(2:2:32);   % x[1], x[3], ..., x[31]
y = x_even + 1j*x_odd;  % 16点复序列

Y = fft(y, 16);  % 16点FFT

% 利用DFT性质恢复32点DFT
% X[k] = (1/2)*(Y[k] + conj(Y[N-k])) - (j/2)*e^{-j*2*pi*k/2N}*(Y[k] - conj(Y[N-k]))
% 其中 N = 16, 2N = 32
X_32_from16 = zeros(1, 32);
for k = 0:31
    k16 = mod(k, 16);  % k mod 16
    k16_neg = mod(16 - k16, 16);  % (-k) mod 16，用于DFT共轭对称性
    
    W = exp(-1j*2*pi*k/32);  % 旋转因子
    
    % 偶数部分DFT: X_even[k] = (Y[k mod 16] + conj(Y[(-k) mod 16])) / 2
    X_even = (Y(k16+1) + conj(Y(k16_neg+1))) / 2;
    % 奇数部分DFT: X_odd[k] = (Y[k mod 16] - conj(Y[(-k) mod 16])) / (2j)
    X_odd = (Y(k16+1) - conj(Y(k16_neg+1))) / (2j);
    
    % X[k] = X_even[k] + W^k * X_odd[k]
    X_32_from16(k+1) = X_even + W * X_odd;
end

figure('Name', '7-25(c) 16点FFT求32点DFT', 'NumberTitle','off');
t = tiledlayout(2,1, 'Padding','compact','TileSpacing','compact');

nexttile;
stem(0:31, real(X_32_from16), 'filled');
grid on;
xlabel('k');
ylabel('Re\{X[k]\}');
title('32点DFT的实部 (由16点FFT计算)');

nexttile;
stem(0:31, imag(X_32_from16), 'filled');
grid on;
xlabel('k');
ylabel('Im\{X[k]\}');
title('32点DFT的虚部 (由16点FFT计算)');

% 验证结果
disp('(c)与(a)结果的最大误差:');
disp(max(abs(X_32 - X_32_from16)));
```

---

### 7-26
```matlab
%% 7-26 线性卷积的直接计算和FFT方法
clear; clc; close all;

%% (a) x1[n] = R_5[n], x2[n] = (-1)^n * R_7[n]
x1a = ones(1, 5);  % R_5[n]
n2a = 0:6;
x2a = (-1).^n2a;  % (-1)^n * R_7[n]

% 直接计算线性卷积
ya_direct = conv(x1a, x2a);
na_direct = 0:(length(ya_direct)-1);

% FFT方法计算线性卷积
% 补零到长度 L >= N1 + N2 - 1 = 5 + 7 - 1 = 11
L_a = length(x1a) + length(x2a) - 1;
X1a = fft(x1a, L_a);
X2a = fft(x2a, L_a);
Ya = X1a .* X2a;
ya_fft = ifft(Ya);
na_fft = 0:(L_a-1);

figure('Name', '7-26(a) 线性卷积', 'NumberTitle','off');
t = tiledlayout(2,2, 'Padding','compact','TileSpacing','compact');

nexttile;
stem(0:4, x1a, 'filled');
grid on;
xlabel('n');
ylabel('x_1[n]');
title('x_1[n] = R_5[n]');

nexttile;
stem(n2a, x2a, 'filled');
grid on;
xlabel('n');
ylabel('x_2[n]');
title('x_2[n] = (-1)^n R_7[n]');

nexttile;
stem(na_direct, ya_direct, 'filled');
grid on;
xlabel('n');
ylabel('y[n]');
title('直接计算 conv(x_1, x_2)');

nexttile;
stem(na_fft, real(ya_fft), 'filled');
grid on;
xlabel('n');
ylabel('y[n]');
title('FFT方法计算卷积');

%% (b) x1[n] = {2,1,1,2} (n=0位置标记), x2[n] = 0.5^n * R_5[n]
x1b = [2 1 1 2];  % n = 0, 1, 2, 3
n2b = 0:4;
x2b = 0.5.^n2b;  % 0.5^n * R_5[n]

% 直接计算线性卷积
yb_direct = conv(x1b, x2b);
nb_direct = 0:(length(yb_direct)-1);

% FFT方法计算线性卷积
L_b = length(x1b) + length(x2b) - 1;
X1b = fft(x1b, L_b);
X2b = fft(x2b, L_b);
Yb = X1b .* X2b;
yb_fft = ifft(Yb);
nb_fft = 0:(L_b-1);

figure('Name', '7-26(b) 线性卷积', 'NumberTitle','off');
t = tiledlayout(2,2, 'Padding','compact','TileSpacing','compact');

nexttile;
stem(0:3, x1b, 'filled');
grid on;
xlabel('n');
ylabel('x_1[n]');
title('x_1[n] = \{2,1,1,2\}');

nexttile;
stem(n2b, x2b, 'filled');
grid on;
xlabel('n');
ylabel('x_2[n]');
title('x_2[n] = 0.5^n R_5[n]');

nexttile;
stem(nb_direct, yb_direct, 'filled');
grid on;
xlabel('n');
ylabel('y[n]');
title('直接计算 conv(x_1, x_2)');

nexttile;
stem(nb_fft, real(yb_fft), 'filled');
grid on;
xlabel('n');
ylabel('y[n]');
title('FFT方法计算卷积');

% 验证两种方法的结果
disp('7-26(a) 两种方法的最大误差:');
disp(max(abs(ya_direct - real(ya_fft))));
disp('7-26(b) 两种方法的最大误差:');
disp(max(abs(yb_direct - real(yb_fft))));
```

---

### 8-30
```matlab
%% 8-30 脉冲响应不变法设计巴特沃思低通IIR滤波器
% 通带截止频率 ωp = 0.4π rad
% 阻带截止频率 ωs = 0.5π rad
% 通带最多衰减 αp = 3dB
% 阻带最小衰减 αs = 40dB
% Td = 1
clear; clc; close all;

% 设计参数
Td = 1;                    % 采样周期
wp = 0.4*pi;               % 离散时间通带截止频率 (rad)
ws = 0.5*pi;               % 离散时间阻带截止频率 (rad)
Rp = 3;                    % 通带最大衰减 (dB)
Rs = 40;                   % 阻带最小衰减 (dB)

% 将数字频率转换为模拟频率（脉冲响应不变法）
% Ω = ω / Td
Wp_analog = wp / Td;       % 模拟通带截止频率 (rad/s)
Ws_analog = ws / Td;       % 模拟阻带截止频率 (rad/s)

% 确定巴特沃思滤波器阶数和截止频率
[N, Wc] = buttord(Wp_analog, Ws_analog, Rp, Rs, 's');
fprintf('巴特沃思滤波器阶数: N = %d\n', N);
fprintf('模拟截止频率: Wc = %.4f rad/s\n', Wc);

% 设计模拟巴特沃思滤波器
[b_s, a_s] = butter(N, Wc, 's');

% 显示模拟滤波器系统函数
disp('模拟滤波器分子系数 (b_s):');
disp(b_s);
disp('模拟滤波器分母系数 (a_s):');
disp(a_s);

% 脉冲响应不变法转换为数字滤波器
[b_z, a_z] = impinvar(b_s, a_s, 1/Td);

% 显示数字滤波器系统函数
disp('数字滤波器分子系数 (b_z):');
disp(b_z);
disp('数字滤波器分母系数 (a_z):');
disp(a_z);

% 绘图
figure('Name', '8-30 巴特沃思滤波器设计', 'NumberTitle','off');
t = tiledlayout(2,2, 'Padding','compact','TileSpacing','compact');

% 模拟滤波器对数幅度响应
nexttile;
w_analog = linspace(0, 3*Ws_analog, 1024);
[H_s, w_s] = freqs(b_s, a_s, w_analog);
plot(w_s, 20*log10(abs(H_s)));
grid on;
xlabel('\Omega (rad/s)');
ylabel('幅度 (dB)');
title('模拟滤波器对数幅度响应');
xlim([0 3*Ws_analog]);
ylim([-80 5]);
hold on;
xline(Wp_analog, 'r--', '\Omega_p');
xline(Ws_analog, 'g--', '\Omega_s');
yline(-Rp, 'b--', '-R_p');
yline(-Rs, 'm--', '-R_s');
hold off;

% 数字滤波器对数幅度响应
nexttile;
[H_z, w_z] = freqz(b_z, a_z, 1024);
plot(w_z/pi, 20*log10(abs(H_z)));
grid on;
xlabel('\omega/\pi');
ylabel('幅度 (dB)');
title('数字滤波器对数幅度响应');
xlim([0 1]);
ylim([-80 5]);
hold on;
xline(wp/pi, 'r--', '\omega_p/\pi');
xline(ws/pi, 'g--', '\omega_s/\pi');
yline(-Rp, 'b--', '-R_p');
yline(-Rs, 'm--', '-R_s');
hold off;

% 模拟滤波器单位脉冲响应
nexttile;
sys_s = tf(b_s, a_s);
[h_s, t_s] = impulse(sys_s);
plot(t_s, h_s);
grid on;
xlabel('t (s)');
ylabel('h(t)');
title('模拟滤波器单位脉冲响应');

% 数字滤波器单位脉冲响应
nexttile;
[h_z, n_z] = impz(b_z, a_z, 50);
stem(n_z, h_z, 'filled');
grid on;
xlabel('n');
ylabel('h[n]');
title('数字滤波器单位脉冲响应');
```

---

### 8-32
```matlab
%% 8-32 切比雪夫II型离散时间IIR高通滤波器设计
% 阻带截止频率 ωp = 0.6π rad (注意：题目中阻带截止频率标为ωp)
% 通带截止频率 ωs = 0.7π rad (注意：题目中通带截止频率标为ωs)
% 通带最大衰减 αp = 3dB
% 阻带最小衰减 αs = 40dB
% 分别采用脉冲响应不变法和双线性变换法
clear; clc; close all;

% 设计参数（高通滤波器）
ws = 0.6*pi;               % 阻带截止频率 (rad)
wp = 0.7*pi;               % 通带截止频率 (rad)
Rp = 3;                    % 通带最大衰减 (dB)
Rs = 40;                   % 阻带最小衰减 (dB)

%% 方法一：脉冲响应不变法
% 注意：脉冲响应不变法不适合设计高通滤波器，因为会产生频谱混叠
Td = 1;  % 采样周期

% 将数字频率转换为模拟频率
Ws_analog = ws / Td;
Wp_analog = wp / Td;

% 确定切比雪夫II型滤波器阶数
[N1, Wn1] = cheb2ord(Wp_analog, Ws_analog, Rp, Rs, 's');
fprintf('脉冲响应不变法 - 滤波器阶数: N = %d\n', N1);

% 设计模拟切比雪夫II型高通滤波器
[b_s1, a_s1] = cheby2(N1, Rs, Wn1, 'high', 's');

% 脉冲响应不变法转换
% 注意：impinvar函数主要用于低通滤波器，高通滤波器会有问题
[b_z1, a_z1] = impinvar(b_s1, a_s1, 1/Td);

%% 方法二：双线性变换法
% 预畸变
Wp_prewarp = 2*tan(wp/2);   % 预畸变后的通带频率
Ws_prewarp = 2*tan(ws/2);   % 预畸变后的阻带频率

% 确定切比雪夫II型滤波器阶数
[N2, Wn2] = cheb2ord(Wp_prewarp, Ws_prewarp, Rp, Rs, 's');
fprintf('双线性变换法 - 滤波器阶数: N = %d\n', N2);

% 设计模拟切比雪夫II型高通滤波器
[b_s2, a_s2] = cheby2(N2, Rs, Wn2, 'high', 's');

% 双线性变换
[b_z2, a_z2] = bilinear(b_s2, a_s2, 1);

%% 或者直接使用数字滤波器设计函数
% 直接设计数字切比雪夫II型高通滤波器（双线性变换法）
[N_direct, Wn_direct] = cheb2ord(wp/pi, ws/pi, Rp, Rs);
[b_z_direct, a_z_direct] = cheby2(N_direct, Rs, Wn_direct, 'high');
fprintf('直接设计 - 滤波器阶数: N = %d\n', N_direct);

%% 绘图比较
figure('Name', '8-32 切比雪夫II型高通滤波器', 'NumberTitle','off');
t = tiledlayout(2,1, 'Padding','compact','TileSpacing','compact');

% 脉冲响应不变法的对数幅度响应
nexttile;
[H_z1, w1] = freqz(b_z1, a_z1, 2048);
plot(w1/pi, 20*log10(abs(H_z1)), 'b', 'LineWidth', 1.5);
grid on;
xlabel('\omega/\pi');
ylabel('幅度 (dB)');
title('脉冲响应不变法 - 对数幅度响应');
xlim([0 1]);
ylim([-80 10]);
hold on;
xline(ws/pi, 'r--', '\omega_s/\pi');
xline(wp/pi, 'g--', '\omega_p/\pi');
yline(-Rp, 'b--', '-R_p');
yline(-Rs, 'm--', '-R_s');
hold off;

% 双线性变换法的对数幅度响应
nexttile;
[H_z2, w2] = freqz(b_z_direct, a_z_direct, 2048);
plot(w2/pi, 20*log10(abs(H_z2)), 'r', 'LineWidth', 1.5);
grid on;
xlabel('\omega/\pi');
ylabel('幅度 (dB)');
title('双线性变换法 - 对数幅度响应');
xlim([0 1]);
ylim([-80 10]);
hold on;
xline(ws/pi, 'r--', '\omega_s/\pi');
xline(wp/pi, 'g--', '\omega_p/\pi');
yline(-Rp, 'b--', '-R_p');
yline(-Rs, 'm--', '-R_s');
hold off;

% 两种方法对比图
figure('Name', '8-32 两种方法对比', 'NumberTitle','off');
[H_z1, w1] = freqz(b_z1, a_z1, 2048);
[H_z2, w2] = freqz(b_z_direct, a_z_direct, 2048);
plot(w1/pi, 20*log10(abs(H_z1)), 'b', 'LineWidth', 1.5);
hold on;
plot(w2/pi, 20*log10(abs(H_z2)), 'r', 'LineWidth', 1.5);
grid on;
xlabel('\omega/\pi');
ylabel('幅度 (dB)');
title('脉冲响应不变法 vs 双线性变换法');
xlim([0 1]);
ylim([-80 10]);
legend('脉冲响应不变法', '双线性变换法', 'Location', 'best');
xline(ws/pi, 'k--', '\omega_s/\pi');
xline(wp/pi, 'k--', '\omega_p/\pi');
hold off;

%% 分析说明
fprintf('\n========== 分析 ==========\n');
fprintf('脉冲响应不变法用于高通滤波器设计时，由于频谱混叠问题，\n');
fprintf('会导致滤波器性能下降，无法满足设计指标。\n');
fprintf('双线性变换法不存在频谱混叠问题，适合设计各种类型的滤波器。\n');
```
