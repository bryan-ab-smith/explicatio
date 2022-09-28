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
import textract

__version__ = '2022.9'
NLTK_VERSION = nltk.__version__
PY_VERSION = platform.python_version()

# A lot of the following was supported by the following:
#   - https://realpython.com/nltk-nlp-python/


class Explicatio(cmd.Cmd):
    intro = stylize(
        'Welcome to the explicatio shell. Type help or ? to list commands.\n',
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
        'Load a file for analysis'
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
            self.corpus = nltk.Text(self.word_tokens)
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
            print(
                stylize(
                    f'  Unique Words: {unique_words_text:,}',
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
        'Show the contents of the file that explicatio is working with.'
        if self.filename is not None:
            print(self.data)
        else:
            self.reportError('Please load a file first.')

    def do_sentiment(self, arg):
        'Run a quick sentiment analysis'
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
        'Do a quick dispersion plot for words'
        args = arg.split(';')

        self.corpus.dispersion_plot(args)

    def do_concordance(self, arg):
        'Run a quick concordance with the argument as the keyword'
        args = arg.split()
        try:
            self.corpus.concordance(args[0], width=80, lines=int(args[1]))
        except AttributeError:
            self.reportError('Please load a file first.')
        except IndexError:
            self.reportError('An argument is missing. Plese try again.')

    def do_collocations(self, arg):
        'Find collocations in the text'
        self.corpus.collocations()

    def do_freqdist(self, arg):
        'Get a frequency distribution.'

        freq_dist = FreqDist(self.corpus)
        try:
            dist = freq_dist.most_common(int(arg))
            print(f'\nShowing top {arg} words')
            print('Word'.ljust(25) + 'Count')
            for item in dist:
                print(item[0].ljust(25), end='')
                print(str(item[1]).ljust(25))
            print('\n')
        except ValueError:
            print(
                stylize(
                    'An error occurred. Please make sure to provide '
                    'a number.\n',
                    colored.fg('red')
                )
            )

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
        'Summarise a text'

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
        Ask a question of the corpus
        Argument:
            the question itself
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
        nltk.download('popular', quiet=True)
        spinner.stop()
    try:
        e = Explicatio().cmdloop()
    except KeyboardInterrupt:
        print('\nQuitting explicatio')
        sys.exit(0)
