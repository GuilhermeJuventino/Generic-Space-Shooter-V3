import pygame


class SpriteSheet:
    def __init__(self, image: pygame.Surface, bg: tuple[int, int, int] = (0, 0, 0)):
        self.bg = bg
        self.sheet = image

        # Width of each sprite NOT sprite sheet
        self.width, self.height = 0, 0

    def get_images(self, rows: int, columns: int, width: float, height: float, fixer: float = 1, bound=True, scale=None):
        self.width = width
        self.height = height

        self.scale = scale

        if not scale:
            self.scale = 2

        images = []

        for i in range(rows):
            for e in range(columns):
                # Mod image
                image = self.sheet.subsurface(pygame.Rect((e * width), ((i * fixer) * columns), width, height)).convert_alpha()
                image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
                if bound:
                    r = image.get_bounding_rect()
                    image = image.subsurface(r)

                images.append(image)

        return images
