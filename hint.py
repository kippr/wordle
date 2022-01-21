#!/usr/bin/env python3
from collections import Counter


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


d = Dictionary()
print(f"{len(d.ordered_words)} six letter words loaded")
print(d.ordered_words[:100])
print(f"train is {d.ordered_words.index('train') + 1}th word in list")
