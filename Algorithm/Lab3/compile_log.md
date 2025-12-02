## 编译过程
### cmd1
```bash
python3 setup.py build
```
替换为了：
```bash
python setup.py build_ext --inplace
```

这个命令会告诉 setup.py 把编译好的 .pyd 文件直接放在当前源代码目录下，这样 eda.py 就能直接引用它了。

### cmd2
将
```bash
python3 eda.py cells.spi AN2D2 
```
替换为
```bash
python eda.py cells.spi AN2D2 "results\20000_1_88_2000\data.csv" > "results\20000_1_88_2000\process.log"
```
将eda.py打印的退火日志信息保存到log文件，将退火过程中的评分保存到.csv文件
data_file用于记录模拟退火过程中的数据文件。

### cmd3
然后评分指令:
```bash
python evaluator.py AN2D2.json AN2D2 cells.spi > "results\20000_1_88_2000\score.log"
```
将评分的信息保存到.log文件

## setup.py的修改：
```python
extra_compile_args = []
if sys.platform == "win32":
    extra_compile_args = ["/std:c++17", "/O2", "/utf-8"]
```
增加了utf-8参数，否则在执行命令`python setup.py build_ext --inplace`时会出现：
```bash
warning C4819: 该文件包含不能在当前代码页(936)中表示的字符
```
因为源文件是 UTF-8 编码，但 Windows 的中文命令行默认使用 GBK (代码页 936)。