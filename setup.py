import setuptools

import explicatio.version

VERSION = explicatio.version.__version__

setuptools.setup(
    name="Explicatio",
    version=VERSION,
    author="Bryan Smith",
    author_email="bryanabsmith@gmail.com",
    description="A simple analysis tool for text.",
    url="http://github.com/bryan-ab-smith/explicatio",
    packages=['explicatio'],
    scripts=['bin/explicatio'],
    install_requires=[
          'colored',
          'nltk'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
