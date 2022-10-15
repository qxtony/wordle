from random import choice
from typing import Dict, List, Literal, Tuple, Union

from config import COUNT_OF_FIELDS_LINE


def read_words_in_file() -> List[str]:
    with open("../ru_words.txt", "r") as file:
        words: List[str] = file.read().splitlines()

    return words


def choice_random_word() -> str:
    return choice(read_words_in_file())


def check_correct_location(letter: str, word: str, position: int) -> bool:
    return letter == word[position]


def check_presence_letter(
    letter: str, word: str, player_word: str, position: int
) -> bool:
    if player_word.count(letter) > 1 and position == player_word.index(letter):
        return False

    return letter in word


def change_layout(key: int) -> Union[str, Literal[False]]:
    letters: Dict[int, str] = {
        113: "й", 119: "ц",
        101: "у", 114: "к",
        116: "е", 121: "н",
        117: "г", 105: "ш",
        111: "щ", 112: "з",
        91: "х", 93: "ъ",
        97: "ф", 115: "ы",
        100: "в", 102: "а",
        103: "п", 104: "р",
        106: "о", 107: "л",
        108: "д", 59: "ж",
        39: "э", 122: "я",
        120: "ч", 99: "с",
        118: "м", 98: "и",
        110: "т", 109: "ь",
        44: "б", 46: "ю",
        96: "ё",
    }
    codes: Dict[int, str] = {65293: "Enter", 65288: "Backspace"}

    if key in codes.keys():
        return codes[key]

    elif key not in letters.keys():
        return False

    return letters[key]


def get_cell_coordinates(
    indent_by_x: int,
    indent_by_y: int,
    distance_from_edge: int,
    indent_from_beginning: int = 75,
) -> Tuple[int, int]:

    x = (
        indent_by_x
        + (distance_from_edge % COUNT_OF_FIELDS_LINE) * indent_from_beginning
    )
    y = (
        indent_by_y
        - (distance_from_edge // COUNT_OF_FIELDS_LINE) * indent_from_beginning
    )

    return x, y
