import setuptools
from version import VERSION

with open("README.md", "r") as file:
    readme = file.read()

setuptools.setup(
    name="quick-password-generator",
    version=VERSION,
    author="ablil",
    author_email="ablil@protonmail.com",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["qpg = src.__main__:main"]},
    description="quick password generator with cache support",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/quick-password-generator",
    classifers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)