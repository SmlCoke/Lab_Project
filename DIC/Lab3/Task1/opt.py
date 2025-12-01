def get_S(CM, type):
    """根据电容倍数CM和门类型，计算所需的N管和P管尺寸S

    参数:
    - CM: 电容倍数
    - type: 门类型，'NAND2' 或 'NOR2'

    返回:
    - SN, SP: 所需的器件尺寸
    """

    if type == 'INV':
        g = 1
        SN = CM / g
        SP = CM / g
        return SN, SP
    elif type == 'NAND2':
        g = 1.5
        SN = CM / g * 2
        SP = CM / g 
        return SN, SP
    elif type == 'NOR2':
        g = 1.5
        SN = CM / g 
        SP = CM / g * 2
        return SN, SP
    elif type == 'NAND3':
        g = 2
        SN = CM / g * 3
        SP = CM / g 
        return SN, SP
    elif type == 'NOR3':
        g = 2
        SN = CM / g 
        SP = CM / g * 3
        return SN, SP
    else:
        raise ValueError("Unsupported gate type. Use 'NAND2' or 'NOR2'.")

if __name__ == "__main__":
    g1 = 1
    g2 = 4/2
    g3 = 3/2
    g4 = 1
    b1 = 1; b2 = 1; b3 = 1; b4 = 1
    H = 192
    hopt = H**(1/4)
    load = 64

    # optimize 4:
    f4 = hopt/g4/b4
    CM4 = load/f4

    f3 = hopt/g3/b3
    CM3 = CM4/f3

    f2 = hopt/g2/b2
    CM2 = CM3/f2

    f1 = hopt/g1/b1
    CM1 = CM2/f1

    print("f1:", f1)
    print("f2:", f2)
    print("f3:", f3)
    print("f4:", f4)

    print("CM1:", CM1)
    print("CM2:", CM2)
    print("CM3:", CM3)
    print("CM4:", CM4)

    SN_2, SP_2 = get_S(CM2, 'NAND3')
    SN_3, SP_3 = get_S(CM3, 'NOR2')
    SN_4, SP_4 = get_S(CM4, 'INV')

    print("NAND3:\n", "SN_2:", SN_2, "\n", "SP_2:", SP_2)
    print("NOR2:\n", "SN_3:", SN_3, "\n", "SP_3:", SP_3)
    print("INV:\n", "SN_4:", SN_4, "\n", "SP_4:", SP_4)

    SN2_int = int(SN_2 + 0.5)
    SP2_int = int(SP_2 + 0.5)
    SN3_int = int(SN_3 + 0.5)
    SP3_int = int(SP_3 + 0.5)
    SN4_int = int(SN_4 + 0.5)
    SP4_int = int(SP_4 + 0.5)

    print("NAND3 int:\n", "SN_2:", SN2_int, "\n", "SP_2:", SP2_int)
    print("NOR2 int:\n", "SN_3:", SN3_int, "\n", "SP_3:", SP3_int)
    print("INV int:\n", "SN_4:", SN4_int, "\n", "SP_4:", SP4_int)