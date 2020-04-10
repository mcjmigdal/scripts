#!/usr/bin/env python2
import os
import readline
from sys import argv

def rlinput(prompt, prefill=''):
   'https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533134'
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

files = [ line.strip() for line in open(argv[1]).readlines() ]
for file in files:
    prompt = "mv {} ".format(file)
    new_name = rlinput(prompt, file)
    os.rename(file, new_name)

