DIC\Lab3是数字集成电路设计课程第三次实验的任务指导、代码、实验数据文件夹，你需要根据相关信息，帮我完成python脚本的纠正。
DIC\Lab3文件夹中你需要阅读的文件有：DIC\Lab3\Lab3 20251126.pdf，DIC\Lab3\Task1\Relation.md，DIC\Lab3\Task1\generate_sp.py，以及Lab3目录下及其嵌套子文件夹下的所有python脚本。其余.tex文件，.csv文件，.pdf文件, .png文件都不需要阅读。
具体任务要求是，现在只有Task1文件夹下的python脚本和sp脚本是正确的，
Task2~Task3错误的原因是，我以为逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数就是NFIN，实则是不对的。真正的对应关系在DIC\Lab3\Task1\Relation.md中，其中CMulti是逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数，SN和SP是P管和N管的尺寸。所以我需要你做的事情是，按照原来Task2, Task2_opt, Task3, Task3_opt中python脚本中的的实验内容和实验方法，结合新的对应关系，帮我修改好Task2, Task2_opt, Task3, Task3_opt中的所用python脚本（不需要修改其他文件，但是python脚本中注释可以写多一点）。在Python脚本中，逻辑门的输入栅电容相对于参考反相器的输入栅电容倍数用CM表示（可以加下标），晶体管尺寸用SN, SP表示（可以加下标，参考DIC\Lab3\Task1\generate_sp.py）
现在，请开始你的工作。