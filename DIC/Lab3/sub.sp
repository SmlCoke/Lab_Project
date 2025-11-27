.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 

.include '../16nfet.pm'
.include '../16pfet.pm'

* 我们认为，所有PMOS的bulk接到vdd，所有NMOS的bulk接到gnd

* Sub circuit: INVerter definition
.subckt INV in out vdd gnd size=1
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

* Sub circuit: 2-NAND
.subckt NAND2 in1 in2 out vdd gnd size=1 Lg=20n
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='size'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='size'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='size'
Mn2 source1 in2 gnd gnd nfet L='Lg' NFIN='size'
.ends NAND2

* Sub circuit: 3-NOR
.subckt NOR3 in1 in2 in3 out vdd gnd size=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='size'
Mp2 source_p1 in2 source_p2 vdd pfet L='Lg' NFIN='size'
Mp3 source_p2 in3 vdd vdd pfet L='Lg' NFIN='size'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='size'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='size'
Mn3 out in3 gnd gnd nfet L='Lg' NFIN='size'
.ends NOR3