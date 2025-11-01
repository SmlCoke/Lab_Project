* Task1. 
* Ids-Vds curve 
* for nmos and pmos 
* for FinFETs and Bulk Si-MOSFETs
* with scanning fin number(FinFETs) or width(Bulk Si-MOSFETs)

* parameter config
.param lambda=8nm
.param Width='16*lambda'
.param Vgs_n=0.75
.param Vgs_p=-0.75
.temp 25

* lib config
.include '../Lab_LIB/Bulk/16nm_HP.pm'

* output file config
.option post=2 


* motivation source for nmos
VGS_N gate_n 0 'Vgs_n'
VDS_N drain_n 0 0

* motivation source for nmos
VGS_P gate_p 0 'Vgs_p'
VDS_P drain_p 0 0

* Bulk device definition for NMOS
MNFET drain_n gate_n 0 0 nmos L='2*lambda' W='Width'

* Bulk device definition for PMOS
MPFET drain_p gate_p 0 0 pmos L='2*lambda' W='Width'

* DC analysis - Sweep VDS from 0 to 0.85V for different fin numbers
.dc VDS_N 0 0.85 0.01 sweep Width '16*lambda' '48*lambda' '8*lambda'
.probe DC I(VDS_N) 

.dc VDS_P 0 -0.85 -0.01 sweep Width '16*lambda' '48*lambda' '8*lambda'
.probe DC I(VDS_P)

.end