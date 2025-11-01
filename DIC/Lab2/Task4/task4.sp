*****************************************************
* Lab2 - Task 4: EDP measurement
*****************************************************
.option post=2 
.temp 25
.param SUPPLY = 0.75
.param Wfin = 0.078u   
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

* .data volts SUPPLY
* 0.5
* 0.6
* 0.75
* 0.9
* 1.0
* .enddata


.tran 1p 10n sweep SUPPLY '0.5' '1.0' '0.02'
* .tran 1p 10n sweep data=volts
.probe tran V(*) I(*)
.measure tran tpLH1 TRIG V(in) = '0.5*SUPPLY' FALL = 2  TARG V(inv1_out) = '0.5*SUPPLY' RISE = 2
.measure tran tpHL1 TRIG V(in) = '0.5*SUPPLY' RISE = 2  TARG V(inv1_out) = '0.5*SUPPLY' FALL = 2
.measure tran tp1 param='(tpLH1+tpHL1)/2'

.measure tran tpLH2 TRIG V(inv1_out) = '0.5*SUPPLY' FALL = 2  TARG V(inv2_out) = '0.5*SUPPLY' RISE = 2
.measure tran tpHL2 TRIG V(inv1_out) = '0.5*SUPPLY' RISE = 2  TARG V(inv2_out) = '0.5*SUPPLY' FALL = 2
.measure tran tp2 param='(tpLH2+tpHL2)/2'

.measure tran tpLH3 TRIG V(inv2_out) = '0.5*SUPPLY' FALL = 2  TARG V(inv3_out) = '0.5*SUPPLY' RISE = 2
.measure tran tpHL3 TRIG V(inv2_out) = '0.5*SUPPLY' RISE = 2  TARG V(inv3_out) = '0.5*SUPPLY' FALL = 2
.measure tran tp3 param='(tpLH3+tpHL3)/2'

.measure tran tpLH4 TRIG V(inv3_out) = '0.5*SUPPLY' FALL = 2  TARG V(inv4_out) = '0.5*SUPPLY' RISE = 2
.measure tran tpHL4 TRIG V(inv3_out) = '0.5*SUPPLY' RISE = 2  TARG V(inv4_out) = '0.5*SUPPLY' FALL = 2
.measure tran tp4 param='(tpLH4+tpHL4)/2'

.measure tran tp_total param='tp1+tp2+tp3+tp4'

.measure TRAN avgpower AVG P(vdd_inv) from=1n to=8n
.measure tran EDP param='abs(avgpower*tp_total*tp_total)'

.end