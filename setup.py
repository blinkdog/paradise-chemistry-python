import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paradise-chemistry",
    version="0.0.2",
    author="Patrick Meade",
    author_email="blinkdog@protonmail.com",
    description="Helper program for Chemistry on Paradise Station (SS13)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blinkdog/paradise-chemistry-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ]
)
