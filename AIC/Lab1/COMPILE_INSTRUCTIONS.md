# Lab1_report.tex 编译说明

## 文档概述
- **文件名**: Lab1_report.tex
- **文档类**: ctexart (中文LaTeX支持)
- **编码**: UTF-8
- **内容**: 模拟集成电路设计Lab1实验报告（10个任务）

## 编译方法

### 方法1：使用XeLaTeX (推荐)
```bash
xelatex Lab1_report.tex
xelatex Lab1_report.tex  # 运行两次以生成正确的交叉引用
```

### 方法2：使用pdfLaTeX
```bash
pdflatex Lab1_report.tex
pdflatex Lab1_report.tex  # 运行两次以生成正确的交叉引用
```

### 方法3：完整编译（如果有参考文献）
```bash
xelatex Lab1_report.tex
bibtex Lab1_report
xelatex Lab1_report.tex
xelatex Lab1_report.tex
```

## 系统要求

### 必需的LaTeX包
文档使用了以下LaTeX包（通常在完整TeX发行版中已包含）：
- amsmath - 数学公式支持
- cases - 分段函数支持
- cite - 参考文献支持
- graphicx - 图片插入支持
- enumerate - 枚举列表
- algorithm & algpseudocode - 算法伪代码
- caption - 图表标题
- geometry - 页面布局
- fancyhdr - 页眉页脚
- xcolor - 颜色支持
- ctex - 中文支持（重要！）

### TeX发行版推荐
- **Windows**: TeX Live 或 MiKTeX
- **macOS**: MacTeX
- **Linux**: TeX Live

## 文档结构

### 章节组织
1. 任务一：NMOS ID vs. VGS特性分析
2. 任务二：跨导gm vs. VGS特性分析
3. 任务三：gm/ID特性分析与最佳工作点
4. 任务四：ID vs. VGS and VDS三维特性分析
5. 任务五：NMOS关键参数提取与计算
6. 任务六：输出电阻ro的分析
7. 任务七：本征增益与尺寸优化分析
8. 任务八：CMOS反相器DC特性分析
9. 任务九：CMOS反相器尺寸优化
10. 任务十：CMOS反相器交直流与时域特性综合分析

### 统计数据
- **总章节数**: 10个主section
- **数学公式**: 34个equation环境
- **插图引用**: 43张PNG图片
- **文档长度**: 约24,000字符

## 图片文件

文档引用了以下图片文件（必须与.tex文件在同一目录）：
- image.png
- image-1.png 到 image-44.png

**注意**: 编译前请确保所有图片文件存在！

## 常见问题

### Q: 编译时提示缺少字体
A: 确保安装了中文字体支持。Windows和macOS通常自带，Linux可能需要安装：
```bash
sudo apt-get install texlive-lang-chinese
```

### Q: 图片无法显示
A: 检查：
1. 图片文件是否与.tex在同一目录
2. 图片文件名是否正确（区分大小写）
3. 图片格式是否支持（PNG, JPG, PDF）

### Q: 编译时提示Package错误
A: 安装完整的TeX发行版，或单独安装缺失的包：
```bash
# TeX Live
tlmgr install <package-name>

# MiKTeX（会自动提示安装缺失包）
```

## 输出文件

成功编译后会生成：
- **Lab1_report.pdf** - 最终PDF报告
- Lab1_report.aux - 辅助文件
- Lab1_report.log - 编译日志
- Lab1_report.out - 超链接信息

## 修改建议

如需修改个人信息，编辑第26-28行：
```latex
\author{
	姓名：\underline{冯峻}~~~~~~
	学号：\underline{523031910148}~~~~~~}
```

如需修改页眉，编辑第35行：
```latex
\fancyhead[L]{冯峻}
```

## 联系与支持

如有问题或需要帮助，请查阅：
- TeX Live文档: https://www.tug.org/texlive/
- ctex宏包文档: http://mirrors.ctan.org/language/chinese/ctex/ctex.pdf
- LaTeX Stack Exchange: https://tex.stackexchange.com/
