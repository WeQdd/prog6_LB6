from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "fermat_cy.pyx",
        annotate=True,  # Для генерации html-аннотации
        compiler_directives={'language_level': "3"}
    )
)