#!/usr/bin/env python

# Built-ins
import cmd
import sys

# Third party modules
import colored
from colored import stylize


class Explicatio(cmd.Cmd):
    intro = stylize(
        'Welcome to the explicatio shell. Type help or ? to list commands.\n',
        colored.fg('green')
    )
    prompt = stylize(
        '[explicatio] ',
        colored.fg('red')
    )
    file = None

    def do_load(self, arg):
        'Load a file for analysis'
        print(f'Loading {arg}')

    def do_quit(self, arg):
        'Quit explicatio'
        print('Thanks for using explicatio!')
        sys.exit(0)


if __name__ == '__main__':
    try:
        e = Explicatio().cmdloop()
    except KeyboardInterrupt:
        print('\nQuitting explicatio')
        sys.exit(0)
