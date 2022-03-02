# standard python modules
from enum import Enum
import json
import random

# imports for proper documentation
from typing import List



'''
official_dictionary.json is the official allowed words and answers as obtained from the official website (https://www.nytimes.com/games/wordle/index.html) on March 01, 2022 by viewing the main.bfba912f.js file under Sources
larger_dictioanry.json is a list of all english words obtained from https://github.com/dwyl/english-words (specifically words_dictionary.json), but reformatted to suit this program's needs
'''



class GuessResults(Enum):
        ''' Enum used for the results of each player's guess
        '''
        INCORRECT = 0   # black
        PARTIAL = 1     # orange
        CORRECT = 2     # green



class WordleBase:
    ''' Base class for the wordle game

    Contains the skeleton and basic functions in order to play the game, but no logic to actually
    go through the loop and steps of playing

    Also leaves things fairly generic. For example, this isn't hard-coded for 5 letter words.

    Args:
        dictionary_filename (str): which dictionary to use. see above for details.
        word_length (int)
    '''
    def __init__(self, dictionary_filename: str = 'official_dictionary.json',  word_length: int = 5):
        with open(dictionary_filename, 'r') as file:
            self.dictionary = json.load(file)
        self.dictionary['answers'] = [word for word in self.dictionary['answers'] if len(word) == word_length]
        self.dictionary['allowed'] = [word for word in self.dictionary['allowed'] if len(word) == word_length]



    def choose_master_word(self) -> str:
        ''' Selects the word that needs to be guessed.
        Only chooses from a select list of possible answers.

        Returns:
            str
        '''
        return random.choice(self.dictionary['answers']).upper()



    def is_valid_word(self, word: str) -> bool:
        ''' Checks if a word is valid to be guessed.

        Returns:
            bool:
        '''
        if word in self.dictionary['answers'] or word in self.dictionary['allowed']:
            return True
        return False



    def check_guess(self, master: str, guess: str) -> List[GuessResults]:
        ''' Shows the results of a player's guess, showing:
            - which letters are not in the word (black)
            - which letters are in the word but not in the right position (orange)
            - which letters are in the word and in the right position (green)

        There is an interesting problem with words with duplicate letters.
        If you were to iterate through the guess letters in order, you may run into this problem
            master: HELLO
            guess:  LULLS
            result: 10220
            wherein the first L is shown to be orange even though it shouldn't
        To remedy this, we first tabulate the guess word so that we know which letters show up multiple times,
        and then we do two passes of checks: the first to check which letters are green and the second to check
        which are orange. See below for more a more detailed explanation.

        Args:
            master (str): the word that the player is trying to guess
            geuss (str): the player's guess

        Returns:
            List[GuessResults]
        '''
        result = [GuessResults.INCORRECT] * len(master) # default result to black
        master = list(master) # makes it easier to work with

        # turn the guess word into a dictionary with keys being the letters and values being the positions that
        # letter appears in. useful for knowing how many times that letter appears and where they are.
        guess_tabulated = dict()
        for position, letter in enumerate(guess):
            if letter not in guess_tabulated:
                guess_tabulated[letter] = [position]
            else:
                guess_tabulated[letter].append(position)

        for letter, positions in guess_tabulated.items():
            for pos in positions[:]:
                # first pass: checks which letters are green and then removes them from both the guess and master words
                # we need this to happen first because we need to prioritize green letters over orange ones
                if letter == master[pos]:
                    result[pos] = GuessResults.CORRECT
                    positions.remove(pos)
                    master[pos] = 0     # we're essentially deleting this letter from the master word without messing with the indexes
            for pos in positions:
                # second pass: check which letters are orange.
                # this can only be done now because the first pass eats/removes those letters to remove false positives
                # while iterating through the letters here, it is important to remove as you go from the master word to avoid false positives
                if letter in master:
                    result[pos] = GuessResults.PARTIAL
                    master[master.index(letter)] = 0
            # default for results is INCORRECT so we don't need to do "if letter not in master"

        return result



    def check_win(self, result: List[GuessResults]) -> bool:
        ''' Checks if the result of a guess is a winning combination.

        Returns:
            bool
        '''
        if GuessResults.INCORRECT in result or GuessResults.PARTIAL in result:
            return False
        return True