from setuptools import setup, find_packages

setup(
    name="libcatalyst",
    version="0.1.0",
    description="Python library for interfacing with Ocupoint hardware devices.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OcupointInc/Libcatalyst-Python.git",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'pyftdi'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
