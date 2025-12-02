*****************************************************
* Lab3 - Task 2: Use Logical Effort to Optimize 4×16 Decoder
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
VA3 A3 0 PULSE (0 'SUPPLY' 900p 100p 100p 900p 2n)
VA2 A2 0 DC 'SUPPLY'
VA1 A1 0 DC 'SUPPLY'
VA0 A0 0 DC 'SUPPLY'

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

* Sub circuit: 2-NOR
* g = 1.5
* CM到SN/SP转换: SN = CM/1.5, SP = CM/1.5*2
.subckt NOR2 in1 in2 out vdd gnd SN=1 SP=1 Lg=20n
*PUN
Mp1 out in1 source_p1 vdd pfet L='Lg' NFIN='SP'
Mp2 source_p1 in2 vdd vdd pfet L='Lg' NFIN='SP'
*PDN
Mn1 out in1 gnd gnd nfet L='Lg' NFIN='SN'
Mn2 out in2 gnd gnd nfet L='Lg' NFIN='SN'
.ends NOR2

* Circuit: 4 to 16 decoder
* The first layer is 4 inverters. After this layer, we get 4 outputs
* which are NA3, NA2, NA1, NA0
Xinv31 A3 NA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv21 A2 NA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv11 A1 NA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv01 A0 NA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The second layer is 4 inverters. After this layer, we get 4 outputs
* which are PA3, PA2, PA1, PA0
Xinv32 NA3 PA3 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv22 NA2 PA2 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv12 NA1 PA1 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv02 NA0 PA0 vdd gnd INV SN='1' SP='1' Lg = '20n'

* The third layer is 8 NAND2 gates. After this layer, we get 8 outputs
* which is Cartesian Product of (PA3, NA3) with (PA2, NA2) and (PA1, NA1) with (PA0, NA0)
* NAND2: CM_NAND2 -> SN_NAND2 = CM_NAND2/1.5*2, SP_NAND2 = CM_NAND2/1.5
XNAND2_0 NA1 NA0 NA1_NA0 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_1 NA1 PA0 NA1_PA0 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_2 PA1 NA0 PA1_NA0 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_3 PA1 PA0 PA1_PA0 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_4 NA3 NA2 NA3_NA2 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_5 NA3 PA2 NA3_PA2 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_6 PA3 NA2 PA3_NA2 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'
XNAND2_7 PA3 PA2 PA3_PA2 vdd gnd NAND2 SN="2" SP="1" Lg = '20n'

* The last layer is 16 NOR2 gates. After this layer, we get 16 outputs
* which is A3'A2'A1'A0', A3'A2'A1'A0, to A3A2A1A0
* NOR2: CM_NOR2 -> SN_NOR2 = CM_NOR2/1.5, SP_NOR2 = CM_NOR2/1.5*2
XNOR2_0  NA3_NA2 NA1_NA0 word_0  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_1  NA3_NA2 NA1_PA0 word_1  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_2  NA3_NA2 PA1_NA0 word_2  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_3  NA3_NA2 PA1_PA0 word_3  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_4  NA3_PA2 NA1_NA0 word_4  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_5  NA3_PA2 NA1_PA0 word_5  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_6  NA3_PA2 PA1_NA0 word_6  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_7  NA3_PA2 PA1_PA0 word_7  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_8  PA3_NA2 NA1_NA0 word_8  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_9  PA3_NA2 NA1_PA0 word_9  vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_10 PA3_NA2 PA1_NA0 word_10 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_11 PA3_NA2 PA1_PA0 word_11 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_12 PA3_PA2 NA1_NA0 word_12 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_13 PA3_PA2 NA1_PA0 word_13 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_14 PA3_PA2 PA1_NA0 word_14 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'
XNOR2_15 PA3_PA2 PA1_PA0 word_15 vdd gnd NOR2 SN="1" SP="1" Lg = '20n'   

* About critical path, we can obviously see that the path which passes 2'inv is the longest.
* Such path has an general feature, it has PA!
* We choose to optimize the path: 
* A3 -> Xinv31 -> NA3 -> Xinv32 -> PA3 -> XNAND2_7 -> PA3_PA2 -> XNOR2_15 -> word_15
* Xinv31: g = 1, b = 1, f = Xinv32_size/Xinv31_size 
* Xinv32: g = 1, b: (XNAND2_7, XNAND2_6), b = 2, f = XNAND2_7_size/Xinv32_size
* XNAND2_7: g = 3/2, b = (XNOR2_12, XNOR2_13, XNOR2_14, XNOR2_15), b= 4, f = XNOR2_15_size/XNAND2_7_size
* XNOR2_15: g = 3/2, b = 1
* Then there are m invs, g = 1, b = 1, f = ratio of size stage by stage
* G = 1 * 3/2 *3/2 * 1... = 9/4, B = 8, F = 128  
* H = 2304
* D = NH^(1/N) + p(Xinv32)(=1) + p(XNAND2_7) + p(XNOR2_15) + p(m*inv)
* D = (m+3)2304^[1/(m+3)] + 1 + 2 + 2 + m = (m+3)2304**[1/(m+3)] + m + 5 = NH**(1/N) + N + 1
* solve critical point of NH**(1/N) + N + 1
* N = 6.05, hopt = 3.59
Xinv_buffer_0 word_15 buffer_out_0 vdd gnd INV SN='1' SP='1' Lg = '20n'
Xinv_buffer_1 buffer_out_0 buffer_out_1 vdd gnd INV SN='3' SP='3' Lg = '20n'
Xinv_buffer_2 buffer_out_1 buffer_out_2 vdd gnd INV SN='7' SP='7' Lg = '20n'
Xinv_buffer_3 buffer_out_2 buffer_out_3 vdd gnd INV SN='18' SP='18' Lg = '20n'
Xinv_buffer_4 buffer_out_3 buffer_out_4 vdd gnd INV SN='49' SP='49' Lg = '20n'
Xinv_load buffer_out_4 load_out vdd gnd INV SN='128' SP='128' Lg = '20n'

.tran 1p 10n 
.probe V(*) I(*)
.measure tran tpLH TRIG V(NA3) = '0.5*SUPPLY' RISE = 4 TARG V(buffer_out_4) = '0.5*SUPPLY' RISE = 4
.measure tran tpHL TRIG V(NA3) = '0.5*SUPPLY' FALL = 4 TARG V(buffer_out_4) = '0.5*SUPPLY' FALL = 4

.measure tran tp param='(tpLH+tpHL)/2'
.end
