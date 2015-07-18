# encoding=utf-8

from sys import argv
from reslides.rule import Rule, getrules
from reslides.context import FileContext, ApplyContext

import rules

def magic(filename: str, rules: [Rule]) -> None:
    with FileContext(filename, 'r') as fc:
        for line in ApplyContext(fc, rules):
            print(line, end='')

def usage():
    print("Usage: reslides file")

if __name__ == '__main__':
    if len(argv) == 2:
        rules = getrules()
        magic(argv[1], rules)
    else:
        usage()
