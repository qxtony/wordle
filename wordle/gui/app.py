from typing import Dict, Literal, Optional, Tuple, Union

from pyglet import app, clock, text, window

from config import (
    COUNT_FIELDS,
    ERROR_COLOR,
    FONT_COLOR,
    HEIGHT,
    TITLE,
    WIDTH,
    WIN_OR_LOSS_COLOR,
)
from logic import (
    change_layout,
    check_correct_location,
    check_presence_letter,
    choice_random_word,
    get_cell_coordinates,
    read_words_in_file,
)
from screen_properties import Field, ScreenResource


class Wordle(window.Window):
    def __init__(self) -> None:
        super(Wordle, self).__init__(WIDTH, HEIGHT, TITLE)

        self.resources = ScreenResource
        self.fields = [Field() for _ in range(COUNT_FIELDS)]

        self.set_icon(self.resources.icon_for_application)
        self.resources.background_music.play()

        self.hidden_word: str = choice_random_word()
        self.count_occupied_fields = 0
        self.count_guessed_words = 0
        self.is_enter_active = False
        self.is_draw_notification = False

    def on_draw(self) -> None:
        self.clear()
        self.resources.background.blit(0, 0)
        self.resources.keyboard.blit(25, 50)

        for distance_from_edge, field in enumerate(self.fields):
            field.rounded_square.blit(
                *get_cell_coordinates(150, 575, distance_from_edge)
            )

        for letter in self.resources.all_entered_letters:
            letter.draw()

        if self.resources.notification:
            self.resources.blurry_background.blit(0, 0)
            self.resources.notification.draw()
            self.is_draw_notification = True

    def on_key_press(self, key: int, _: int) -> Optional[bool]:
        converted_letter: Union[str, Literal[False]] = change_layout(key)

        if not converted_letter:
            return False

        if self.is_draw_notification:
            self.clear_error()
            self.is_draw_notification = False

        permission_to_draw: Union[str, bool] = self.get_permission_to_draw(
            converted_letter
        )

        if permission_to_draw == "Backspace":
            if self.count_occupied_fields % 5 == 0:
                if (
                    self.count_occupied_fields // 5
                    != self.count_guessed_words + 1
                ):
                    return False

            self.resources.all_entered_letters.pop()
            self.count_occupied_fields -= 1

        elif permission_to_draw == "Enter":
            suggested_word: str = self.get_word_of_line()
            result: Dict[str, str] = self.get_correct_word(suggested_word)

            if result["status"] == "error":
                self.write_text_on_center_screen(
                    "Слово не найдено.", color=ERROR_COLOR
                )

            elif result["status"] == "win":
                self.write_text_on_center_screen(
                    "Вы выиграли!", color=WIN_OR_LOSS_COLOR
                )
                clock.schedule_once(lambda _: exit(), 3)

        if permission_to_draw is True:
            if self.count_occupied_fields == 25:
                self.write_text_on_center_screen(
                    f"Вы проиграли. Загаданное слово: {self.hidden_word}",
                    color=WIN_OR_LOSS_COLOR,
                    font_size=26,
                )
                clock.schedule_once(lambda _: exit(), 3)

            x, y = get_cell_coordinates(182, 620, self.count_occupied_fields)

            letter: text.Label = text.Label(
                text=converted_letter,
                font_name="Open Sans",
                font_size=45,
                anchor_x="center",
                anchor_y="center",
                color=FONT_COLOR,
                x=x,
                y=y,
            )
            self.resources.all_entered_letters.append(letter)
            self.count_occupied_fields += 1

    def write_text_on_center_screen(
        self,
        message: str, color: Tuple[int, int, int, int],
        font_size: int = 50
    ) -> None:
        self.resources.notification = text.Label(
            text=message,
            font_name="Open Sans",
            font_size=font_size,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
            color=color,
        )

    def get_permission_to_draw(self, key: str) -> Union[str, bool]:
        if key in ["Backspace", "Enter"]:
            return_full_line = [False, True][key == "Enter"]

            if self.is_string_complete(return_full_line=return_full_line):
                self.is_enter_active = True
                return key

        elif self.is_string_complete():
            suggested_word: str = self.get_word_of_line()
            result: Dict[str, str] = self.get_correct_word(suggested_word)

            if result["status"] == "continue" and self.is_enter_active:
                return True
            return key

        elif not self.is_string_complete():
            return True

    def is_string_complete(self, return_full_line: bool = True) -> bool:
        quantity_is_not_zero = self.count_occupied_fields > 0
        is_full_line = self.count_occupied_fields % 5 == 0

        if return_full_line:
            return quantity_is_not_zero and is_full_line

        return quantity_is_not_zero

    def get_word_of_line(self) -> str:
        letters = self.resources.all_entered_letters[
            self.count_occupied_fields - 5: self.count_occupied_fields
        ]
        return "".join([label.text for label in letters])

    def get_correct_word(self, suggested_word: str) -> Dict[str, str]:
        if suggested_word not in read_words_in_file():
            return {"status": "error"}

        elif suggested_word == self.hidden_word:
            return {"status": "win"}

        self.count_guessed_words = len(self.resources.all_entered_letters) // 5

        for count, letter in enumerate(suggested_word):
            if check_correct_location(letter, self.hidden_word, count):
                rgba_color = "green"

            elif check_presence_letter(
                    letter, self.hidden_word, suggested_word, count
            ):
                rgba_color = "orange"

            else:
                rgba_color = "gray"

            self.fields[
                self.count_occupied_fields + count - 5
            ].set_color_field(rgba_color)
            self.on_draw()

        return {"status": "continue"}

    def clear_error(self) -> None:
        self.resources.all_entered_letters = (
            self.resources.all_entered_letters[
                : self.count_occupied_fields - 5
            ]
        )
        self.count_occupied_fields -= 5
        self.resources.notification = None


if __name__ == "__main__":
    window_game = Wordle()
    app.run()
