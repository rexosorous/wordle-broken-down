# standard python modules
from os import system

# local modules
import WordleBase

# dependencies
import colorama

# imports for proper documentation
from typing import List



class WordleConsole(WordleBase.WordleBase):
    ''' Proper implementation of the wordle game for use in the console
    '''
    def __init__(self):
        super().__init__()



    def start(self):
        ''' Starts the game and then continues to play multiple games if the player wants to.
        '''
        while True:
            system('cls')
            self.play()
            cont = input('another game? ')
            if cont != 'y':
                break



    def play(self):
        ''' The main logic for each game

        1. chooses the master word to find
        2. allows the player to make up to 6 guesses
        3. shows the results after each guess
        4. displays a win or loss message after the game is over
        '''
        master = self.choose_master_word()
        history = dict()
        won = False
        guess_count = 0

        while guess_count < 6 and not won:
            guess_count += 1
            guess = self.make_guess(guess_count)
            result = self.check_guess(master, guess)
            won = self.check_win(result)
            history[guess_count] = {'word': guess, 'result': result, 'print': self.prettify_result(guess, result)}
            system('cls')
            for line, value in history.items():
                print(f'Guess #{line}: {value["print"]}')

        if won:
            print(f'WIN on guess #{guess_count}')
        else:
            print(f'LOSE. Correct word was {master}')



    def make_guess(self, guess_count: int):
        ''' Continues to ask user for a guess until they input a valid word/guess.

        Args:
            guess_count (int): used just to print what guess the user is making
        '''
        while True:
            guess = input(f'Guess #{guess_count}: ')
            if self.is_valid_word(guess):
                return guess.upper()
            else:
                print('Invalid word. Try again.')



    def prettify_result(self, guess: str, result: List[WordleBase.GuessResults]) -> str:
        ''' Colors the text after each guess.

        RED for incorrect letter
        YELLOW for correct letter wrong place
        GREEN for correct letter correct place

        Args:
            guess (str)
            result (List[WordleBase.GuessResults]): should be obtained from WordleBase.WordleBase.check_guess()

        Returns:
            str: the prettified/colored string to be printed.
        '''
        result_colors = {
            WordleBase.GuessResults.INCORRECT: colorama.Fore.RED,
            WordleBase.GuessResults.PARTIAL: colorama.Fore.YELLOW,
            WordleBase.GuessResults.CORRECT: colorama.Fore.GREEN
        }

        line = ''
        for letter, res in zip(guess, result):
            line += f'{result_colors[res]}{letter}'
        line += colorama.Style.RESET_ALL
        return line


if __name__ == '__main__':
    ''' Run the game
    '''
    game = WordleConsole()
    game.start()