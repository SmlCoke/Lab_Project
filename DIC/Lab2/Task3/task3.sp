*****************************************************
* Lab2 - Task 3: CMOS Inverter Power
*****************************************************
.option post=2 
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 
* Configuration of inverter chain dimension
.param f2 = 5
.param f3 = 15
.param f4 = 60
* lib
.include '../16nfet.pm'
.include '../16pfet.pm'

* Sub circuit: Inverter definition
.subckt inv in out vdd gnd nfin=1
Mn out in gnd gnd nfet L='Lg' NFIN ='nfin'
Mp out in vdd vdd pfet L='Lg' NFIN ='nfin'
.ends inv

* Definition of drive source
Vdd_inv vdd_inv 0 DC 'SUPPLY'
vdd_load vdd_laod 0 DC 'SUPPLY' 
VIN in 0 PULSE 0 'SUPPLY' 400p 25p 25p 400p 800p

* Connet subckt
Xinv1 in inv1_out vdd_inv 0 inv nfin = 1
Xinv2 inv1_out inv2_out vdd_inv 0 inv nfin = 'f2'
Xinv3 inv2_out inv3_out vdd_inv 0 inv nfin = 'f3'
Xinv4 inv3_out inv4_out vdd_inv 0 inv nfin = 'f4'
XinvL inv4_out invL_out vdd_load 0 inv nfin = 256



.tran 1p 10n 
.probe tran V(*) I(*)

.MEASURE TRAN avgpower AVG P(vdd_inv) from=1n to=10n
.end