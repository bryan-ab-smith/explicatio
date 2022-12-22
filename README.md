## Explicatio

Explicatio (noun): Latin for "explanation"

**NOTE: This is nowhere near being usable at this point. Explicatio is still very much under development.**

### Description
This is the home of an in development piece of software to support text analysis. More to come. Currently, explicatio supports:
* Sentiment analysis
* Dispersion plots
* Concordance
* Collocations
* Frequency distributions
* Parts of speech breakdown
* Text summarisation

### Running and Packaging

#### Running
If you want to run this without installing, run explicatio like so:

    python3 explicatio/__init__.py

#### Packaging
Packaging explicatio as a Python wheel is as easy as running build:

    python3 -m build

The resulting wheel will be in dist/. Install it with the following:

    python3 -m pip install dist/NAME_OF_WHL (where NAME_OF_WHL is the name of the wheel (.whl) file).

If you're on a machine with ZSH support, you can also run the `build.sh` script which runs the build command and cleans up the source directory a bit.

### Using Explicatio

#### Configuring
You can configure Explicatio by editing the config.ini file (either in explicatio/ or, if the wheel is installed, see the output of the about command) or by using the built in `config` command and passing three parameters: a section, a property, a value. Not sure what the section and property values are? See below.

| Section | Property | Details | Command That Uses This Property |
|---|---|---|---|
| MODELS | summarisation | This is the machine learning model that serves to summarise the text. | summary
| MODELS | question | This is the machine learning model that serves to answer questions asked of the text. | question |

So, to configure explicatio to use a different machine learning model for summarisation, you would execute the following:

    config MODELS summarisation NAME_OF_MODEL (where NAME_OF_MODEL is the model)

For any changes to take effect, whether by manually editing the config file or by way of the `config` command, you will need to restart Explicatio.

#### Supported Input Formats
Explicatio uses [textract](https://textract.readthedocs.io/en/stable/) to import content. Formats supported by explicatio for reading are therefore those supported by textract. Whatever you open, you are encouraged to verify that the content explicatio is working with is what you expect it to be by running the `showcontents` command after loading a file. If in doubt, your best bet is to put the text you want to work with in a plain text file and go from there.


#### Building
The app is not really designed to be compiled but it should work with Nuitka:

    export TCL_LIBRARY=<path to TCL-TK> && export TK_LIBRARY=<path to TCL-TK> && python3 -m nuitka __init__.py --onefile --enable-plugin=tk-inter --enable-plugin=numpy

For this to work, TCL (tcl-tk through Homebrew on macOS) and a C compiler (eg. gcc, clang) need to be installed.

NOTE: This is not actively tested nor is it a priority if this doesn't work.

### Documentation
Documentation for explicatio is provided by way of pandoc. To build the documentation, you will need to install Pandoc first (see [here](https://pandoc.org/installing.html)) and then run the build script in docs/pandocs:

    sh ./build.sh

The docs will be generated and made available in the docs/pandocs/output directory. As of now, the following is made:
* HTML
* Man page (which is installed with the build script)
* PDF (if LateX is installed)

### Licence

Copyright 2022 Bryan Smith.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.