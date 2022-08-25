#!/usr/bin/env python

# Built-ins
import cmd
import os
import sys
import tkinter
from tkinter import filedialog as fd

# Third party modules
import colored
from colored import stylize
from halo import Halo

import nltk
from nltk import tokenize, FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import version
VERSION = version.__version__


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
            with open(self.filename) as f:
                self.data = f.read()
                self.word_tokens = nltk.word_tokenize(self.data)
                self.corpus = nltk.Text(self.word_tokens)
            print(f'Loaded {self.filename}')

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

    def do_showcontents(self, arg):
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

    def do_freqdist(self, arg):
        'Get a frequency distribution.'

        freq_dist = FreqDist(self.corpus)
        dist = freq_dist.most_common(int(arg))
        print(f'\nShowing top {arg} words')
        print('Word'.ljust(25) + 'Count')
        for item in dist:
            print(item[0].ljust(25), end='')
            print(str(item[1]).ljust(25))
        print('\n')

    def do_about(self, arg):
        print(f'Version: {VERSION}')

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
            text='Natural language data not found. Downloading to '
                 f'{nltk.data.path[0]}...',
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
