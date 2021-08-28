import pygame
import sys

from lib.screens import gameScreen, menuScreen
from lib.constants import WIDTH, HEIGHT


def main():
    pygame.init()

    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    current_screen = menuScreen((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        current_screen.draw()
        screen.blit(current_screen, (0, 0))

        # Update the scenes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if isinstance(
                (new_screen := current_screen.handle_event(event, gameScreen)),
                gameScreen,
            ):
                current_screen = new_screen

        pygame.display.update()


if __name__ == "__main__":
    main()
