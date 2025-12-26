*****************************************************
* Lab4 - Task 2: 8-bit Adder Simulation with FA28/FA16 and Buffers
*****************************************************
* global configuration
.option post=2 RUNLVL = 6
.temp 25
.param SUPPLY = 0.75
.param Lg = 20n 


* lib
.include '../../../16nfet.pm'
.include '../../../16pfet.pm'

* We believe that the bulk of all PMOS transistors should be connected to VDD, and the bulk of all NMOS transistors should be connected to GND.

* Sub circuit: INVerter definition
.subckt INV in out vdd gnd size=1 Lg=20n
Mn out in gnd gnd nfet L='Lg' NFIN ='size'
Mp out in vdd vdd pfet L='Lg' NFIN ='size'
.ends INV

* Sub circuit: Buffer
.subckt buffer in out vdd gnd size=1 Lg=20n
Xinv1 in mid vdd gnd INV size='size' Lg='Lg'
Xinv2 mid out vdd gnd INV size='size' Lg='Lg'
.ends

* Sub circuit: FA28_with_buffer
.subckt FA28_with_buffer Ain Bin Cin Cout Sum Sum_bar2 vdd vdd2 gnd Lg=20n 
Xbuffer1 Ain A vdd2 gnd buffer size='1' Lg='Lg'
Xbuffer2 Bin B vdd2 gnd buffer size='1' Lg='Lg'
* Carry-block 
* Cout = AB + (A+B)Cin
* PDN:
Mn1 Cout_bar Cin mn1_source gnd nfet L='Lg' NFIN='1'
Mn2 mn1_source A gnd gnd nfet L='Lg' NFIN='1'
Mn3 mn1_source B gnd gnd nfet L='Lg' NFIN='1'
Mn4 Cout_bar A mn4_source gnd nfet L='Lg' NFIN='1'
Mn5 mn4_source B gnd gnd nfet L='Lg' NFIN='1'
* PUN:
Mp1 Cout_bar Cin mp1_source vdd pfet L='Lg' NFIN='1'
Mp2 mp1_source A vdd vdd pfet L='Lg' NFIN='1'
Mp3 mp1_source B vdd vdd pfet L='Lg' NFIN='1'
Mp4 Cout_bar A mp4_source vdd pfet L='Lg' NFIN='1'
Mp5 mp4_source B vdd vdd pfet L='Lg' NFIN='1'
* Inverter to get Cout
Xinv_cout Cout_bar Cout vdd gnd INV size = '1' Lg = 'Lg'

* Sum-block
* Sum = ABCin + Cout_bar(A + B + Cin)
* PDN:
Mn6 Sum_bar Cout_bar mn6_source gnd nfet L='Lg' NFIN='1'
Mn7 mn6_source A gnd gnd nfet L='Lg' NFIN='1'
Mn8 mn6_source B gnd gnd nfet L='Lg' NFIN='1'
Mn9 mn6_source Cin gnd gnd nfet L='Lg' NFIN='1'
Mn10 Sum_bar Cin mn10_source gnd nfet L='Lg' NFIN='1'
Mn11 mn10_source A Mn11_source gnd nfet L='Lg' NFIN='1'
Mn12 Mn11_source B gnd gnd nfet L='Lg' NFIN='1'
* PUN:
Mp6 Sum_bar Cout_bar mp6_source vdd pfet L='Lg' NFIN='1'
Mp7 mp6_source A vdd vdd pfet L='Lg' NFIN='1'
Mp8 mp6_source B vdd vdd pfet L='Lg' NFIN='1'
Mp9 mp6_source Cin vdd vdd pfet L='Lg' NFIN='1'
Mp10 Sum_bar Cin mp10_source vdd pfet L='Lg' NFIN='1'
Mp11 mp10_source A mp11_source vdd pfet L='Lg' NFIN='1'
Mp12 mp11_source B vdd vdd pfet L='Lg' NFIN='1'
* Inverter to get Sum
Xinv_sum Sum_bar Sum vdd gnd INV size = '1' Lg = 'Lg'
Xinv_sum_bar Sum Sum_bar2 vdd2 gnd INV size = '2' Lg = 'Lg'
.ends

* Sub circuit: FA16_with_buffer
.subckt FA16_with_buffer Ain Bin Cin Cout Sum Sum_bar vdd vdd2 gnd Lg=20n 
Xbuffer1 Ain A vdd2 gnd buffer size='1' Lg='Lg'
Xbuffer2 Bin B vdd2 gnd buffer size='1' Lg='Lg'
* Cout = (AB' + A'B)Cin + (AB + A'B')A
* Sum = A ⊕ B ⊕ Cin
* Module1 : get AB' + A'B and AB + A'B'
Xinv_B B B_bar vdd gnd INV size = '1' Lg = 'Lg'
Mp2 A B AxorB vdd pfet L='Lg' NFIN='1'
Mn2 A B_bar AxorB gnd nfet L='Lg' NFIN='1'
Mn1 B_bar A AxorB gnd nfet L='Lg' NFIN='1'
Mp1 B A AxorB vdd pfet L='Lg' NFIN='1'
Xinv_AxorB AxorB AxnorB vdd gnd INV size = '1' Lg = 'Lg'
* Module2 : get Sum
Mp4 Cin AxorB Sum vdd pfet L='Lg' NFIN='1'
Mn4 Cin AxnorB Sum gnd nfet L='Lg' NFIN='1'
Mn3 AxnorB Cin Sum gnd nfet L='Lg' NFIN='1'
Mp3 AxorB Cin Sum vdd pfet L='Lg' NFIN='1'
* Module3 : get Cout
Mp6 Cin AxnorB Cout vdd pfet L='Lg' NFIN='1'
Mn6 Cin AxorB Cout gnd nfet L='Lg' NFIN='1'
Mp5 A AxorB Cout vdd pfet L='Lg' NFIN='1'
Mn5 A AxnorB Cout gnd nfet L='Lg' NFIN='1'
Xinv_sum_bar Sum Sum_bar vdd2 gnd INV size = '2' Lg = 'Lg'
.ends

* 8 bit Adder using FA16_with_buffer and FA28_with_buffer
.subckt Adder8_2 A0 A1 A2 A3 A4 A5 A6 A7 B0 B1 B2 B3 B4 B5 B6 B7 Cin Cout Sum0 Sum1 Sum2 Sum3 Sum4 Sum5 Sum6 Sum7 vdd vdd2 gnd Lg=20n
XFA0 A0 B0 Cin Cout1   Sum0 Sum_bar0 vdd vdd2 gnd FA28_with_buffer Lg='Lg'
XFA1 A1 B1 Cout1 Cout2 Sum1 Sum_bar1 vdd vdd2 gnd FA16_with_buffer Lg='Lg'
XFA2 A2 B2 Cout2 Cout3 Sum2 Sum_bar2 vdd vdd2 gnd FA28_with_buffer Lg='Lg'
XFA3 A3 B3 Cout3 Cout4 Sum3 Sum_bar3 vdd vdd2 gnd FA16_with_buffer Lg='Lg'
XFA4 A4 B4 Cout4 Cout5 Sum4 Sum_bar4 vdd vdd2 gnd FA28_with_buffer Lg='Lg'
XFA5 A5 B5 Cout5 Cout6 Sum5 Sum_bar5 vdd vdd2 gnd FA16_with_buffer Lg='Lg'
XFA6 A6 B6 Cout6 Cout7 Sum6 Sum_bar6 vdd vdd2 gnd FA28_with_buffer Lg='Lg'
XFA7 A7 B7 Cout7 Cout  Sum7 Sum_bar7 vdd vdd2 gnd FA16_with_buffer Lg='Lg'
.ends

* Source
Vdd VDD GND DC 'SUPPLY'
Vdd2 VDD2 GND DC 'SUPPLY'
VA0 A0 GND DC 'SUPPLY'
VA1 A1 GND DC 'SUPPLY'
VA2 A2 GND DC 'SUPPLY'
VA3 A3 GND DC 'SUPPLY'
VA4 A4 GND DC 'SUPPLY'
VA5 A5 GND DC 'SUPPLY'
VA6 A6 GND DC 'SUPPLY'
VA7 A7 GND DC 'SUPPLY'
VC0 C0 GND PULSE (0 'SUPPLY' 500p 50p 50p 950p 2n)

* Circuit: Testbench for 8 bit Adder with FA28_with_buffer and FA16_with_buffer
* Circuit: Testbench for 8 bit Adder with FA28_with_buffer
Xadder8 A0 A1 A2 A3 A4 A5 A6 A7 GND GND GND GND GND GND GND GND C0 Cout Sum0 Sum1 Sum2 Sum3 Sum4 Sum5 Sum6 Sum7 VDD VDD2 GND Adder8_2 Lg='Lg'

.tran 1p 5n
.probe V(*) I(*)
* C0 -> C8
.measure tran tpLH_C0toCout TRIG V(C0) VAL='0.5*SUPPLY' RISE=2 TARG V(Cout) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL_C0toCout TRIG V(C0) VAL='0.5*SUPPLY' FALL=2 TARG V(Cout) VAL='0.5*SUPPLY' FALL=2
.measure tran tp_C0toCout PARAM='(tpLH_C0toCout+tpHL_C0toCout)/2'
* C0 -> S7
.measure tran tpLH_C0toS7 TRIG V(C0) VAL='0.5*SUPPLY' FALL=2 TARG V(Sum7) VAL='0.5*SUPPLY' RISE=2
.measure tran tpHL_C0toS7 TRIG V(C0) VAL='0.5*SUPPLY' RISE=2 TARG V(Sum7) VAL='0.5*SUPPLY' FALL=2
.measure tran tp_C0toS7 PARAM='(tpLH_C0toS7+tpHL_C0toS7)/2'
.end