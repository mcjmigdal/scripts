#!/usr/bin/env python2
# Interactively ask user to rename files listed in txt file
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

files = [ line.strip() for line in os.listdir(argv[1]) ]
for file in files:
    if os.path.exists(file):
        prompt = "mv {} ".format(file)
        new_name = rlinput(prompt, file)
        while os.path.exists(new_name) and new_name != file:
            print file, "already exists choose different name."
            prompt = "mv {} ".format(file)
            new_name = rlinput(prompt, file)
        os.rename(file, new_name)
    else:
        print file, "does not exist skiping."

