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

import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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

    def do_load(self, arg):
        'Load a file for analysis'
        print(f'Loading {arg}...')
        # https://bytes.com/topic/python/answers/19510-tkfiledialog-without-parent-window
        root = tkinter.Tk()
        root.withdraw()
        # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
        self.filename = fd.askopenfilename()
        root.destroy()
        with open(self.filename) as f:
            self.data = f.read()
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
        print(args)
        corpus = nltk.Text(self.data)
        corpus.dispersion_plot(args)

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
        print(
            stylize(
                '[ERROR] NLTK is not installed. This needs to be installed so'
                ' please wait while NLTK\'s data is downloaded...',
                colored.fg('red')
            )
        )
        # Download all NLTK data just in case
        # Thanks to https://stackoverflow.com/a/47616241
        nltk.download('all', quiet=True)
    try:
        e = Explicatio().cmdloop()
    except KeyboardInterrupt:
        print('\nQuitting explicatio')
        sys.exit(0)
