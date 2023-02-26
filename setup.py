import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="incharge",
    version="0.0.2",
    author="Tim van Grieken",
    author_email="tgriek@gmail.com",
    description="A package to talk to the VattenFall InCharge API's",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgriek/incharge",
    packages=['incharge'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
)
