from typing import List, NoReturn

from pyglet import image, media, text


class ScreenResource:
    keyboard: image.AbstractImage = image.load("resources/images/keyboard.png")
    background: image.AbstractImage = image.load(
        "resources/images/background.png"
    )
    blurry_background: image.AbstractImage = image.load(
        "resources/images/blurry_background.png"
    )
    icon_for_application: image.AbstractImage = image.load(
        "resources/images/icon.png"
    )
    background_music: media.Source = media.load(
        "resources/sounds/background_music.mp3"
    )

    all_entered_letters: List[text.Label] = []
    notification: text.Label = None


class Field:
    def __init__(self) -> None:
        self.rounded_square: image.AbstractImage = image.load(
            "resources/images/rounded_square.png"
        )
        self.__rounded_square_green: image.AbstractImage = image.load(
            "resources/images/rounded_square_green.png"
        )
        self.__rounded_square_orange: image.AbstractImage = image.load(
            "resources/images/rounded_square_orange.png"
        )
        self.__rounded_square_gray: image.AbstractImage = image.load(
            "resources/images/rounded_square_gray.png"
        )

    def set_color_field(self, color: str) -> NoReturn:
        if color == "green":
            self.rounded_square = self.__rounded_square_green
        elif color == "orange":
            self.rounded_square = self.__rounded_square_orange
        else:
            self.rounded_square = self.__rounded_square_gray
