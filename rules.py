# encoding=utf-8

from reslides.rule import *

@rule
@remove
def background(a, b):
    return a.startswith('@') and b.startswith('@')

@rule
@replace
def color(a: str):
    return a.replace('color', 'style')