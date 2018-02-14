from setuptools import setup

setup(
    name="marc2iiif",
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    version="2.0.0",
    license="LGPL3.0",
    description="An application to convert MARC records into IIIF records",
    keywords="python3.6 iiif-presentation manifests",
    packages=['marc2iiif'],
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Processing :: Markup :: XML",
    ]
)
