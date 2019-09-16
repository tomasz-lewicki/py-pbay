import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-pbay",
    version="0.0.1",
    author="Tomasz Lewicki",
    author_email="t.w.lewicki@gmail.com",
    description="A python driver for PBay board",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomek-l/py-pbay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)