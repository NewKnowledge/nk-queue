from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nk_queue",
    version="1.0.0",
    description="A redis queue wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NewKnowledge/nk-queue",
    packages=["nk_queue"],
    include_package_data=True,
    install_requires=["redis>=3.3.1", "kafka"],
    license="MIT",
)
