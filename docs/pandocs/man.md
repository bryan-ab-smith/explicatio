<!-- Based on https://pandoc.org/demo/pandoc.1.md -->

# NAME

explicatio - text analysis tool

# SYNOPSIS

explicatio

# DESCRIPTION

Explicatio (noun): Latin for "explanation"

This is the home of an in development piece of software to support text analysis. More to come. Currently, explicatio supports:
* Sentiment analysis
* Dispersion plots
* Concordance
* Collocations
* Frequency distributions
* Parts of speech breakdown
* Text summarisation

# COMMANDS

load *FILENAME*
:   load *FILENAME* file for analysis. You can
    pass anything that is supported by textract. 
    This is a flexible library that can 
    import a lot of content but you are strongly
    encouraged to ensure that the file is 
    loaded as you wish by executing showcontents.

showcontents
:   Show the contents of the file that explicatio
    is working with. This is helpful to ensure that 
    explicatio is working with the text in a form 
    that you accept for analysis. If you import a 
    text, it is possible for parts to be excluded 
    or converted in a way that challenges accurate 
    analysis. This function gives you the chance 
    to make sure that you and explicatio are working 
    with the same text.

sentiment
:   Run a sentiment analysis on the text. This can 
    be used to give you a sense of the emotional 
    tone of the text. The function returns four 
    values, one of which consolidates the other 
    three to give you an overall score for the 
    sentiment expressed in the text. Reports back
    four values: negative, positive, neutral, and
    compound (the overall score).

dispersion *LIST_OF_WORDS*
:   This can be used to see where a *LIST_OF_WORDS* 
    are in the text and compare them against each 
    other. In effect, this shows you the spread of 
    words across a text and in allowing you to do 
    this with multiple words, you can see how the 
    spread of various word compare. *LIST_OF_WORDS* 
    is a semi-colon delimited set of words. For
    example, *LIST_OF_WORDS* could be
    `dracula;vampire`.

concordance *WORD* *NUM_RESULTS*
:   Run a concordance. This can be used to see 
    where a *WORD* is sitauted in the text with the 
    context around it. Running a concordance can 
    thus provide insight into the contextual use of 
    the word by providing a sense of the words 
    before and after it. The *NUM_RESULTS* sets how 
    many results will be shown.

collocations
:   Run a collocation. This can be used to see what 
    words are commonly collocated (or co-located) 
    with each other. This can help with finding 
    common noun phrases for example.

freqdist *NUM_WORDS*
:   Run a frequency distribution. This can be used 
    to see what the most common words are in a corpus.
    *NUM_WORDS* will determine how many words to show
    in the results.