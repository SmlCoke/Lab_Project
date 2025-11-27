*****************************************************
* Lab3 - Task 1: Use Logical Effort to Size Gates
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
.subckt INV in out vdd gnd size=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='size'
Mp out in vdd vdd pfet L='Lg' NFIN ='size'
.ends INV

* Sub circuit: 3-NAND
.subckt NAND3 in1 in2 in3 out vdd gnd size=1 Lg=20n
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='size'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='size'
Mp3 out in3 vdd vdd pfet L='Lg' NFIN='size'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='size'
Mn2 source1 in2 source2 gnd nfet L='Lg' NFIN='size'
Mn3 source2 in3 gnd gnd nfet L='Lg' NFIN='size'
.ends NAND3

* Sub circuit: 2-NOR
.subckt NOR2 in1 in2 out vdd gnd size=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='size'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='size'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='size'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='size'
.ends NOR2

* Transistor size variable
.param S2 = '4'
.param S3 = '7'
.param S4 = '17'

Xinv1 vpulse inv1_out vdd gnd INV size = 1 Lg = 'Lg'
Xnand3 inv1_out vdd vdd nand3_out vdd gnd NAND3 size = 'S3' Lg = 'Lg'
Xnor2 nand3_out gnd nor2_out vdd gnd NOR2 size = 'S2' Lg = 'Lg'
Xinv2 nor2_out inv2_out vdd gnd INV size = 'S4' Lg = 'Lg'
Xinv_load inv2_out inv_load_out vdd gnd INV size = '64' Lg = 'Lg'


.data sweepdata S2 S3 S4
+ 2 5 15
+ 3 5 15
+ 4 5 15
+ 5 5 15
+ 6 5 15
* -------
+ 2 6 15
+ 3 6 15
+ 4 6 15
+ 5 6 15
+ 6 6 15
* -------
+ 2 7 15
+ 3 7 15
+ 4 7 15
+ 5 7 15
+ 6 7 15
* -------
+ 2 8 15
+ 3 8 15
+ 4 8 15
+ 5 8 15
+ 6 8 15
* -------
+ 2 9 15
+ 3 9 15
+ 4 9 15
+ 5 9 15
+ 6 9 15
* -------
+ 2 5 16
+ 3 5 16
+ 4 5 16
+ 5 5 16
+ 6 5 16
* -------
+ 2 6 16
+ 3 6 16
+ 4 6 16
+ 5 6 16
+ 6 6 16
* -------
+ 2 7 16
+ 3 7 16
+ 4 7 16
+ 5 7 16
+ 6 7 16
* -------
+ 2 8 16
+ 3 8 16
+ 4 8 16
+ 5 8 16
+ 6 8 16
* -------
+ 2 9 16
+ 3 9 16
+ 4 9 16
+ 5 9 16
+ 6 9 16
* -------
+ 2 5 17
+ 3 5 17
+ 4 5 17
+ 5 5 17
+ 6 5 17
* -------
+ 2 6 17
+ 3 6 17
+ 4 6 17
+ 5 6 17
+ 6 6 17
* -------
+ 2 7 17
+ 3 7 17
+ 4 7 17
+ 5 7 17
+ 6 7 17
* -------
+ 2 8 17
+ 3 8 17
+ 4 8 17
+ 5 8 17
+ 6 8 17
* -------
+ 2 9 17
+ 3 9 17
+ 4 9 17
+ 5 9 17
+ 6 9 17
* -------
+ 2 5 18
+ 3 5 18
+ 4 5 18
+ 5 5 18
+ 6 5 18
* -------
+ 2 6 17
+ 3 6 17
+ 4 6 17
+ 5 6 17
+ 6 6 17
* -------
+ 2 7 17
+ 3 7 17
+ 4 7 17
+ 5 7 17
+ 6 7 17
* -------
+ 2 8 17
+ 3 8 17
+ 4 8 17
+ 5 8 17
+ 6 8 17
* -------
+ 2 9 17
+ 3 9 17
+ 4 9 17
+ 5 9 17
+ 6 9 17
* -------
+ 2 5 18
+ 3 5 18
+ 4 5 18
+ 5 5 18
+ 6 5 18
* -------
+ 2 6 18
+ 3 6 18
+ 4 6 18
+ 5 6 18
+ 6 6 18
* -------
+ 2 7 18
+ 3 7 18
+ 4 7 18
+ 5 7 18
+ 6 7 18
* -------
+ 2 8 18
+ 3 8 18
+ 4 8 18
+ 5 8 18
+ 6 8 18
* -------
+ 2 9 18
+ 3 9 18
+ 4 9 18
+ 5 9 18
+ 6 9 18
* -------
+ 2 5 19
+ 3 5 19
+ 4 5 19
+ 5 5 19
+ 6 5 19
* -------
+ 2 6 19
+ 3 6 19
+ 4 6 19
+ 5 6 19
+ 6 6 19
* -------
+ 2 7 19
+ 3 7 19
+ 4 7 19
+ 5 7 19
+ 6 7 19
* -------
+ 2 8 19
+ 3 8 19
+ 4 8 19
+ 5 8 19
+ 6 8 19
* -------
+ 2 9 19
+ 3 9 19
+ 4 9 19
+ 5 9 19
+ 6 9 19

.tran 1p 20n sweep data = sweepdata 
.measure tran tpLH TRIG V(vpulse) = '0.5*SUPPLY' RISE = 4 TARG V(inv2_out) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(vpulse) = '0.5*SUPPLY' FALL = 4 TARG V(inv2_out) = '0.5*SUPPLY' FALL = 4
.measure tran tp param='(tpLH+tpHL)/2'

.probe tran V(*) I(*)
.end