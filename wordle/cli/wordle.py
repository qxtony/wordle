from colors import Color, color_print
from logic import (
    check_letter,
    check_location,
    checking_for_correctness,
    choice_random_word,
)


def start_game() -> None:
    word: str = choice_random_word()
    count_entered_words = 0

    while count_entered_words < 5:
        player_word: str = input()
        answer = checking_for_correctness(player_word)

        if answer:
            print(answer)
            continue

        for index, letter in enumerate(player_word):
            if player_word == word:
                print(
                    f"ПОЗДРАВЛЯЮ! Вы угадали слово с {count_entered_words + 1}/6 попытки!"
                )
                exit(0)

            if check_location(letter, word, index):
                color_print(letter, Color.GREEN)

            elif check_letter(letter, word, player_word, index):
                color_print(letter, Color.YELLOW)

            else:
                color_print(letter, Color.GRAY)

        count_entered_words += 1
        print()

    print(f"Вы проиграли. Загаданное слово: {word}")


if __name__ == "__main__":
    start_game()
