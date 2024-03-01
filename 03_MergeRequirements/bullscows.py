from random import choice
import argparse
import os
import urllib.request
import cowsay

def ask(prompt: str, valid: list[str] = None):
    print(cowsay.cowsay(prompt, cow=cowsay.get_random_cow()))
    guess = str(input())
    if valid is not None:
        while guess not in valid:
            print(cowsay.cowsay(prompt, cow=cowsay.get_random_cow()))
            guess = str(input())
    return guess

def inform(format_string: str, bulls: int, cows: int):
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=cowsay.get_random_cow()))

def bullscows(guess: str, secret: str):
    bulls = 0
    for c1, c2 in zip(guess, secret):
        if c1 == c2:
            bulls += 1
    cows = 0
    for c in guess:
        if c in secret:
            cows += 1
            secret = secret.replace(c, '', 1)
    return (bulls, cows)

def gameplay(ask: callable, inform: callable, words: list[str]):
    secret = choice(words)
    guess = ''
    attempts = 0
    while guess != secret:
        guess = ask("Введите слово: ", words)
        attempts += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
    print(attempts)

parser = argparse.ArgumentParser()
parser.add_argument('wordlist', type=str)
parser.add_argument('length', nargs='?', default=5, type=int)
args = parser.parse_args()

wordlist = args.wordlist
words = []
if os.path.exists(wordlist):
    with open(wordlist, "r") as f:
        words = f.read().split()
else:
    words = [word.decode("utf-8").strip() for word in urllib.request.urlopen(wordlist).readlines()]

length = args.length
words = [word for word in filter(lambda w : len(w) == length, words)]

gameplay(ask, inform, words)
