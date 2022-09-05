#!/usr/bin/env python

# Built-ins
import cmd
from collections import Counter
import mimetypes
import os
import platform
import sys
import tkinter
from tkinter import filedialog as fd

# Third party modules
import colored
from colored import stylize
from halo import Halo
from matplotlib import pyplot as plt
import nltk
from nltk import tokenize, FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import textract

__version__ = '2022.8'
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
            '''with open(self.filename) as f:
                self.data = f.read()
                self.word_tokens = nltk.word_tokenize(self.data)
                self.corpus = nltk.Text(self.word_tokens)'''
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
        except FileNotFoundError:
            print(
                stylize(
                    f'! {self.filename} was not found',
                    colored.fg('red')
                )
            )
            pass
        except textract.exceptions.MissingFileError:
            pass

    def do_showcontents(self, arg):
        'Show the contents of the file that explicatio is working with.'
        if self.filename is not None:
            print(self.data)
        else:
            print(
                stylize(
                    '[ERROR] Please load a file first.',
                    colored.fg('red')
                )
            )

    def do_sentiment(self, arg):
        'Run a quick sentiment analysis'
        if self.filename is not None:
            sents = tokenize.sent_tokenize(self.data)
            # https://www.nltk.org/howto/sentiment.html
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(sents[2])
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
        else:
            print(
                stylize(
                    '[ERROR] Please load a file first.',
                    colored.fg('red')
                )
            )

    def do_dispersion(self, arg):
        'Do a quick dispersion plot for words'
        args = arg.split(';')

        self.corpus.dispersion_plot(args)

    def do_concordance(self, arg):
        'Run a quick concordance with the argument as the keyword'
        args = arg.split()
        self.corpus.concordance(args[0], lines=args[1])

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

    def do_nerec(self, arg):
        'Named entity recognition tree building'
        # Broken for now.

        pos = nltk.pos_tag(self.word_tokens)
        tree = nltk.ne_chunk(pos)
        tree.draw()

    def do_about(self, arg):
        'About explicatio'
        print(f'Version: {__version__}')
        print(f'  NLTK: {NLTK_VERSION}')
        print(f'  Python: {PY_VERSION}')

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
