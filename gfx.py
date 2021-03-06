import pygame, pygame.gfxdraw, math
from colors import RED, GREEN, LIGHTRED, LIGHTGREEN, DARKRED, KEYOUT

##Returns a surface with the keyboard drawn on it
def keys(keyboard, color = LIGHTGREEN, correct = None, corcolor = LIGHTRED):
    surf = pygame.Surface((556, 164))
    surf.fill(KEYOUT)
    surf.set_colorkey(KEYOUT)

    for row, keys in keyboard.items():
        for i, key in enumerate(keys):
            if type(correct) != list: keycolor = corcolor if key == correct else color
            else: keycolor = corcolor if key in correct else color
            x = (28 * row) + (56 * i)
            y = 56 * row
            pygame.draw.rect(surf, keycolor, [x, y, 52, 52])
            if key == 'f' or key == 'j':
                linecolor = tuple([min(255, max(0, c-85)) for c in keycolor])
                pygame.draw.line(surf, linecolor, (x + 8, y + 42), (x + 44, y + 42), 2)
    return surf

def timer(elapse, maxTime, radius = 80, innercolor = LIGHTRED, outercolor = DARKRED):
    surf = pygame.Surface(((radius+1) * 2, (radius+1) * 2))
    surf.fill(KEYOUT)
    surf.set_colorkey(KEYOUT)

    angle = int(elapse / maxTime * 720)
    cx = radius
    cy = radius
    points = [(cx, cy)]
    for i in range(angle, 720):
        x = cx + int((radius - 3) * math.cos(math.radians((i*0.5)-90)))
        y = cy + int((radius - 3) * math.sin(math.radians((i*0.5)-90)))
        points.append((x, y))

    pygame.gfxdraw.aacircle(surf, cx, cy, radius, outercolor)
    pygame.gfxdraw.filled_circle(surf, cx, cy, radius, outercolor)
    if len(points) > 2:
        pygame.gfxdraw.aapolygon(surf, points, innercolor)
        pygame.gfxdraw.filled_polygon(surf, points, innercolor)
    return surf

def lifebar(height, width, mistakes, maxAllowed):
    surf = pygame.Surface((width, height))
    pygame.draw.rect(surf, DARKRED, [0, 0, width, height])
    if mistakes <= maxAllowed - 1:
        pygame.draw.rect(surf, LIGHTRED, [0+2, 0+2, (width - 4) - ((width - 4) * mistakes/maxAllowed), height - 4])
    return surf
