from abc import abstractmethod
import pygame
import random

from typing import Optional
from lib.constants import (
    ALPHABET,
    BLACK,
    DEFAULT_FONT_SIZE,
    DEFAULT_SMALL_FONT_SIZE,
    RED,
    WHITE,
    WIDTH,
    HEIGHT,
    LINE_SPACING,
    PATH_TO_DICTIONARY,
)
from lib.inputs import menuLengthBox, menuGuessBox
from lib.parser import parse_dictionary
from lib.strategy import generate_word_families, pick_largest_word_family


class genericScreen(pygame.Surface):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(genericScreen, self).__init__(resolution)
        self._instructions = ""
        self._resolution = resolution
        self._monospace_small = pygame.font.SysFont(
            "monospace", DEFAULT_SMALL_FONT_SIZE
        )
        self._monospace_large = pygame.font.SysFont("monospace", DEFAULT_FONT_SIZE)

    @abstractmethod
    def draw(self):
        return

    def draw_background(self):
        # Draw the background
        self.fill(BLACK)

    def draw_text(
        self,
        text: str = "",
        color: pygame.Color = WHITE,
        x: int = WIDTH / 2 - 300,
        y: int = HEIGHT / 2 - 100,
        width: int = 600,
        height: int = 200,
        font: Optional[pygame.font.SysFont] = None,
    ) -> None:
        bounding_box = pygame.rect.Rect(x, y, width, height)
        y = bounding_box.top
        if not font:
            font = self._monospace_large
        font_height = font.size(text)[1]

        while text:
            i = 1
            if y + font_height > bounding_box.bottom:
                break
            while font.size(text[:i])[0] < bounding_box.width and i < len(text):
                i += 1
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            image = font.render(text[:i], True, color)
            self.blit(image, (bounding_box.left, y))
            y += font_height + LINE_SPACING
            text = text[i:]

    def draw_warning(
        self,
        text: str = "",
        x: int = WIDTH / 2 - 300,
        y: int = HEIGHT / 2 - 100,
        width: int = 600,
        height: int = 200,
        color: pygame.Color = RED,
    ) -> None:
        return self.draw_text(
            text=text, x=x, y=y, width=width, height=height, color=color
        )


class menuScreen(genericScreen):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(menuScreen, self).__init__(resolution)
        self._instructions = (
            "Type in the length of the word and press enter when ready: "
        )
        self._length_input = 0
        self._menu_box = menuLengthBox(
            x=(WIDTH / 2 - 300), y=(HEIGHT / 2 + 100), width=300, height=200
        )
        self._guesses = None

    def draw(self):
        self.draw_background()
        self.draw_text(text=self._instructions)
        self.draw_menu_box()

    def draw_menu_box(self):
        self._menu_box.update()
        self._menu_box.draw(self)

    def handle_event(self, event):
        # Handle the child input box event
        if not self._length_input:
            if isinstance((length_input := self._menu_box.handle_event(event)), int):
                self._length_input = length_input
                self._menu_box = menuGuessBox(
                    x=(WIDTH / 2 - 300),
                    y=(HEIGHT / 2 + 100),
                    width=300,
                    height=200,
                )
                self._instructions = (
                    "Type in the number of guesses and press enter when ready: "
                )
        elif not self._guesses:
            if isinstance((guess_input := self._menu_box.handle_event(event)), int):
                self._guesses = guess_input
        else:
            return gameScreen(self._resolution, self._length_input, self._guesses)


class gameScreen(genericScreen):
    def __init__(
        self,
        resolution: tuple[float, float] = (1280, 720),
        length_input: int = 0,
        guesses: int = 0,
    ):
        super(gameScreen, self).__init__(resolution)
        self._win = False
        self._lost = False
        self._word_families = parse_dictionary(PATH_TO_DICTIONARY)[length_input]
        print(self._word_families)
        self._shown = str("-" * length_input)
        self._remaining_guesses = guesses
        self._instructions = "Press any character to start guessing."
        self._seen = set()
        self._warning = ""
        # Set this randomly for the loss text
        self._text = ""

    def draw(self):
        self.draw_background()

        if self._win:
            self.draw_text(
                text=f"You win, the word was {self._shown}! Press enter to play again"
            )
        elif self._lost:
            self.draw_text(
                text=f"You lost, the word was {self._text}! Press enter to play again",
                color=RED,
            )
        else:
            if self._warning:
                self.draw_warning(
                    text=self._warning,
                    y=5 * HEIGHT / 8,
                )

            self.draw_text(
                text=f"The character's you've seen so far: {sorted(list(self._seen))}",
                y=HEIGHT / 8,
                font=self._monospace_small,
            )
            self.draw_text(
                text=self._instructions,
                y=HEIGHT / 4,
            )
            self.draw_text(text=self._shown)
            self.draw_text(
                text=f"Number of remaining guesses: {self._remaining_guesses}",
                y=3 * HEIGHT / 4,
            )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Reset the warnings if there are any
            self._warning = ""
            if (self._win or self._lost) and event.key == pygame.K_RETURN:
                return menuScreen(self._resolution)
            elif self._win or self._lost:
                pass
            else:
                unicode_character = event.unicode
                if unicode_character in self._seen:
                    self._warning = (
                        f"Character {unicode_character} has already been used"
                    )
                elif unicode_character not in ALPHABET:
                    self._warning = f"Character {unicode_character} not in alphabet"
                else:
                    self._seen.add(unicode_character)

                    word_families = generate_word_families(
                        character=unicode_character,
                        words=self._word_families,
                        existing_characters=self._shown,
                    )

                    new_shown, new_word_family = pick_largest_word_family(word_families)

                    self._shown = new_shown
                    self._word_families = new_word_family

                    # If no appeared change has been made, reduce the counter
                    if new_shown == self._shown:
                        self._remaining_guesses -= 1

                    # Re-render the text.
                    self.txt_surface = self._monospace_large.render(
                        self._shown, True, WHITE
                    )

        # If at any point, there are no more "-" in shown characters, the player has won
        if len(self._word_families) == 0:
            self._win = True
        elif self._remaining_guesses == 0:
            self._lost = True
            self._text = random.choice(self._word_families)
