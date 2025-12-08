import sympy as sp

# ------------- 0.25μm工艺参数 --------------
VTN = 0.43
VTP = -0.4
gamma_N = 0.4
gamma_P = -0.4
VDSAT_N = 0.63
VDSAT_P = -1
k_N = 115e-6*1.5
k_P = 30e-6*0.6
lambda_N = 0.06
lambda_P = -0.1
VDD = 2.5


if __name__ == "__main__":
    VF = sp.symbols('VF')

    eq1 = k_P*((0-VDD-VTP)*VDSAT_P - 0.5*VDSAT_P**2)*(1+lambda_P*(VF-VDD)) - k_N*((VDD-VTN)*VF - 0.5*VF**2)*(1+lambda_N*VF)
    eq2 = k_P*((0-VDD-VTP)*VDSAT_P - 0.5*VDSAT_P**2)*(1+lambda_P*(VF-VDD)) - 4*k_N*((VDD-VTN)*VF - 0.5*VF**2)*(1+lambda_N*VF)

    sol1 = sp.solve(eq1, VF, dict=True)
    sol2 = sp.solve(eq2, VF, dict=True)
    print("(1):")
    print(sol1)
    print("(2):")
    print(sol2)