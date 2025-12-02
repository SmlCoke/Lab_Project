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
VA4 A4 0 DC '0'
VA3 A3 0 DC '0'
VA2 A2 0 DC '0'
VA1 A1 0 DC '0'
VA0 A0 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
* CM到SN/SP转换: SN = CM, SP = CM
.subckt INV in out vdd gnd SN=1 SP=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='SN'
Mp out in vdd vdd pfet L='Lg' NFIN ='SP'
.ends INV

* Sub circuit: 2-NAND
* g = 1.5
* CM到SN/SP转换: SN = CM/1.5*2, SP = CM/1.5
.subckt NAND2 in1 in2 out vdd gnd SN=1 SP=1 Lg=20n
* PUN
Mp1 out in1 vdd vdd pfet L='Lg' NFIN='SP'
Mp2 out in2 vdd vdd pfet L='Lg' NFIN='SP'
* PDN
Mn1 out in1 source1 gnd nfet L='Lg' NFIN='SN'
Mn2 source1 in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NAND2

* Sub circuit: 3-NOR
* g = 2
* CM到SN/SP转换: SN = CM/2, SP = CM/2*3
.subckt NOR3 in1 in2 in3 out vdd gnd SN=1 SP=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 source_p2 vdd pfet L='Lg' NFIN='SP'
Mp3 source_p2 in3 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
Mn3 out in3 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR3

* Circuit: 5 to 32 decoder
* The first layer is 5 inverters. After this layer, we get 5 outputs
* which are NA4, NA3, NA2, NA1, NA0
Xinv41 A4 NA4 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv31 A3 NA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The second layer is 5 inverters. After this layer, we get 5 outputs
* which are PA4, PA3, PA2, PA1, PA0
Xinv42 NA4 PA4 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv32 NA3 PA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 9 outputs
* which is Cartesian Product of (PA4, NA4) with (PA3, NA3) and (PA2, NA2) with (PA1, NA1)
* and NPA0 (inverter for PA0)
* XinvPA0: INV, CM = XinvPA0_size, SN = SP = CM
XinvPA0 PA0 NPA0 vdd gnd INV SN='6' SP='6' Lg = '20n'

* NAND2: CM = XNAND2_cm, SN = CM/1.5*2, SP = CM/1.5
XNAND2_0 NA2 NA1 NA2_NA1 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_1 NA2 PA1 NA2_PA1 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_2 PA2 NA1 PA2_NA1 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_3 PA2 PA1 PA2_PA1 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_4 NA4 NA3 NA4_NA3 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_5 NA4 PA3 NA4_PA3 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_6 PA4 NA3 PA4_NA3 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'
XNAND2_7 PA4 PA3 PA4_PA3 vdd gnd NAND2 SN="8" SP="4" Lg = '20n'

* The last layer: 32 NOR3 gates (4×4×2 = 32 combinations)
* Format: NOR3(A4A3_combo, A2A1_combo, A0_signal)
* NOR3: CM = XNOR3_cm, SN = CM/2, SP = CM/2*3

* A4A3 = 00 (NA4_NA3)
XNOR3_0  NA4_NA3 NA2_NA1 PA0  word_0  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_1  NA4_NA3 NA2_NA1 NPA0 word_1  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_2  NA4_NA3 NA2_PA1 PA0  word_2  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_3  NA4_NA3 NA2_PA1 NPA0 word_3  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_4  NA4_NA3 PA2_NA1 PA0  word_4  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_5  NA4_NA3 PA2_NA1 NPA0 word_5  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_6  NA4_NA3 PA2_PA1 PA0  word_6  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_7  NA4_NA3 PA2_PA1 NPA0 word_7  vdd gnd NOR3 SN="1" SP="3" Lg='20n'

* A4A3 = 01 (NA4_PA3)
XNOR3_8  NA4_PA3 NA2_NA1 PA0  word_8  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_9  NA4_PA3 NA2_NA1 NPA0 word_9  vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_10 NA4_PA3 NA2_PA1 PA0  word_10 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_11 NA4_PA3 NA2_PA1 NPA0 word_11 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_12 NA4_PA3 PA2_NA1 PA0  word_12 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_13 NA4_PA3 PA2_NA1 NPA0 word_13 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_14 NA4_PA3 PA2_PA1 PA0  word_14 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_15 NA4_PA3 PA2_PA1 NPA0 word_15 vdd gnd NOR3 SN="1" SP="3" Lg='20n'

* A4A3 = 10 (PA4_NA3)
XNOR3_16 PA4_NA3 NA2_NA1 PA0  word_16 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_17 PA4_NA3 NA2_NA1 NPA0 word_17 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_18 PA4_NA3 NA2_PA1 PA0  word_18 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_19 PA4_NA3 NA2_PA1 NPA0 word_19 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_20 PA4_NA3 PA2_NA1 PA0  word_20 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_21 PA4_NA3 PA2_NA1 NPA0 word_21 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_22 PA4_NA3 PA2_PA1 PA0  word_22 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_23 PA4_NA3 PA2_PA1 NPA0 word_23 vdd gnd NOR3 SN="1" SP="3" Lg='20n'

* A4A3 = 11 (PA4_PA3)
XNOR3_24 PA4_PA3 NA2_NA1 PA0  word_24 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_25 PA4_PA3 NA2_NA1 NPA0 word_25 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_26 PA4_PA3 NA2_PA1 PA0  word_26 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_27 PA4_PA3 NA2_PA1 NPA0 word_27 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_28 PA4_PA3 PA2_NA1 PA0  word_28 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_29 PA4_PA3 PA2_NA1 NPA0 word_29 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_30 PA4_PA3 PA2_PA1 PA0  word_30 vdd gnd NOR3 SN="1" SP="3" Lg='20n'
XNOR3_31 PA4_PA3 PA2_PA1 NPA0 word_31 vdd gnd NOR3 SN="1" SP="3" Lg='20n'  

* About critical path1, In reality, when the levels of A1 to A4 remain low, all 15 NOR3 gates connected to node Xinv12 that are not on critical path 1 will have at least one input at a high level. This means that regardless of how the A0 level toggles, the pull-down network of the NOR3 gates will definitely conduct, while the pull-up network will remain off. Consequently, even if the output level of Xinv12 changes, all NOR3 gates connected to its output—except for the one on the path—will maintain a low output level. When the output level of Xinv12 toggles, the input gate capacitances of these NOR3 gates will not affect the delay. In other words, under these conditions, we can consider the branch effort of Xinv12 to be equal to 1.
* A0 -> Xinv01 -> NA0 -> Xinv02 -> PA0 -> XinvPA0 -> NPA0 -> XNOR3_1 -> word_1
* Xinv02: p = 1, g = 1, f = XinvPA0_size/Xinv02_size, b = 1
* XinvPA0: p = 1, g = 1, f = XNOR3_1_size/XinvPA0_size, b = 16
* XNOR3_1: p = 3, g = 2, f = Xbuffer_0_size/XNOR3_1_size, b = 1
* H1 = x + 16y/x + 2z1/y + z2/z1 + ... + zm/z(m-1) + 256/zm
* H1min = 16 * 2 * 256 = 8192
* D = 1 + 1 + 3 + m + (m+3)*8192**[1/(m+3)] = (m+3)*8192**[1/(m+3)] + m + 6 = N8192**(1/N) + N + 3

* x1 = XinvPA0_size, x2 = XNAND2_size, y = XNOR3_size

Xbuffer_0 word_1 buffer_out_0 vdd gnd INV SN='7' SP='7' Lg='20n'
Xbuffer_1 buffer_out_0 buffer_out_1 vdd gnd INV SN='42' SP='42' Lg='20n'
Xinv_load buffer_out_1 load_out vdd gnd INV SN='256' SP='256' Lg='20n'


.tran 1p 10n 
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA0) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_1) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA0) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_1) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end
