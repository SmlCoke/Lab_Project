*****************************************************
* Lab3 - Task 1: Use Logical Effort to CMulti Gates
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../16nfet.pm'
.include '../16pfet.pm'

* source
Vdd vdd 0 DC 'SUPPLY'
Vpulse vpulse 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)

* 我们认为，所有PMOS的bulk接到vdd，所有NMOS的bulk接到gnd

* Sub circuit: INVerter definition
* SN = SP = CMulti
.subckt INV in out vdd gnd Lg = 20n SN = 1 SP = 1 
Mn out in gnd gnd nfet L='Lg' NFIN ='SN'
Mp out in vdd vdd pfet L='Lg' NFIN ='SP'
.ends INV

* Sub circuit: 3-NAND
* g = 2
* SN = CMulti/2*3
* SP = CMulti/2
.subckt NAND3 in1 in2 in3 out vdd gnd Lg=20n SN = 1 SP = 1 
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='SP'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='SP'
Mp3 out in3 vdd vdd pfet L='Lg' NFIN='SP'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='SN'
Mn2 source1 in2 source2 gnd nfet L='Lg' NFIN='SN'
Mn3 source2 in3 gnd gnd nfet L='Lg' NFIN='SN'
.ends NAND3

* Sub circuit: 2-NOR
* g = 1.5
* SN = CMulti/1.5
* SP = CMulti/1.5*2
.subckt NOR2 in1 in2 out vdd gnd Lg=20n SN = 1 SP = 1
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR2

* Transistor CMulti variable
.param SN_2 = 1
.param SN_3 = 1
.param SN_4 = 1
.param SP_2 = 1
.param SP_3 = 1
.param SP_4 = 1

Xinv1 vpulse inv1_out vdd gnd INV CMulti = 1 Lg = 'Lg'
Xnand3 inv1_out vdd vdd nand3_out vdd gnd NAND3 SN='SN_2' SP = 'SP_2' Lg = 'Lg'
Xnor2 nand3_out gnd nor2_out vdd gnd NOR2 SN = 'SN_3' SP = 'SP_3' Lg = 'Lg'
Xinv2 nor2_out inv2_out vdd gnd INV SN = 'SN_4' SP = 'SP_4' Lg = 'Lg'
Xinv_load inv2_out inv_load_out vdd gnd INV CMulti = '64' Lg = 'Lg'


.data sweepdata SN_2 SP_2 SN_3 SP_3 SN_4 SP_4
5 2 3 6 14 14
5 2 3 6 17 17
5 2 3 6 20 20
5 2 5 10 14 14
5 2 5 10 17 17
5 2 5 10 20 20
5 2 7 14 14 14
5 2 7 14 17 17
5 2 7 14 20 20
6 2 3 6 14 14
6 2 3 6 17 17
6 2 3 6 20 20
6 2 5 10 14 14
6 2 5 10 17 17
6 2 5 10 20 20
6 2 7 14 14 14
6 2 7 14 17 17
6 2 7 14 20 20
7 2 3 6 14 14
7 2 3 6 17 17
7 2 3 6 20 20
7 2 5 10 14 14
7 2 5 10 17 17
7 2 5 10 20 20
7 2 7 14 14 14
7 2 7 14 17 17
7 2 7 14 20 20
.enddata

.tran 1p 20n sweep data = sweepdata 
.measure tran tpLH TRIG V(vpulse) = '0.5*SUPPLY' RISE = 4 TARG V(inv2_out) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(vpulse) = '0.5*SUPPLY' FALL = 4 TARG V(inv2_out) = '0.5*SUPPLY' FALL = 4
.measure tran tp param='(tpLH+tpHL)/2'

.probe tran V(*) I(*)
.end
