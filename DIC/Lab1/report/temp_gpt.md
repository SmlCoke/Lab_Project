我看完了你最新的报告稿子（`template.pdf`），你的 **Technical Analysis** 部分已经写得很完整了，现在就缺最后的 **Observations and conclusions**。你问的那个问题（为什么温度升高时 FinFET 的 Ioff 增加更剧烈）其实是合理的：

* FinFET 由于强电场控制，阈值电压的温度敏感性更大（表格里 VT 在升温时下降的比例远大于 bulk）。
* 一旦 VT 显著下降，亚阈区的电流公式 (I_{sub} \propto e^{(V_{GS}-V_T)/(nV_T)}) 中的指数项变化更敏感，导致 Ioff 在升温时放大得更厉害。
* 同时，载流子迁移率在高温下下降，而 FinFET 的导通电流主要受限于电荷调控，因此 Ioff 对温度变化的响应比 bulk 更明显。

所以，你的观察符合物理机理，可以放心写进结论。

下面我帮你写一个适合作为 **第 4 部分 Observations and conclusions** 的版本，你可以直接放进报告：

---

### 4 Observations and Conclusions

From the simulation experiments, several key observations can be made:

1. **Temperature dependence:**
   Both bulk Si-MOSFETs and FinFETs experience an increase in off-state leakage current (Ioff) with rising temperature. However, the increase is much more pronounced in FinFETs. This is consistent with the stronger temperature sensitivity of FinFET threshold voltage, which drops significantly as temperature rises. The sharp reduction in VT shifts the device into stronger inversion even at low gate voltages, resulting in a dramatic Ioff increase.

2. **On-state current stability:**
   Although Ion decreases slightly with temperature due to mobility degradation, the reduction is relatively modest compared to the exponential growth of Ioff. This explains why the Ion/Ioff ratio deteriorates so rapidly, particularly for FinFETs.

3. **Device comparison:**
   At room temperature, FinFETs clearly outperform bulk MOSFETs with lower leakage current, higher Ion/Ioff ratio, and steeper subthreshold slope. But at elevated temperature, while FinFETs still maintain advantages, their Ioff increases faster than in bulk devices, narrowing the performance gap.

4. **Practical implications:**
   These results highlight the importance of thermal management in nanoscale devices. Although FinFETs offer excellent electrostatic control and reduced leakage at nominal temperature, their leakage performance can degrade quickly at high temperatures. This must be carefully considered in low-power circuit design.

5. **Learning outcomes:**
   This lab provided a concrete understanding of how fundamental device parameters (Ion, Ioff, VT, SS) are extracted from simulation and how they reflect underlying physics. Comparing bulk MOSFETs with FinFETs deepened the understanding of short-channel effects, leakage mechanisms, and temperature dependencies. The experiment closely connects simulation practice with theoretical knowledge from class, reinforcing why advanced device structures such as FinFETs are necessary in deep-submicron technologies.

---

要不要我帮你把这个 Observations and Conclusions 部分直接插进你的 `template.pdf`（就是接在第 3 部分后面），生成一份完整的最终实验报告？
