from setuptools import setup, find_packages
setup(
    name="unhingedmf",
    version="0.1",
    py_modules=["unhingedmf"],
    entry_points={
        "console_scripts": [
            "unhingedmf = unhingedmf:main",
        ],
    },
)
