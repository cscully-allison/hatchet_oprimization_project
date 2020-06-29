from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("np_timing.pyx", annotate=True)
)
