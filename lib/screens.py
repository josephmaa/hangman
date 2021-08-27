import pygame

from typing import Optional


class startingScreen(pygame.Surface):
    def __init__(
        resolution: tuple[float, float] = (1280, 720),
        flags: Optional[int] = 0,
        depth: Optional[int] = 0,
        masks: Optional[tuple(float)] = None,
    ):
        super.__init__(resolution, flags, depth, masks)
        

class mainScreen(pygame.Surface):
    def __init__(
        resolution: tuple[float, float] = (1280, 720),
        flags: Optional[int] = 0,
        depth: Optional[int] = 0,
        masks: Optional[tuple(float)] = None,
    ):
        super.__init__(resolution, flags, depth, masks)
