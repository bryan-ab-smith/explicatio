### Explicatio

**NOTE: This is nowhere near being usable at this point. Explicatio is still very much under development.**

#### Description
This is the home of an in development piece of software to support text 
analysis. More to come.

### Running and Packaging

#### Running
If you want to run this without installing, run explicatio like so:

    python3 explicatio/__init__.py

#### Packaging
Packaging explicatio as a Python wheel is as easy as running the build script:

    sh build.sh

NOTE: The build script is macOS/Linux/*nix only. On Windows, you will need to run the setup script yourself and clean up the build directories:

    python3 setup.py bdist_wheel