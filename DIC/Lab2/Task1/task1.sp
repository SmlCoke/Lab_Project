*****************************************************
* Lab2 - Task 1: CMOS Inverter FO4 Delay Measurement
*****************************************************
.option post=2 
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 

* lib
.include '../16nfet.pm'
.include '../16pfet.pm'

* Sub circuit: Inverter definition
.subckt inv in out vdd gnd nfin=1
Mn out in gnd gnd nfet L='Lg' NFIN ='nfin'
Mp out in vdd vdd pfet L='Lg' NFIN ='nfin'
.ends inv

* Definition of drive source
Vdd vdd 0 DC 'SUPPLY' 
VIN in 0 PULSE 0 'SUPPLY' 400p 25p 25p 400p 800p

* Connet subckt
Xinv1 in inv1_out vdd 0 inv nfin=1
Xinv2 inv1_out inv2_out vdd 0 inv nfin=2
Xinv3 inv2_out inv3_out vdd 0 inv nfin=4
* Load
Xinv4 inv3_out inv4_out vdd 0 inv nfin=4
Xinv5 inv3_out inv5_out vdd 0 inv nfin=4
Xinv6 inv3_out inv6_out vdd 0 inv nfin=4
Xinv7 inv3_out inv7_out vdd 0 inv nfin=4

.tran 1p 10n
.probe tran V(*) I(*)
.measure tran tpLH TRIG V(inv2_out) = '0.5*SUPPLY' FALL = 2 TARG V(inv3_out) = '0.5*SUPPLY' RISE = 2
.measure tran tpHL TRIG V(inv2_out) = '0.5*SUPPLY' RISE = 2 TARG V(inv3_out) = '0.5*SUPPLY' FALL = 2
.measure tran tp param = '(tpLH+tpHL)/2'
.end
