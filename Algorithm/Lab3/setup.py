from setuptools import setup, Extension
import sys
import pybind11

extra_compile_args = []
if sys.platform == "win32":
    extra_compile_args = ["/std:c++17", "/O2", "/utf-8"]

ext_modules = [
    Extension(
        "sa_core",
        sources=["sa_bindings.cpp"], 
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=extra_compile_args,
    )
]

setup(
    name="sa_core",
    version="0.1",
    ext_modules=ext_modules,
)