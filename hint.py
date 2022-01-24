#!/usr/bin/env python3
from collections import Counter
import itertools
import functools
import argparse


def load_six_letter_words():
    with open('/usr/share/dict/words', 'r') as src:
        words = src.readlines()
    return set(w.lower().strip() for w in words if len(w) == 6)


def count_unique_letter_frequencies(words):
    return Counter(letter for word in words for letter in set(word))


class Dictionary:

    def __init__(self):
        words = load_six_letter_words()
        self.frequencies = count_unique_letter_frequencies(words)
        self.ordered_words = self.order_words_by_unique_letter_frequency(words)

    def order_words_by_unique_letter_frequency(self, words):
        return sorted(words, key=self.word_weight, reverse=True)

    def word_weight(self, word):
        return sum(self.frequencies[letter] for letter in set(word.lower().strip()))


def parse_args():
    parser = argparse.ArgumentParser(description='Suggest next guesses..')
    parser.add_argument('guesses', metavar='G', type=str, nargs='*',
                        help='Guess/result pairs: '
                        '"train/..xXx" means "a" and "n" are present but in different spot, "i" is in correct location')
    return parser.parse_args()


def next_best(guesses):
    d = Dictionary()
    if not guesses:
        print(f"{len(d.ordered_words)} six letter words loaded.. Best starting words:")
    return apply_constraints(d, guesses)


def apply_constraints(dictionary, guesses):
    constraints = tuple(create_constraints(guesses))
    return (word for word in dictionary.ordered_words if all(match(word) for match in constraints))


def create_constraints(guesses):
    for guess_and_result in guesses:
        guess, result = guess_and_result.split('/')
        assert len(guess) == len(result) == 5, 'guess and result must be 5 long'
        guess = guess.lower()
        for position, (letter, result) in enumerate(zip(guess, result)):
            if result == '.':
                yield functools.partial(no_match, position, letter)
            elif result == 'X':
                yield functools.partial(exact_match, position, letter)
            elif result == 'x':
                yield functools.partial(inexact_match, position, letter)
            else:
                raise ValueError(f"Invalid result '#{result}': must be one of '.xX'")


def no_match(position, letter, candidate):
    return letter not in candidate


def exact_match(position, letter, candidate):
    return candidate[position] == letter


def inexact_match(position, letter, candidate):
    return letter in candidate and candidate[position] != letter


if __name__ == '__main__':
    args = parse_args()
    candidates = next_best(args.guesses)
    print(', '.join(itertools.islice(candidates, 10)))
