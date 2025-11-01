*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = 7
*****************************************************
.option post=2
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n

.include '../../16nfet.pm'
.include '../../16pfet.pm'

.subckt inv in out vdd gnd nfin=1
Mn out in gnd gnd nfet L='Lg' NFIN='nfin'
Mp out in vdd vdd pfet L='Lg' NFIN='nfin'
.ends inv

Vdd vdd 0 DC 'SUPPLY'
Vin in 0 PULSE (0 'SUPPLY' 400p 25p 25p 400p 800p)

* Chain instances (1x then stages 2..N, then load 256x)
Xinv1 in inv1_out vdd 0 inv nfin=1
Xinv2 inv1_out inv2_out vdd 0 inv nfin='2'
Xinv3 inv2_out inv3_out vdd 0 inv nfin='4'
Xinv4 inv3_out inv4_out vdd 0 inv nfin='10'
Xinv5 inv4_out inv5_out vdd 0 inv nfin='23'
Xinv6 inv5_out inv6_out vdd 0 inv nfin='52'
Xinv7 inv6_out inv7_out vdd 0 inv nfin='115'

* load
XinvL inv7_out invL_out vdd 0 inv nfin=256


.tran 1p 10n

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
.measure tran tpLH6 TRIG V(inv5_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv6_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL6 TRIG V(inv5_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv6_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp6 PARAM='(tpLH6+tpHL6)/2'
.measure tran tpLH7 TRIG V(inv6_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv7_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL7 TRIG V(inv6_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv7_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp7 PARAM='(tpLH7+tpHL7)/2'
.measure tran tp_total PARAM='tp1+tp2+tp3+tp4+tp5+tp6+tp7'

.probe V(*) I(*)
.end
