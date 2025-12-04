.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 

.include '../16nfet.pm'
.include '../16pfet.pm'

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

* Sub circuit: 2-NAND
* g = 1.5
* SN = CMulti/1.5*2
* SP = CMulti/1.5
.subckt NAND2 in1 in2 out vdd gnd Lg=20n SN = 1 SP = 1
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='SP'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='SP'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='SN'
Mn2 source1 in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NAND2

* Sub circuit: 3-NOR
* g = 2
* SN = CMulti/2
* SP = CMulti/2*3
.subckt NOR3 in1 in2 in3 out vdd gnd Lg=20n SN = 1 SP = 1
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 source_p2 vdd pfet L='Lg' NFIN='SP'
Mp3 source_p2 in3 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
Mn3 out in3 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR3