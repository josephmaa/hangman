import pygame

from lib.constants import COLOR_ACTIVE, COLOR_INACTIVE, RED, DEFAULT_FONT_SIZE
from lib.logic import is_valid_guess, is_valid_word_in_dictionary
from lib.parser import parse_dictionary


class inputBox:
    def __init__(self, x: int, y: int, width: int, height: int, text: str = ""):
        self.text_bounding_box = pygame.Rect(x, y, width, height)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.SysFont("monospace", DEFAULT_FONT_SIZE)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self._prompt_for_input = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the input_box, toggle the active variable
            if self.text_bounding_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = COLOR_ACTIVE
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def prompt_for_valid_input(self):
        self._prompt_for_input = True
        self.text = ""

    def update(self):
        # Resize the box if the text is too long.
        width = max(600, self.txt_surface.get_width() + 10)
        self.text_bounding_box.width = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(
            self.txt_surface,
            (self.text_bounding_box.x + 5, self.text_bounding_box.y + 5),
        )
        # Blit the text_bounding_box.
        pygame.draw.rect(screen, self.color, self.text_bounding_box, 2)


class menuWordBox(inputBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary_path = "media/dictionary.txt"

    def handle_event(self, event):
        """
        Overloads the default input box template so that it can handle the specific instruction.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the input_box, toggle the active variable
            if self.text_bounding_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = COLOR_ACTIVE
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    map_word_length_to_words = parse_dictionary(self._dictionary_path)
                    if is_valid_word_in_dictionary(map_word_length_to_words, self.text):
                        return self.text.strip()
                    else:
                        self.prompt_for_valid_input()
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        if self._prompt_for_input:
            # Draw a prompt text message in the top right corner of the box
            prompt_instructions = "Please input a valid word"
            prompt_font = pygame.font.SysFont("monospace", 20)
            prompt_text = prompt_font.render(prompt_instructions, True, RED)
            screen.blit(
                prompt_text,
                (
                    screen.get_width() / 2
                    + self.text_bounding_box.width / 2
                    - prompt_text.get_width(),
                    screen.get_height() / 2
                    + self.text_bounding_box.height / 2
                    - prompt_text.get_height(),
                ),
            )

        # Blit the text.
        screen.blit(
            self.txt_surface,
            (self.text_bounding_box.x + 5, self.text_bounding_box.y + 5),
        )
        # Blit the text_bounding_box.
        pygame.draw.rect(screen, self.color, self.text_bounding_box, 2)


class menuGuessesBox(inputBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_event(self, event):
        """
        Overloads the default input box template so that it can handle the specific instruction.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the input_box, toggle the active variable
            if self.text_bounding_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = COLOR_ACTIVE
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.text.isnumeric() and is_valid_guess(int(self.text)):
                        return int(self.text)
                    else:
                        self.prompt_for_valid_input()
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        if self._prompt_for_input:
            # Draw a prompt text message in the bottom right corner of the box
            prompt_instructions = "Please input a valid word/number"
            prompt_font = pygame.font.SysFont("monospace", 20)
            prompt_text = prompt_font.render(prompt_instructions, True, RED)
            screen.blit(
                prompt_text,
                (
                    screen.get_width() / 2
                    + self.text_bounding_box.width / 2
                    - prompt_text.get_width(),
                    screen.get_height() / 2
                    + self.text_bounding_box.height / 2
                    - prompt_text.get_height(),
                ),
            )

        # Blit the text.
        screen.blit(
            self.txt_surface,
            (self.text_bounding_box.x + 5, self.text_bounding_box.y + 5),
        )
        # Blit the text_bounding_box.
        pygame.draw.rect(screen, self.color, self.text_bounding_box, 2)
