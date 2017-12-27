#!/usr/bin/python

import readline

def main(text, state):
    addrs = ['list', 'create', 'delete', 'quit', 'exit', 'bye']
    options = [x for x in addrs if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(main)
readline.parse_and_bind("tab: complete")

while 1:
    a = raw_input("[yacc]\n$ ")
    if a in ['quit', 'exit', 'bye']:
        break
    print "You entered", a
    print
