#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "sa_core.cpp"

namespace py = pybind11;

py::tuple run_sa(
    int w_ref,
    const std::vector<std::string>& nets,
    const std::vector<int>& pins,
    const std::vector<Mos>& pmos_ary,
    const std::vector<Mos>& nmos_ary,
    const std::vector<std::optional<Mos>>& pp_ary,
    const std::vector<std::optional<Mos>>& np_ary,
    double t0,
    double tt,
    double decrease,
    int times,
    const std::string& data_filename = "" // fj_pro: 记录退火过程中得分的数据文件名字
) {
    auto res = simulated_annealing_cpp(
        w_ref, nets, pins,
        pmos_ary, nmos_ary,
        pp_ary, np_ary,
        t0, tt, decrease, times, data_filename // fj_pro: 传入数据文件名字
    );

    std::vector<Mos> new_pmos, new_nmos;
    std::vector<std::optional<Mos>> new_pp, new_np;
    std::tie(new_pmos, new_nmos, new_pp, new_np) = res;

    return py::make_tuple(new_pmos, new_nmos, new_pp, new_np);
}

PYBIND11_MODULE(sa_core, m) {
    py::class_<Mos>(m, "Mos")
        .def(py::init<>())
        .def_readwrite("name", &Mos::name)
        .def_readwrite("id", &Mos::id)
        .def_readwrite("x", &Mos::x)
        .def_readwrite("s", &Mos::s)
        .def_readwrite("g", &Mos::g)
        .def_readwrite("d", &Mos::d)
        .def_readwrite("w", &Mos::w);

    // m.def("run_sa", &run_sa, "Run simulated annealing core");

    // fj_pro: 修改为带有 data_filename 参数的 run_sa
    m.def("run_sa", &run_sa, "Run simulated annealing core",
        py::arg("w_ref"),
        py::arg("nets"),
        py::arg("pins"),
        py::arg("pmos_ary"),
        py::arg("nmos_ary"),
        py::arg("pp_ary"),
        py::arg("np_ary"),
        py::arg("t0"),
        py::arg("tt"),
        py::arg("decrease"),
        py::arg("times"),
        py::arg("data_filename") = "" // [新增] 允许 Python 调用时不传此参数
    );
}