*****************************************************
* Task5: Inverter chain optimization (auto-generated)
* N = 1
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

* load
XinvL inv1_out invL_out vdd 0 inv nfin=256


.tran 1p 10n

.measure tran tpLH1 TRIG V(in) VAL='0.5*SUPPLY' FALL=2 TARG V(inv1_out) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL1 TRIG V(in) VAL='0.5*SUPPLY' RISE=2 TARG V(inv1_out) VAL='0.5*SUPPLY' FALL=2
.measure tran tp1 PARAM='(tpLH1+tpHL1)/2'
.measure tran tp_total PARAM='tp1'

.probe V(*) I(*)
.end
