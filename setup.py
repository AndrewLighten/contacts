from setuptools import setup, find_packages

setup(
    name="contacts",
    version="0.2",
    packages=find_packages(),
    scripts=["contacts.py"],
    # metadata to display on PyPI
    author="Andrew Lighten",
    author_email="andrew@digital-ironworks.com",
    description="Contact manager",
    long_description="A tool for searching and displaying contact details based on command line queries",
    keywords="contacts",
    classifiers=["Development Status :: 4 - Beta", "License :: OSI Approved :: Apache Software License", "Intended Audience :: End Users/Desktop"],
    entry_points={"console_scripts": ["contacts = contacts:main",],},
    python_requires=">=3.7.5",
    license="https://www.apache.org/licenses/LICENSE-2.0",
    url="https://github.com/AndrewLighten/contacts",
    platforms=["Operating System :: MacOS :: MacOS X", "Operating System :: POSIX :: Linux"]
)
