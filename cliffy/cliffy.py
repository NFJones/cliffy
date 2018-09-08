#!/usr/bin/env python3

from __future__ import print_function
import future
import builtins
import past
import six
from builtins import input

from colorama import Fore
from colorama import Style
from threading import RLock
from threading import Thread
import argcomplete
import argparse
import os
import readline
import shlex
import subprocess
import sys
import time


class Cliffy(object):
    def __init__(self, cli, historyFile=None, historyLimit=4096):
        self._cli = cli
        self._homedir = os.path.expanduser('~')
        self._historyFile = historyFile if historyFile else '{}/.cli-{}.history'.format(
            self._homedir, '_'.join(self._cli))
        self._historyLimit = historyLimit
        self._lock = RLock()
        self._running = False
        self._thread = None
        self._code = 0

    def start(self):
        self._init_history()

        readline.parse_and_bind("tab: complete")

        with self._lock:
            self._running = True
            self._thread = Thread(target=self._run)
            self._thread.start()

    def stop(self):
        with self._lock:
            self._running = False
        if self._thread:
            try:
                self._thread.join()
            except:
                pass

    def running(self):
        with self._lock:
            return self._running

    def _init_history(self):
        readline.set_history_length(self._historyLimit)
        try:
            with open(self._historyFile, 'a'):
                pass
            readline.read_history_file(self._historyFile)
        except:
            print('Could not open history file: {}'.format(self._historyFile))

    def _run(self):
        try:
            while self.running():
                with self._lock:
                    if self._code:
                        codeColor = Fore.RED
                    else:
                        codeColor = Fore.GREEN

                    cliJoined = ' '.join(self._cli)
                    codePart = '{}{}{}'.format(
                        codeColor, self._code, Style.RESET_ALL)
                    cliPart = '{}{}{}'.format(
                        Fore.LIGHTCYAN_EX, cliJoined, Style.RESET_ALL)

                    line = input('[{}] ({}) > '.format(codePart, cliPart))
                    if readline.get_history_length() == 0:
                        readline.add_history(line)
                    elif line != readline.get_history_item(readline.get_current_history_length()):
                        readline.add_history(line)

                    self._execute(shlex.split(line))
        except EOFError:
            self.stop()
            try:
                readline.write_history_file(self._historyFile)
            except:
                print()
                print('Could not save history file: {}'.format(
                    self._historyFile))

    def _execute(self, argv):
        argv = self._cli + argv
        try:
            self._code = subprocess.call(argv)
        except Exception as e:
            print(str(e))
            self._code = 255
        except KeyboardInterrupt:
            self._code = 130


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'cli', help='The command around which the CLI should be wrapped.', nargs='+')
        parser.add_argument('-f', '--history-file', dest='historyFile',
                            default=None, help='The history file to use.')
        parser.add_argument('-l', '--history-limit', dest='historyLimit', default=4096, type=int,
                            help='The maximum number of history entries to retain in the history file.')
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        cli = Cliffy(args.cli, historyFile=args.historyFile,
                     historyLimit=args.historyLimit)
        cli.start()
        while cli.running():
            time.sleep(0.1)
        print()
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        sys.exit(1)
