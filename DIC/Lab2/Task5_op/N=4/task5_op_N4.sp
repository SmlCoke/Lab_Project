*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = 4
*****************************************************
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n
.param f2 = 4
.param f3 = 16
.param f4 = 64
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
XinvL inv4_out invL_out vdd 0 inv nfin = 256

* sweeping parameter config
.data sweepdata f2 f3 f4
+ 4 16 56
+ 4 16 58
+ 4 16 60
+ 4 16 62
+ 4 16 64
+ 4 16 66
+ 4 16 68
+ 4 16 70
+ 4 15 56
+ 4 15 58
+ 4 15 60
+ 4 15 62
+ 4 15 64
+ 4 15 66
+ 4 15 68
+ 4 15 70
+ 4 17 56
+ 4 17 58
+ 4 17 60
+ 4 17 62
+ 4 17 64
+ 4 17 66
+ 4 17 68
+ 4 17 70
+ 5 16 56
+ 5 16 58
+ 5 16 60
+ 5 16 62
+ 5 16 64
+ 5 16 66
+ 5 16 68
+ 5 16 70
+ 5 15 56
+ 5 15 58
+ 5 15 60
+ 5 15 62
+ 5 15 64
+ 5 15 66
+ 5 15 68
+ 5 15 70
+ 5 17 56
+ 5 17 58
+ 5 17 60
+ 5 17 62
+ 5 17 64
+ 5 17 66
+ 5 17 68
+ 5 17 70
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
.measure tran tp_total PARAM='tp1+tp2+tp3+tp4'

.probe V(*) I(*)
.end
