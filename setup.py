from setuptools import setup, find_packages

setup(
    name="contacts",
    version="0.1",
    packages=find_packages(),
    scripts=["contacts.py"],
    # metadata to display on PyPI
    author="Andrew Lighten",
    author_email="andrew@digital-ironworks.com",
    description="Contact manager",
    keywords="contacts",
    classifiers=["License :: OSI Approved :: Python Software Foundation License"],
    entry_points={"console_scripts": ["contacts = contacts:main",],},
    python_requires=">=3.7.5",
)
