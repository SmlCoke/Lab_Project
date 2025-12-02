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
    int times
) {
    auto res = simulated_annealing_cpp(
        w_ref, nets, pins,
        pmos_ary, nmos_ary,
        pp_ary, np_ary,
        t0, tt, decrease, times
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

    m.def("run_sa", &run_sa, "Run simulated annealing core");
}