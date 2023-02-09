""" to help a dummy like me play wordle """

import csv

from collections import Counter
from typing import Dict, List

WORDLIST_FILENAME = 'words.txt'
FREQUENCY_FILENAME = 'frequency.csv'
USED_WORDS_LIST_FILENAME = 'used.txt'

def get_frequency(filename: str = FREQUENCY_FILENAME) -> Dict[str, float]:
    """ loads a csv listing letters and their frequency in English into a dict """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return {x[0] : float(x[1]) for x in reader}

def distinct_count(word: str) -> int:
    """ returns the number of unique letters in a word """
    return len(set(word))

def word_score(word: str, frequencies: Dict[str, float]) -> float:
    """ rates each word by adding up how commonly it's used in english """
    return sum([frequencies[x] for x in word])

def load_list_of_words(to_filter: bool) -> List[str]:
    """ loads a list of words and sorts them by number of unique letters and word score """
    freq = get_frequency()
    with open(WORDLIST_FILENAME) as wordsfile:
        list_of_words = [x.strip() for x in wordsfile.readlines()]

    if to_filter:
        with open(USED_WORDS_LIST_FILENAME) as wordsfile:
            used = [x.strip().lower() for x in wordsfile.readlines()]
        list_of_words = [x for x in list_of_words if x not in used]

    return sorted(list_of_words, key=lambda x: (-distinct_count(x), -word_score(x, freq)))

class Wordle:
    """ an object storing possible answers """
    def __init__(self, to_filter: bool=False) -> None:
        """ initializes an instance with fresh word list """
        self.to_filter = to_filter
        self.words = load_list_of_words(to_filter)

    def reset(self) -> None:
        """ refreshes the list of words """
        self.words = load_list_of_words(self.to_filter)

    def report(self) -> None:
        """ prints the number of possible words """
        count = len(self.words)
        print("{} words remaining.".format(count))
        if count < 10:
            print("Try the following:")
            self.guess()

    def include(self, letters: str) -> None:
        """ filter a list of word to include only those that contain the specified letters """
        for letter in letters:
            self.words = [x for x in self.words if letter in x]
        self.report()

    def includesubstring(self, letters: str) -> None:
        """ filters a list of words to include only those that contain the specified substring """
        self.words = [x for x in self.words if letters in x]
        self.report()

    def startswith(self, letters: str) -> None:
        """ filter a list of word to include only those that start with the specified letters """
        self.words = [x for x in self.words if x.startswith(letters)]
        self.report()

    def endswith(self, letters: str) -> None:
        """ filter a list of word to include only those that end with the specified letters """
        self.words = [x for x in self.words if x.endswith(letters)]
        self.report()

    def black(self, letters: str) -> None:
        """ filters a list of words to exclude those that contain the specified letters """
        for letter in letters:
            self.words = [x for x in self.words if letter not in x]
        self.report()

    def green(self, letter: str, position: int) -> None:
        """ filter a list of words to only include those that contain a specific letter at a
        specific position """
        self.words = [x for x in self.words if x[position] == letter]
        self.report()

    def yellow(self, letter: str, position: int) -> None:
        """ filter a list of words to only include those that contain a specific letter at all but
        a specific position """
        self.words = [x for x in self.words if x[position] != letter and letter in x]
        self.report()

    def greenword(self, letters: str) -> None:
        """ filters a list of words to include only those that include the given letters """
        for index, letter in enumerate(letters):
            if letter.isalpha():
                self.green(letter, index)

    def yellowword(self, letters: str) -> None:
        """ filters a list of words to include only those that include the given letters """
        for index, letter in enumerate(letters):
            if letter.isalpha():
                self.yellow(letter, index)

    def guess(self) -> None:
        """
        basically tries to guess the word that will eliminate the maximum possible potential
        letters
        TODO: sometimes this is useless. think through a proper algorithm
        """
        if len(self.words) == 1:
            print(self.words)
            return

        freq = [x[0] for x in Counter("".join(self.words)).most_common()]
        filtered = self.words[:]
        for letter in freq:
            placeholder = [x for x in filtered if letter in x]
            if not placeholder:
                print(filtered)
                break
            filtered = placeholder

    def applyscore(self, word: str, score: str) -> None:
        """
        filters available list based on guess
        param word: a 5-letter word
        param score: a 5-letter string using only the characters 'b', 'g', 'y'
        """
        score = score.lower()

        if len(word) != 5:
            print('Uh, this word is {} letters long.'.format(len(word)))
            return

        if len(score) != 5:
            print('Uh, this score is {} letters long'.format(len(score)))
            return

        if not word.isalpha():
            print('I don\'t understand this word.')
            return

        if not all(x in 'bgy' for x in score):
            print("The score should only use the letters 'b', 'g', or 'y'.")
            return

        for position, letter in enumerate(word):
            if score[position] == 'b':
                self.black(letter)
            elif score[position] == 'g':
                self.green(letter, position)
            elif score[position] == 'y':
                self.yellow(letter, position)

        self.report()

def main() -> None:
    """ a main method """
    print("Don't run me directly.")

if __name__ == '__main__':
    main()
