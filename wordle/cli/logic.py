from random import choice
from typing import List


def read_words_infile() -> List[str]:
    with open("../ru_words.txt", "r") as file:
        words: List[str] = file.read().splitlines()

    return words


def choice_random_word() -> str:
    return choice(read_words_infile())


def checking_for_correctness(word: str) -> str:

    if not word.isalpha():
        return "Слово должно состоять из букв"

    elif len(word) != 5:
        return "Слово должно состоять из 5 букв"

    elif word not in read_words_infile():
        return "Слово не найдено в списке слов"


def check_location(letter: str, word: str, position: int) -> bool:
    return letter == word[position]


def check_letter(letter: str, word: str, player_word: str, position: int) -> bool:
    if player_word.count(letter) > 1 and position == player_word.index(letter):
        return False

    return letter in word
