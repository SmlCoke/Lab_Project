* Task1. 
* Ids-Vds curve 
* for nmos and pmos 
* for FinFETs and Bulk Si-MOSFETs
* with scanning fin number(FinFETs) or width(Bulk Si-MOSFETs)

* parameter config
.param fin_height=26n
.param fin_width=12n
.param Lg_fin=20n
.param Vgs_n=0.75
.param Vgs_p=-0.75
.param Nfin=4
.temp 25

* lib config
.include '../Lab_LIB/FINFET/modelfiles/hp/16nfet.pm'
.include '../Lab_LIB/FINFET/modelfiles/hp/16pfet.pm'


* output file config
.option post=2 


* motivation source for nmos
VGS_N gate_n 0 'Vgs_n'
VDS_N drain_n 0 0

* motivation source for nmos
VGS_P gate_p 0 'Vgs_p'
VDS_P drain_p 0 0

* FinFET device definition for NMOS
MNFET drain_n gate_n 0 0 nfet L='Lg_fin' NFIN='Nfin' 
+ tfin='fin_width' hfin='fin_height'

* FinFET device definition for PMOS
MPFET drain_p gate_p 0 0 pfet L='Lg_fin' NFIN='Nfin' 
+ tfin='fin_width' hfin='fin_height'

* DC analysis - Sweep VDS from 0 to 0.85V for different fin numbers
.dc VDS_N 0 0.85 0.01 sweep Nfin 4 8 2
.probe DC I(VDS_N) 
.dc VDS_P 0 -0.85 -0.01 sweep Nfin 4 8 2
.probe DC I(VDS_P)

.end