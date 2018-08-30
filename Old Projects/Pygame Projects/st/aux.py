from const import *

def load_image(name, color_key=None, scaling=1):
    pathname=os.path.join(IMG_DIR,name+IMG_EXT)
    try:
        image=pygame.image.load(pathname)
    except pygame.error, msg:
        #print 'Error loading image %s' % name
        raise SystemExit, msg
    image=image.convert()
    if color_key:
        if color_key==-1:
            color_key=image.get_at((0,0))
        image.set_colorkey(color_key, RLEACCEL)
    if scaling!=1:
        image=scale(image, (int(image.get_size()[0]*scaling),
                            int(image.get_size()[1]*scaling)))
    return image

def load_all_images():
    for i in STR_NAMES:
        images[i]=load_image(i)

def calc_borders():
    for s in STR_NAMES:
        w=2*BORDER_WIDTH
        tmp=pygame.Surface((STR_WIDTHS[s]*WIDTH, STR_HEIGHTS[s]*HEIGHT)).convert()
        tmp.fill(BORDER_COLOR)
        tmp2=pygame.Surface((tmp.get_size()[0]-w, tmp.get_size()[1]-w)).convert()
        tmp2.fill((1,1,1))
        tmp.blit(tmp2, (BORDER_WIDTH, BORDER_WIDTH))
        tmp.set_colorkey((1,1,1))
        BORDERS[s]=pygame.sprite.Sprite()
        BORDERS[s].image=tmp
        BORDERS[s].rect=tmp.get_rect()
