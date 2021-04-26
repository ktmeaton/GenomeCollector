import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as r:
    require_list = r.read().strip().split("\n")

setuptools.setup(
    name="NCBImeta",
    version="0.8.1dev",
    description=(
        "Efficient and comprehensive metadata acquisition "
        "from the NCBI databases (includes SRA)."
    ),
    python_requires=">=3.6,<3.9",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Katherine Eaton",
    author_email="ktmeaton@gmail.com",
    url="https://ktmeaton.github.io/NCBImeta/",
    # packages=setuptools.find_packages(),
    packages=["ncbimeta"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=require_list,  # external packages as dependencies
    extras_require={
        "dev": [
            "coverage==4.5.4",
            "codecov==2.0.15",
            "pytest==5.3.1",
            "pytest-cov==2.8.1",
            "check-manifest==0.42",
            "twine==3.2.0",
            "pre-commit<=2.6.0",
            "sphinx==3.2.1",
            "sphinx-rtd-theme==0.5.0",
            "m2r==0.2.1",
            "flake8==3.8.3",
            "flake8-bugbear==20.1.4",
            "black==19.10b0",
        ]
    },
    scripts=[
        "ncbimeta/NCBImeta",
        "ncbimeta/NCBImetaExport",
        "ncbimeta/NCBImetaJoin",
        "ncbimeta/NCBImetaAnnotateReplace",
        "ncbimeta/NCBImetaAnnotateConcatenate",
    ],
)
