#!/usr/bin/env python

import cmd
import sys
import tkinter
from tkinter import filedialog as fd

import colored
from colored import stylize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Explicatio(cmd.Cmd):
    intro = stylize(
        'Welcome to the explicatio shell. Type help or ? to list commands.\n',
        colored.fg('green')
    )
    prompt = stylize(
        '[explicatio] ',
        colored.fg('red')
    )
    filename = None

    def do_load(self, arg):
        'Load a file for analysis'
        print(f'Loading {arg}...')
        # https://bytes.com/topic/python/answers/19510-tkfiledialog-without-parent-window
        root = tkinter.Tk()
        root.withdraw()
        # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
        self.filename = fd.askopenfilename()
        root.destroy()
        print(self.filename)

    def do_sentiment(self, arg):
        'Run a quick sentiment analysis'
        sents = [
            'Hello, my name is Bryan.',
            'Everything is great!',
            'The world is a vampire and it sucks bad.'
        ]
        # https://www.nltk.org/howto/sentiment.html
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(sents[2])
        print(
            '[Sentiment Scores (Vader)]\n',
            stylize(f'Negative: {scores["neg"]}\n', colored.fg('red')),
            stylize(f'Positive: {scores["pos"]}\n', colored.fg('green')),
            stylize(f'Neutral: {scores["neu"]}\n', colored.fg('yellow')),
            stylize(f'Compound: {scores["compound"]}\n', colored.fg('blue')),
            )

    def do_quit(self, arg):
        'Quit explicatio'
        print('Thanks for using explicatio!')
        sys.exit(0)

    def do_exit(self, arg):
        'Exit explicatio'
        print('Thanks for using explicatio!')
        sys.exit(0)


if __name__ == '__main__':
    try:
        e = Explicatio().cmdloop()
    except KeyboardInterrupt:
        print('\nQuitting explicatio')
        sys.exit(0)
