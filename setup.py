from setuptools import find_packages, setup

setup(
    name="flows",
    version="0.0.0",
    description="Prefect examples",
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["py.typed"],
    },
    install_requires=["prefect==1.4.1", "prefect-memory-profiling==1.0.0", "dask_kubernetes==2023.3.2"],
    extras_require={
        "dev": [
            "autoflake~=2.0",
            "black~=23.3",
            "build~=0.10",
            "isort~=5.12",
            "flake8~=6.0",
            "flake8-annotations~=3.0",
            "flake8-colors~=0.1",
            "pre-commit~=2.20",
            "pytest~=7.3",
        ]
    },
)
