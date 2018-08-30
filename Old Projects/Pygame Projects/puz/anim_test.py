import pygame
import Image

def should_quit():
    event = pygame.event.poll()
    return event.type == pygame.QUIT or event.type == pygame.KEYDOWN

def to_triplets(pil_palette):
    return [pil_palette[i:i+3] for i in range(0, len(pil_palette), 3)]
    
def make_sprite(image_filename):
    sprite = Sprite()
    if image_filename.endswith(".gif"):
        pil_image = Image.open(image_filename)
        sprite.image = pygame.image.fromstring(pil_image.tostring(), pil_image.size, 'P')
        palette = to_triplets(pil_image.getpalette())
        sprite.image.set_palette(palette)
        sprite.image.set_colorkey(pil_image.info['transparency'])
    else:
        sprite.image = pygame.image.load(image_filename)
    return sprite

class Sprite:
    position = (0, 0)
    def paint(self):
        screen.blit(self.image, self.position)

class Scene:
    sprites = []
    def __init__(self, sprites):
        self.sprites += sprites
    def paint(self):
        for sprite in self.sprites:
            sprite.paint()
        pygame.display.flip()
    def add_sprites(self, sprites):
        self.sprites += sprites

screen = pygame.display.set_mode((500, 375))
pygame.mouse.set_visible(False)

background = make_sprite('red-forest.jpg')
player = make_sprite('hulk.gif')
scene = Scene([background, player])

while not should_quit():
    scene.paint()
    player.position = pygame.mouse.get_pos()
