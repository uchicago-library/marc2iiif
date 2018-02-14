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
    entry_points={
        'console_scripts': [
            'test = marc2iiif.test:main'
        ]
    },
    
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Processing :: Markup :: XML",
    ]
)
