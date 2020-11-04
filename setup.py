import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jose5",
    version="0.1.0",
    author="Aplazame",
    author_email="dev@aplazame.com",
    description="JSON Composer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aplazame/jose5",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
