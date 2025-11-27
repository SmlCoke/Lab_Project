*****************************************************
* Lab3 - Task 3: Use Logical Effort to Optimize 5×32 Decoder
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../../16nfet.pm'
.include '../../16pfet.pm'

* source
Vdd vdd 0 DC 'SUPPLY'
VA0 A4 0 DC 'SUPPLY'
VA3 A3 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)
VA2 A2 0 DC 'SUPPLY'
VA1 A1 0 DC 'SUPPLY'
VA0 A0 0 DC 'SUPPLY'

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
.subckt INV in out vdd gnd size=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='size'
Mp out in vdd vdd pfet L='Lg' NFIN ='size'
.ends INV

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

* Circuit: 4 to 16 decoder
* The first layer is 4 inverters. After this layer, we get 4 outputs
* which are NA4, NA3, NA2, NA1, NA0
Xinv41 A4 NA4 vdd gnd INV size = '1' Lg = '20n'
Xinv31 A3 NA3 vdd gnd INV size = '1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV size = '1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV size = '1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV size = '1' Lg = '20n'

* The second layer is 4 inverters. After this layer, we get 5 outputs
* which are PA4, PA3, PA2, PA1, PA0
Xinv42 NA4 PA4 vdd gnd INV size = '1' Lg = '20n'
Xinv32 NA3 PA3 vdd gnd INV size = '1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV size = '1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV size = '1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV size = '1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 9 outputs
* which is Cartesian Product of (PA4, NA4) with (PA3, NA3) and (PA2, NA2) with (PA1, NA1)
* and NPA0
XinvPA0 PA0 NPA0 vdd gnd INV size = '1' Lg = '20n'

XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 size = "{XNAND2_size}" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 NPA0 word_0  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 PA0  word_1  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 NPA0 word_2  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 PA0  word_3  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 NPA0 word_4  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 PA0  word_5  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 NPA0 word_6  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 PA0  word_7  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 NPA0 word_8  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 PA0  word_9  vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 NPA0 word_10 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 PA0  word_11 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 NPA0 word_12 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 PA0  word_13 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 NPA0 word_14 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 PA0  word_15 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 NPA0 word_16 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 PA0  word_17 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 NPA0 word_18 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 PA0  word_19 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 NPA0 word_20 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 PA0  word_21 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 NPA0 word_22 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 PA0  word_23 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 NPA0 word_24 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 PA0  word_25 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 NPA0 word_26 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 PA0  word_27 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 NPA0 word_28 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 PA0  word_29 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 NPA0 word_30 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 PA0  word_31 vdd gnd NOR3 size="{XNOR3_size}" Lg='20n'  

* About critical path, we can obviously see that the path which passes 3'inv(A0 -> NA0 -> PA0 -> NPA0) is the longest.
* A0 -> Xinv01 -> NA0 -> Xinv02 -> PA0 -> XinvPA0 -> NPA0 -> XNOR2_15 -> word_15
* Xinv31: g = 1, b = 1, f = Xinv32_size/Xinv31_size 
* Xinv32: g = 1, b: (XNAND2_7, XNAND2_6), b = 2, f = XNAND2_7_size/Xinv32_size
* XNAND2_7: g = 3/2, b = (XNOR2_12, XNOR2_13, XNOR2_14, XNOR2_15), b= 4, f = XNOR2_15_size/XNAND2_7_size
* XNOR2_15: g = 3/2, b = 1
* Then there are 2m invs, g = 1, b = 1, f = ratio of size stage by stage
* G = 1 * 3/2 *3/2 * 1... = 9/4, B = 8, F = 128  
* H = 2304
* D = NH^(1/N) + p(Xinv32)(=1) + p(XNAND2_7) + p(XNOR2_15) + p(2m*inv)
* D = (2m+3)2304^[1/(2m+3)] + 1 + 2 + 2 + 2m = (2m+4=3)2304**[1/(2m+3)] + 2m + 5 = NH**(1/N) + N + 1
* solve critical point of NH**(1/N) + N + 1
{instance_lines}

.tran 1p 20n 
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V({output}) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V({output}) = '0.5*SUPPLY' FALL = 4
.measure tran tp param='(tpLH+tpHL)/2'
.end