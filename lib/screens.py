from abc import abstractmethod
import pygame
from pygame.constants import K_RETURN

from lib.constants import ALPHABET, BLACK, DEFAULT_FONT_SIZE, RED, WHITE, WIDTH, HEIGHT
from lib.inputs import menuWordBox, menuGuessesBox


class genericScreen(pygame.Surface):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(genericScreen, self).__init__(resolution)
        self._instructions = ""
        self._resolution = resolution
        self._monospace = pygame.font.SysFont("monospace", DEFAULT_FONT_SIZE)

    @abstractmethod
    def draw(self):
        return

    def draw_background(self):
        # Draw the background
        self.fill(BLACK)

    def draw_text(
        self,
        text: str = "",
        width: int = WIDTH / 2,
        height: int = HEIGHT / 2,
        color: pygame.Color = WHITE,
    ) -> None:
        text_size = self._monospace.size(text)
        text = self._monospace.render(text, True, color)
        self.blit(
            text,
            (
                width - text_size[0] / 2,
                height - text_size[1] / 2,
            ),
        )

    def draw_warning(
        self,
        text: str = "",
        width: int = WIDTH / 2,
        height: int = HEIGHT / 2,
        color: pygame.Color = RED,
    ) -> None:
        return self.draw_text(text=text, width=width, height=height, color=color)


class menuScreen(genericScreen):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(menuScreen, self).__init__(resolution)
        self._instructions = (
            "Type in a word for hangman below and press enter when ready: "
        )
        self._text = ""
        self._menu_box = menuWordBox(
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
        if not self._text:
            if isinstance((text_input := self._menu_box.handle_event(event)), str):
                self._text = text_input
                self._menu_box = menuGuessesBox(
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
            return gameScreen(self._resolution, self._text, self._guesses)


class gameScreen(genericScreen):
    def __init__(
        self,
        resolution: tuple[float, float] = (1280, 720),
        text: str = "",
        guesses: int = 0,
    ):
        super(gameScreen, self).__init__(resolution)
        self._win = False
        self._lost = False
        self._text = text
        self._shown = str("-" * len(text))
        self._remaining_guesses = guesses
        self._instructions = "Press any character to start guessing."
        self._seen = set()
        self._warning = ""

    def draw(self):
        self.draw_background()

        if self._win:
            self.draw_text(text="You win! Press enter to play again")
        elif self._lost:
            self.draw_text(text="You lost! Press enter to play again", color=RED)
        else:
            if self._warning:
                self.draw_warning(
                    text=self._warning,
                    width=WIDTH / 2,
                    height=7 * HEIGHT / 8,
                )

            self.draw_text(text=self._instructions, width=WIDTH / 2, height=HEIGHT / 4)
            self.draw_text(text=self._shown, width=WIDTH / 2, height=HEIGHT / 2)
            self.draw_text(
                text=f"Number of remaining guesses: {self._remaining_guesses}",
                width=WIDTH / 2,
                height=3 * HEIGHT / 4,
            )

    def handle_event(self, event, *args, **kwargs):
        if event.type == pygame.KEYDOWN:
            # Reset the warnings if there are any
            self._warning = ""

            if self._win or self._lost and event == K_RETURN:
                return menuScreen(self._resolution)
            else:
                unicode_character = event.unicode
                if unicode_character in self._seen:
                    self._warning = "Character has already been used"
                elif unicode_character not in ALPHABET:
                    self._warning = "Character not in alphabet"
                else:
                    self._remaining_guesses -= 1
                    self._seen.add(unicode_character)

                    if unicode_character in self._text:
                        self._shown = "".join(
                            [
                                c
                                if self._shown[i] != "-" or c == unicode_character
                                else "-"
                                for i, c in enumerate(self._text)
                            ]
                        )
                    # Re-render the text.
                    self.txt_surface = self._monospace.render(self._shown, True, WHITE)

        # If at any point, there are no more "-" in shown characters, the player has won
        if "-" not in self._shown:
            self._win = True
        elif self._remaining_guesses == 0:
            self._lost = True
