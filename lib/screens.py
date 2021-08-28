import pygame

from pygame.constants import KEYUP, K_RETURN
from lib.constants import BLACK, WHITE, WIDTH, HEIGHT
from lib.inputs import inputBox


class menuScreen(pygame.Surface):
    def __init__(self, resolution: tuple[float, float] = (WIDTH, HEIGHT)):
        super(menuScreen, self).__init__(resolution)
        self._monospace = pygame.font.SysFont("monospace", 30)
        self._instructions = "Type in a word for hangman below: "
        self._instructions_size = self._monospace.size(self._instructions)
        self._input_box = None

    def draw(self):
        # Draw the background
        self.fill(BLACK)

        # Render the text instructions
        instructions = self._monospace.render(self._instructions, 1, WHITE)
        self.blit(
            instructions,
            (
                WIDTH / 2 - self._instructions_size[0] / 2,
                HEIGHT / 2 - self._instructions_size[1] / 2,
            ),
        )

        # Render the InputBox
        if not self._input_box:
            self._input_box = inputBox(
                x=(WIDTH / 2 - 300), y=(HEIGHT / 2 + 100), width=300, height=200
            )
        else:
            self._input_box.update()
        self._input_box.draw(self)

    def handle_event(self, event, scene):
        if event.type == KEYUP:
            if event.key == K_RETURN:
                return scene()


class gameScreen(pygame.Surface):
    def __init__(self, resolution: tuple[float, float] = (1280, 720)):
        super(gameScreen, self).__init__(resolution)

    def draw(self):
        rect = pygame.rect.Rect((10, 10), (10, 10))
        self.fill(BLACK)
        color = WHITE
        pygame.draw.rect(self, color, rect)

    def handle_event(self, *args, **kwargs):
        pass
