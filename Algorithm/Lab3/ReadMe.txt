我的环境配置
wsl
ubuntu 2204
python3.10.12

补全代码后依次运行以下三条可以获得打分结果(可能会缺库,自己补全一下就可以了,不会装也可以来问)
python3 setup.py build
python3 eda.py cells.spi AN2D2
python3 evaluator.py AN2D2.json AN2D2 cells.spi