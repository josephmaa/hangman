import pygame

from lib.constants import BLACK, DEFAULT_FONT_SIZE, WHITE, WIDTH, HEIGHT
from lib.inputs import menuWordBox, menuGuessesBox


class menuScreen(pygame.Surface):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(menuScreen, self).__init__(resolution)
        self._resolution = resolution
        self._monospace = pygame.font.SysFont("monospace", DEFAULT_FONT_SIZE)
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
        self.draw_instructions()
        self.draw_menu_box()

    def draw_background(self):
        # Draw the background
        self.fill(BLACK)

    def draw_instructions(self):
        # Calculate the instructions size
        self._instructions_size = self._monospace.size(self._instructions)

        # Render the text instructions
        instructions = self._monospace.render(self._instructions, True, WHITE)
        self.blit(
            instructions,
            (
                WIDTH / 2 - self._instructions_size[0] / 2,
                HEIGHT / 2 - self._instructions_size[1] / 2,
            ),
        )

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
            if isinstance((guess_input := self._menu_box.handle_event(event)),int):
                self._guesses = guess_input
        else:
            return gameScreen(self._resolution, self._text, self._guesses)


class gameScreen(pygame.Surface):
    def __init__(
        self,
        resolution: tuple[float, float] = (1280, 720),
        text: str = "",
        guesses: int = 0,
    ):
        super(gameScreen, self).__init__(resolution)

    def draw(self):
        rect = pygame.rect.Rect((10, 10), (10, 10))
        self.fill(BLACK)
        color = WHITE
        pygame.draw.rect(self, color, rect)

    def handle_event(self, *args, **kwargs):
        pass
