* Task2. 
* Metrics to be Measured 
* for nmos and pmos 
* for FinFETs
* for temp=25 and 90
* for supply = 0.75
* fin number = 2
* measure VTH: VTH is the value of VGS when IDS = 0.3*W/L

* parameter config
.param fin_height=26n
.param fin_width=12n
.param Lg_fin=20n
.param supply=0.75
.param Nfin=2
.param Width = '2*(2*fin_height + fin_width)'
.temp  25

* lib config
.include '../../../Lab_LIB/FINFET/modelfiles/hp/16nfet.pm'
.include '../../../Lab_LIB/FINFET/modelfiles/hp/16pfet.pm'

* output file config
.option post=2 


* motivation source for nmos
VG_N gate_n gnd 'supply'
VD_N drain_n gnd 'supply'
VS_N source_n gnd 0

* motivation source for nmos
VG_P gate_p  gnd '-supply'
VD_P drain_p gnd '-supply'
VS_P source_p gnd 0

* FinFET device definition for NMOS
MNFET drain_n gate_n source_n gnd nfet L='Lg_fin' NFIN='Nfin' 
+ tfin='fin_width' hfin='fin_height'

* FinFET device definition for PMOS
MPFET drain_p gate_p source_p gnd pfet L='Lg_fin' NFIN='Nfin' 
+ tfin='fin_width' hfin='fin_height'

************ temperature = 25 *****************
.dc VG_N 0 0.8 0.01
.probe DC I(VG_N)
.measure DC VTH_n FIND V(gate_n) WHEN I(VD_N) = '-0.3u*Width/Lg_fin'
.dc VG_P 0 -0.8 -0.01
.probe DC I(VG_P)
.measure DC VTH_p FIND V(gate_p) WHEN I(VD_P) = '0.3u*Width/Lg_fin'
************ temperature = 90 *****************
.alter
.temp 90
.dc VG_N 0 0.8 0.01
.probe DC I(VG_N)
.measure DC VTH_n FIND V(gate_n) WHEN I(VD_N) = '-0.3u*Width/Lg_fin'
.dc VG_P 0 -0.8 -0.01 
.probe DC I(VG_P)
.measure DC VTH_p FIND V(gate_p) WHEN I(VD_P) = '0.3u*Width/Lg_fin'

.end