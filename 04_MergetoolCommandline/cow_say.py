import cowsay
import argparse
import sys
import cmd
import shlex

class CowsayShell(cmd.Cmd):
    prompt = "cow_cmd>> "

    def do_list_cows(self, arg):
        """    List cows names
    USAGE: list_cows [cow_path]"""
        args = shlex.split(arg)
        if len(args) > 1:
            return
        print(' '.join(cowsay.list_cows(*args)))
    
    def do_make_bubble(self, arg):
        """    Print bubble with text
    USAGE: make_bubble text [width [brackets [wrap_text]]]"""
        args = shlex.split(arg)
        if len(args) < 1 or len(args) > 4:
            return
        if len(args) >= 2:
            args[1] = cowsay.THOUGHT_OPTIONS[args[1]]
        if len(args) >= 3:
            args[2] = int(args[2])
        if len(args) == 4:
            args[3] = bool(args[3])
        print(cowsay.make_bubble(*args))

    def complete_make_bubble(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        options = []
        if len(words) == 3:
            options = ['cowsay', 'cowthink']
        elif len(words) == 5:
            options = ['True', 'False']
        return [c for c in options if c.startswith(text)]

    def do_cowsay(self, arg):
        """    Print cow saying message
    USAGE: cowsay message [cow [eyes [tongue]]]"""
        args = shlex.split(arg)
        if len(args) < 1 or len(args) > 4:
            return
        if len(args) >= 3:
            args = args[:2] + [None] + args[2:]
        print(cowsay.cowsay(*args))
    
    def complete_cowsay(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        options = []
        if len(words) == 3:
            options = cowsay.list_cows()
        elif len(words) == 4:
            options = ['..', 'aa', 'vv']
        elif len(words) == 5:
            options = ['w', 'v', 'u']
        return [c for c in options if c.startswith(text)]

    def do_cowthink(self, arg):
        """    Print cow thinking message
    USAGE: cowsay message [cow [eyes [tongue]]]"""
        args = shlex.split(arg)
        if len(args) < 1 or len(args) > 4:
            return
        if len(args) >= 3:
            args = args[:2] + [None] + args[2:]
        print(cowsay.cowthink(*args))
    
    def complete_cowthink(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()
        options = []
        if len(words) == 3:
            options = cowsay.list_cows()
        elif len(words) == 4:
            options = ['..', 'aa', 'vv']
        elif len(words) == 5:
            options = ['w', 'v', 'u']
        return [c for c in options if c.startswith(text)]

if __name__ == "__main__":
    CowsayShell().cmdloop()
