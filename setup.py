import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="surviv_py_olliroxx",
    version="0.0.1",
    author="Olliroxx",
    description="Documentation and client for surviv.io",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Olliroxx/surviv.py",
    project_urls={
        "Bug Tracker": "https://github.com/Olliroxx/surviv.py/issues/",
        "Documentations": "https://survivpy.readthedocs.io/",
        "Source": "https://github.com/Olliroxx/surviv.py/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GPLv3+",
        "Development Status :: 3 - Alpha",
    ],
    keywords="surviv surviv.io game",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
