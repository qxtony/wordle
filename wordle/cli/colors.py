from enum import Enum

from rich.console import Console

console = Console()


class Color(Enum):
    YELLOW = "#F9ED69"
    GREEN = "#30E3CA"
    GRAY = "#323232"


def color_print(word: str, color: Color) -> None:
    console.print(word, style=f"{color.value} bold", end="")
