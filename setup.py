from setuptools import setup

setup(
    name="marc2iiif",
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    version="0.1.0",
    license="LGPL3.0",
    description="An application to convert MARC records into IIIF records",
    keywords="python3.6 iiif-presentation manifests marc",
    packages=['marc2iiif'],
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser " +
        "General Public License (LGPL)",
        "Development Status :: 5 - Alpha/Prototype",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    dependency_links = [
        'https://github.com/uchicago-library/pyiiif/tarball/master#egg=pyiiif'
    ],
    install_requires = [
        'pymarc'

    ]
)
