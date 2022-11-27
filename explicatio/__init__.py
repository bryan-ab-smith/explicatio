#!/usr/bin/env python

# Built-ins
import cmd
import configparser
from collections import Counter
import mimetypes
import os
import platform
import sys
# https://stackoverflow.com/a/25823885
from timeit import default_timer as timer
import tkinter
from tkinter import filedialog as fd

# Third party modules
import colored
from colored import stylize
from transformers import pipeline
from halo import Halo
from matplotlib import pyplot as plt
import nltk
from nltk import tokenize, FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import textract

# Version numbering.
__version__ = '2022.10'
__version__ = 1.0
NLTK_VERSION = nltk.__version__
PY_VERSION = platform.python_version()

# A lot of the following was supported by the following:
#   - https://realpython.com/nltk-nlp-python/


class Explicatio(cmd.Cmd):

    try:
        ver_check = requests.get(
            'https://bryanabsmith.com/explicatio/version.txt'
        )
        ver_check = float(ver_check.text)

        if ver_check > __version__:
            print(
                stylize(
                    'Your version of explicatio is out of date. Version'
                    f' {ver_check} is available.\n'
                    'Head over to the explicatio homepage for upgrade'
                    ' instructions.\n',
                    colored.fg('yellow')
                )
            )
        else:
            print(
                stylize(
                    '\U0001F44F Your version of explicatio is up to date.',
                    colored.fg('green')
                )
            )
    except requests.exceptions.ConnectionError:
        print(
            stylize(
                '! Can\'t see if you\'re up to date. A check will be run next'
                ' time you open explicatio.',
                colored.fg('yellow')
            )
        )

    intro = stylize(
        '\nWelcome to the explicatio shell.'
        'Type help or ? to list commands.\n',
        colored.fg('green')
    )
    prompt = stylize(
        '[explicatio] ',
        colored.fg('cyan')
    )
    filename = None
    data = ''
    word_tokens = []

    config = configparser.ConfigParser()
    # https://stackoverflow.com/a/595315
    config_path = os.path.abspath(os.path.dirname(__file__))
    config.read(f'{config_path}/config.ini')

    summary_model = config['MODELS']['summarisation']
    question_model = config['MODELS']['question']

    def reportError(self, text):
        print(
            stylize(
                f'[ERROR] {text}',
                colored.fg('red')
            )
        )

    def do_load(self, arg):
        '''
        Load a file for analysis.

        You can pass anything that is supported by textract. This is a flexible
        library that can import a lot of content but you are strongly
        encouraged to ensure that the file is loaded as you wish by executing
        showcontents.

        Parameters:
            - filename: This must be a resolvable path to the file. If in
                        doubt, use an absolute file path.

        Usage:
            load <filename>

        Output:
            None.

        Example:
            load dracula.txt
        '''

        if arg != '':
            print(f'Loading {arg}...')
            self.filename = arg
        else:
            print('Prompting for file...')
            # https://bytes.com/topic/python/answers/19510-tkfiledialog-without-parent-window
            root = tkinter.Tk()
            root.withdraw()
            # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
            self.filename = fd.askopenfilename()
            root.destroy()

        try:
            self.data = textract.process(self.filename, encoding='utf-8')
            self.data = self.data.decode('utf-8')
            self.word_tokens = nltk.word_tokenize(self.data)
            # https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
            '''stop_words = set(stopwords.words('english'))
            self.corpus_no_stopwords = [
                word for word in self.word_tokens if not word.lower()
                in stop_words
            ]'''
            self.corpus = nltk.Text(self.word_tokens)
            # Below is the corpus without stop words
            # This performs worse than the regular corpus in FreqDist
            # So, it has been held back for now
            # self.corpus = nltk.Text(self.corpus_no_stopwords)
            print(f'Loaded {self.filename}')

            if mimetypes.guess_type(self.filename)[0] != 'text/plain':
                print(
                    stylize(
                        'CAUTION: As you have loaded a non-plain text '
                        'document, you are strongly encouraged to run '
                        '\'showcontents\' to verify what explicatio is '
                        'working with.',
                        colored.fg('yellow')
                    )
                )

            len_text = len(self.data)
            words_text = len(self.data.split())
            unique_words_text = len(set(self.data.split()))
            print(
                stylize(
                    '(Approximate) Quick facts',
                    colored.fg('blue')
                )
            )
            print(
                stylize(
                    f'  Characters: {len_text:,}',
                    colored.fg('green')
                )
            )
            print(
                stylize(
                    f'  Words: {words_text:,}',
                    colored.fg('green')
                )
            )
            unique_percent = round(
                (unique_words_text/words_text)*100,
                2
            )
            print(
                stylize(
                    f'  Unique Words: {unique_words_text:,} '
                    f'({unique_percent}%)',
                    colored.fg('green')
                )
            )
            print(
                stylize(
                    'NOTE: This is indicative of a sense of the size of the '
                    'file, not a measurement that should be used to draw '
                    'conclusions.',
                    colored.fg('red')
                )
            )

            self.prompt = stylize(
                f'[explicatio -> {self.filename}] ',
                colored.fg('cyan')
            )
        except (
            FileNotFoundError,
            textract.exceptions.MissingFileError
        ):
            self.reportError(f'{self.filename} was not found')

    def do_showcontents(self, arg):
        '''
        Show the contents of the file that explicatio is working with.

        This is helpful to ensure that explicatio is working with the
        text in a form that you accept for analysis. If you import a
        text, it is possible for parts to be excluded or converted in
        a way that challenges accurate analysis. This function gives
        you the chance to make sure that you and explicatio are
        worlking with the same text.

        Parameters:
            None.

        Usage:
            showcontents

        Output:
            The contents of the file.

        Example:
            showcontents
        '''

        if self.filename is not None:
            print(self.data)
        else:
            self.reportError('Please load a file first.')

    def do_sentiment(self, arg):
        '''
        Run a sentiment analysis on the text.

        This can be used to give you a sense of the emotional tone of
        the text. The function returns four values, one of which
        consolidates the other three to give you an overall score for
        the sentiment expressed in the text.

        Parameters:
            None.

        Usage:
            sentiment

        Output:
            - Negative: the negative score.
            - Positive: the positive score.
            - Neutral: the neutral score.
            - Compound: the compound score (what you're likely looking for).

        Example:
            sentiment
        '''

        if self.filename is not None:
            start = timer()
            sents = tokenize.sent_tokenize(self.data)
            # https://www.nltk.org/howto/sentiment.html
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(sents[2])
            end = timer()
            print(
                '[Sentiment Scores (Vader)]\n',
                stylize(
                    f'Negative: {scores["neg"]}\n',
                    colored.fg('red')
                ),
                stylize(
                    f'Positive: {scores["pos"]}\n',
                    colored.fg('green')
                ),
                stylize(
                    f'Neutral: {scores["neu"]}\n',
                    colored.fg('yellow')
                ),
                stylize(
                    f'Compound: {scores["compound"]}\n',
                    colored.fg('blue')
                ),
            )
            print(f'Elapsed time: {end-start:.2f} seconds.')
        else:
            self.reportError('Please load a file first.')

    def do_dispersion(self, arg):
        '''
        Run a dispersion plot.

        This can be used to see where a list of words are in the text
        and compare them against each other. In effect, this shows you
        the spread of words across a text and in allowing you to do
        this with multiple words, you can see how the spread of various
        word compare.

        Parameters:
            - list_of_words: A semi-colon delimited set of words.

        Usage:
            dispersion <list_of_words>

        Output:
            A graph that shows the dispersion of the semi-colon delimited
            list of words.

        Example:
            dispersion Dracula;vampire
        '''
        args = arg.split(';')

        self.corpus.dispersion_plot(args)

    def do_concordance(self, arg):
        '''
        Run a concordance.

        This can be used to see where a word is sitauted in the text
        with the context around it. Running a concordance can thus
        provide insight into the contextual use of the word by
        providing a sense of the words before and after it.

        Parameters:
            - word: The word to run the concordance on.
            - num_results: Number of results to show. It is
                           possible that the number of results shown
                           will be lower than the value provided here
                           if there are fewer results than the value
                           requested.

        Usage:
            dispersion <word> <num_results>

        Output:
            A list of <num_results> number of phrases where <word> is in
            the middle.

        Example:
            concordance dracula 10
        '''

        args = arg.split()
        try:
            self.corpus.concordance(args[0], width=80, lines=int(args[1]))
        except AttributeError:
            self.reportError('Please load a file first.')
        except IndexError:
            self.reportError('An argument is missing. Plese try again.')

    def do_collocations(self, arg):
        '''
        Run a collocation.

        This can be used to see what words are commonly collocated
        (or co-located) with each other. This can help with finding
        common noun phrases for example.

        Parameters:
            None.

        Usage:
            collocation

        Output:
            A list of collocated words.

        Example:
            collocation
        '''

        try:
            self.corpus.collocations()
        except AttributeError:
            self.reportError(
                'It would appear that a corpus isn\'t available. Have you'
                ' loaded a file?'
            )

    def do_freqdist(self, arg):
        '''
        Run a frequency distribution.

        This can be used to see what the most common words are in a corpus.

        Parameters:
            - num_words: The number of words to run a distribution for.
                         This will set how many "top words" to show.

        Usage:
            freqdist <num_words>

        Output:
            A list of the <num_words> most common words.

        Example:
            freqdist 20
        '''

        freq_dist = FreqDist(self.corpus)
        try:
            dist = freq_dist.most_common(int(arg))
            print(f'\nShowing top {arg} words')
            print('Word'.ljust(25) + 'Count')
            for item in dist:
                # The word
                print(item[0].ljust(25), end='')

                # The count
                print(str(f'{item[1]:,}').ljust(25))
            print('\n')
        except ValueError:
            print(
                stylize(
                    'An error occurred. Please make sure to provide '
                    'a number.\n',
                    colored.fg('red')
                )
            )

    # This is a disaster right now.
    def do_posgraph(self, arg):
        'Generate a graph of parts of speech'
        # list_pos = []
        pos = nltk.pos_tag(self.word_tokens)
        # https://www.h2kinfosys.com/blog/simple-statistics-with-nltk-counting-of-pos-tags-and-frequency-distributions/
        count = Counter(tag for _, tag in pos)
        # https://stackoverflow.com/a/37708190
        plt.xticks(rotation=45)
        # https://stackoverflow.com/a/52572237
        plt.bar(count.keys(), count.values())
        plt.show()

    def do_summary(self, arg):
        '''
        Generates a summary of the text.

        This can be used to create a quick sumamry of the text. The
        quality and speed of this depends on the machine learning model
        that explicatio is configured to use. See the models > sumamrisation
        config option.

        Parameters:
            None.

        Usage:
            summary

        Output:
            A summary of the corpus. The length of time it took to generate the
            summary is also provided as a helpful metric for speed (should you
            choose to pursue other options).

        Example:
            summary
        '''

        spinner = Halo(
            text='Summarising. Please wait as this may take a while...\n',
            text_color='yellow',
            spinner='bouncingBall'
        )
        spinner.start()
        start = timer()
        # https://huggingface.co/facebook/bart-large-cnn
        summarizer = pipeline('summarization', model=self.summary_model)
        end = timer()
        print('\n\n',
              summarizer(
                    self.data,
                    truncation=True
                )[0]['summary_text']
              )
        spinner.stop()
        print(f'Elapsed time: {end-start:.2f} seconds.')

    def do_question(self, arg):
        '''
        Ask a question of the corpus.

        This can be used to quickly "question" the corpus and
        get an answer back. As this leverages a machine learning model,
        this should (as always) be taken with a grain of salt.

        Parameters:
            - query: the question to ask

        Usage:
            question <query>

        Output:
            An answer to the <query>. The length of time it took to generate
            the answer is also provided as a helpful metric for speed (should
            you choose to pursue other options). A confidence value is also
            provided to give you a sense of how confident the model is in its
            answer.

        Example:
            question Who is Dracula?
        '''

        print(
                stylize(
                    f'Using {self.question_model} model.\n'
                    f'Answering the question, "{arg}"',
                    colored.fg('blue')
                )
            )

        spinner = Halo(
            text='Please wait',
            text_color='yellow',
            spinner='bouncingBall'
        )
        spinner.start()

        start = timer()
        answerer = pipeline(
            'question-answering',
            model=self.question_model,
            tokenizer=self.question_model
        )

        question = {
            'question': arg,
            'context': self.data
        }

        result = answerer(question)
        end = timer()
        spinner.stop()

        score = result['score']
        answer = result['answer']
        print(f'The answer is {answer}. I am {score*100:.2f}% confident.')
        print(f'Elapsed time: {end-start:.2f} seconds.')

    def do_config(self, arg):
        '''
        Set configuration options.

        This can be used to quickly set configuration options. Using this
        requires you to know which section and property the configuration
        option can be found. This information is available in the help
        documentation. The app needs to be restarted for these values to
        take effect.

        Parameters:
            - section: the section in which the config property is found
            - property: the specific property to set
            - value: the value to set for the property

        Usage:
            config <section> <property> <value>

        Output:
            None.

        Example:
            config MODELS summarisation facebook/bart-large-cnn
        '''
        args = arg.split()
        self.config[args[0]][args[1]] = args[2]
        with open(f'{self.config_path}/config.ini', 'w') as conf:
            self.config.write(conf)
        print(
            stylize(
                'Restart explicatio to load saved changes.',
                colored.fg('red')
            )
        )

    def do_about(self, arg):
        'About explicatio'
        print(
            stylize(
                'Versions',
                colored.fg('spring_green_1')
            )
        )
        print(f'Explicatio: {__version__}')
        print(f'  NLTK: {NLTK_VERSION}')
        print(f'  Python: {PY_VERSION}')

        print(
            stylize(
                '\nConfiguration',
                colored.fg('spring_green_1')
            )
        )

        print(f'File: {self.config_path}/config.ini')
        print(f'  Summarisation model: {self.summary_model}')
        print(f'  Question (and answer) model: {self.question_model}')

    def do_quit(self, arg):
        'Quit explicatio'
        print('Thanks for using explicatio!')
        sys.exit(0)

    def do_exit(self, arg):
        'Exit explicatio'
        print('Thanks for using explicatio!')
        sys.exit(0)


if __name__ == '__main__':
    # Quick and easy way to see if NLTK data is downloaded.
    if os.path.exists(nltk.data.path[0]) is False:
        spinner = Halo(
            text='NLTK data not found. Downloading to '
                 f'{nltk.data.path[0]}. '
                 'This may take a while.',
            text_color='red',
            spinner='bouncingBall'
        )
        spinner.start()
        # Download all NLTK data just in case
        # Thanks to https://stackoverflow.com/a/47616241
        nltk.download('all', quiet=True)
        spinner.stop()
    try:
        e = Explicatio().cmdloop()
    except KeyboardInterrupt:
        print('\nQuitting explicatio')
        sys.exit(0)
