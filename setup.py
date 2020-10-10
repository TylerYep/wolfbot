""" setup.py """
import setuptools

with open("README.md") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="wolfbot",
    version="0.0.1",
    author="Tyler Yep",
    author_email="tyep10@gmail.com",
    description="One Night Ultimate Werewolf: AI Edition",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tyleryep/wolfbot",
    packages=["src"],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
