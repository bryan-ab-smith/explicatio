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

#### Supported Input Formats
Explicatio uses [textract](https://textract.readthedocs.io/en/stable/) to import content. Formats supported by explicatio for reading are therefore those supported by textract. Whatever you open, you are encouraged to verify that the content explicatio is working with is what you expect it to be by running the `showcontents` command after loading a file. If in doubt, your best bet is to put the text you want to work with in a plain text file and go from there.

### Running and Packaging

#### Running
If you want to run this without installing, run explicatio like so:

    python3 explicatio/__init__.py

#### Packaging
Packaging explicatio as a Python wheel is as easy as running the build script:

    python3 -m build

The resulting wheel will be in dist/.

If you're on a machine with ZSH support, you can also run the `build.sh`3 script which runs the build command and cleans up the source directory a bit.


### Licence

Copyright 2022 Bryan Smith.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.