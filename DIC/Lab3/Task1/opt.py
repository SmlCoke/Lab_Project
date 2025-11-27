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
    S4 = load/f4

    f3 = hopt/g3/b3
    S3 = S4/f3

    f2 = hopt/g2/b2
    S2 = S3/f2

    f1 = hopt/g1/b1
    S1 = S2/f1

    print("f1:", f1)
    print("f2:", f2)
    print("f3:", f3)
    print("f4:", f4)

    print("S1:", S1)
    print("S2:", S2)
    print("S3:", S3)
    print("S4:", S4)


    '''
    f1: 3.7224194364083982
    f2: 1.8612097182041991
    f3: 2.481612957605599
    f4: 3.7224194364083982
    S1: 1.0000000000000002
    S2: 3.7224194364083987
    S3: 6.92820323027551
    S4: 17.193118909176672
    '''