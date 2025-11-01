*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = 2
*****************************************************
.option post=2 RUNLVL = 6
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
Xinv2 inv1_out inv2_out vdd 0 inv nfin='16'

* load
XinvL inv2_out invL_out vdd 0 inv nfin=256


.tran 1p 10n

.measure tran tpLH1 TRIG V(in) VAL='0.5*SUPPLY' FALL=2 TARG V(inv1_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL1 TRIG V(in) VAL='0.5*SUPPLY' RISE=2 TARG V(inv1_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp1 PARAM='(tpLH1+tpHL1)/2'
.measure tran tpLH2 TRIG V(inv1_out) VAL='0.5*SUPPLY' FALL=2 TARG V(inv2_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL2 TRIG V(inv1_out) VAL='0.5*SUPPLY' RISE=2 TARG V(inv2_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp2 PARAM='(tpLH2+tpHL2)/2'
.measure tran tp_total PARAM='tp1+tp2'

.probe V(*) I(*)
.end
