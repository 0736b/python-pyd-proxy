from Cython.Distutils import build_ext
from setuptools import Extension, setup

ext_modules = [Extension("brain", ["brain.py"])]
setup(
    name="brain",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
