*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = 4
*****************************************************
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n
.param f2 = 3
.param f3 = 9
.param f4 = 27
.param f5 = 84
.include '../../16nfet.pm'
.include '../../16pfet.pm'

.subckt inv in out vdd gnd nfin=1
Mn out in gnd gnd nfet L='Lg' NFIN='nfin'
Mp out in vdd vdd pfet L='Lg' NFIN='nfin'
.ends inv

Vdd vdd 0 DC 'SUPPLY'
Vin in 0 PULSE (0 'SUPPLY' 400p 25p 25p 400p 800p)

* Connet subckt
Xinv1 in inv1_out vdd 0 inv nfin = 1
Xinv2 inv1_out inv2_out vdd 0 inv nfin = 'f2'
Xinv3 inv2_out inv3_out vdd 0 inv nfin = 'f3'
Xinv4 inv3_out inv4_out vdd 0 inv nfin = 'f4'
Xinv5 inv4_out inv5_out vdd 0 inv nfin = 'f5'
XinvL inv5_out invL_out vdd 0 inv nfin = 256

* sweeping parameter config
.data sweepdata f2 f3 f4 f5
+ 3 9 27 80
+ 3 9 27 84
+ 3 9 27 88
+ 3 9 25 80
+ 3 9 25 84
+ 3 9 25 88
+ 3 9 29 80
+ 3 9 29 84
+ 3 9 29 88
+ 3 7 27 80
+ 3 7 27 84
+ 3 7 27 88
+ 3 7 25 80
+ 3 7 25 84
+ 3 7 25 88
+ 3 7 29 80
+ 3 7 29 84
+ 3 7 29 88
+ 3 11 27 80
+ 3 11 27 84
+ 3 11 27 88
+ 3 11 25 80
+ 3 11 25 84
+ 3 11 25 88
+ 3 11 29 80
+ 3 11 29 84
+ 3 11 29 88
+ 2 9 27 80
+ 2 9 27 84
+ 2 9 27 88
+ 2 9 25 80
+ 2 9 25 84
+ 2 9 25 88
+ 2 9 29 80
+ 2 9 29 84
+ 2 9 29 88
+ 2 7 27 80
+ 2 7 27 84
+ 2 7 27 88
+ 2 7 25 80
+ 2 7 25 84
+ 2 7 25 88
+ 2 7 29 80
+ 2 7 29 84
+ 2 7 29 88
+ 2 11 27 80
+ 2 11 27 84
+ 2 11 27 88
+ 2 11 25 80
+ 2 11 25 84
+ 2 11 25 88
+ 2 11 29 80
+ 2 11 29 84
+ 2 11 29 88
+ 4 9 27 80
+ 4 9 27 84
+ 4 9 27 88
+ 4 9 25 80
+ 4 9 25 84
+ 4 9 25 88
+ 4 9 29 80
+ 4 9 29 84
+ 4 9 29 88
+ 4 7 27 80
+ 4 7 27 84
+ 4 7 27 88
+ 4 7 25 80
+ 4 7 25 84
+ 4 7 25 88
+ 4 7 29 80
+ 4 7 29 84
+ 4 7 29 88
+ 4 11 27 80
+ 4 11 27 84
+ 4 11 27 88
+ 4 11 25 80
+ 4 11 25 84
+ 4 11 25 88
+ 4 11 29 80
+ 4 11 29 84
+ 4 11 29 88


.tran 1p 10n sweep data = sweepdata

.measure tran tpLH1 TRIG V(in) VAL='0.5*SUPPLY' FALL=2 TARG V(inv1_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL1 TRIG V(in) VAL='0.5*SUPPLY' RISE=2 TARG V(inv1_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp1 PARAM='(tpLH1+tpHL1)/2'
.measure tran tpLH2 TRIG V(inv1_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv2_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL2 TRIG V(inv1_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv2_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp2 PARAM='(tpLH2+tpHL2)/2'
.measure tran tpLH3 TRIG V(inv2_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv3_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL3 TRIG V(inv2_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv3_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp3 PARAM='(tpLH3+tpHL3)/2'
.measure tran tpLH4 TRIG V(inv3_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv4_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL4 TRIG V(inv3_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv4_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp4 PARAM='(tpLH4+tpHL4)/2'
.measure tran tpLH5 TRIG V(inv4_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv5_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL5 TRIG V(inv4_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv5_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp5 PARAM='(tpLH5+tpHL5)/2'
.measure tran tp_total PARAM='tp1+tp2+tp3+tp4+tp5'

.probe V(*) I(*)
.end