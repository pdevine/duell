
import os.path

import game

import pygame

from pygame.locals import *

CARD_MAPPING = [
   ['1.png', '2.png', '3.png', '4.png'],
   ['49.png', '50.png', '51.png', '52.png'],
   ['45.png', '46.png', '47.png', '48.png'],
   ['41.png', '42.png', '43.png', '44.png'],
   ['37.png', '38.png', '39.png', '40.png'],
]


def loadImage(filename):
    fullname = os.path.join('images', filename)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print "Cannnot load image:", fulname
        raise SystemExit, message

    return image, image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, position=0, actionType='resting'):
        pygame.sprite.Sprite.__init__(self)

        self.actions = {
            'resting' : {
                'offset' : 0,
                'updateFrameCount' : 100,
                'frames' : 2,
                'startFrame' : 0,
                },
            'walking' : {
                'offset' : 1,
                'updateFrameCount' : 17,
                'frames' : 4,
                'startFrame' : 0,
                },
            'attacking' : {
                'offset' : 2,
                'updateFrameCount' : 15,
                'frames' : 3,
                'startFrame' : 0,
                },
            'dying' : {
                'offset' : 3,
                'updateFrameCount' : 15,
                'frames' : 3,
                'startFrame' : 0,
                }
        }

        self.imageSheet, rect = loadImage('player1.png')
        self.rect = pygame.Rect(0, 0, 128, 128)
        self.moveToRect = pygame.Rect(0, 0, 0, 0)

        self.setPosition(position)
        self.setAction(actionType)

        self.updateCycle = 0
        self.updateCounter = 0

    def setPosition(self, position=0):
        self.rect.y = 280
        self.rect.x = (52 * position) + 2
        self.position = position

    def moveToPosition(self, position=0):
        self.position = position
        self.moveToRect.x = (52 * position) + 2
        self.setAction('walking')

    def setAction(self, actionType):
        assert actionType in self.actions.keys()

        self.images = []

        self.action = actionType
        actionData = self.actions[self.action]

        for count in range(actionData['frames']):
            surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            surface.blit(self.imageSheet, (0, 0),
                pygame.Rect(
                    count * 128,
                    128 * actionData['offset'],
                    128,
                    128))

            if (actionType == 'walking' and self.moveToRect.x < self.rect.x) or \
               (actionType != 'walking' and self.position >= 12):
                surface = pygame.transform.flip(surface, True, False)

            self.images.append(surface)

        self.image = self.images[actionData['startFrame']]
        self.updateCycle = actionData['startFrame']
        self.updateCounter = 0

        self.frames = actionData['frames']
        self.updateFrameCount = actionData['updateFrameCount']

    def update(self):
        if self.updateCycle % self.updateFrameCount == 0:
            self.updateCounter += 1
            if self.updateCounter >= self.frames:
                self.updateCounter = 0

            self.image = self.images[self.updateCounter]

        self.updateCycle += 1

        if self.rect.x < self.moveToRect.x:
            self.rect.x += 1
        elif self.action == 'walking' and self.rect.x == self.moveToRect.x:
            self.setAction('resting')


class Card(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage(os.path.join('cards', '1.png'))

    def update(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))

    bg, bgRect = loadImage('bg.png')

    screen.blit(bg, (0, 50))

    player1 = Player(21)

    spriteList = pygame.sprite.Group(player1)

    while True:
        screen.blit(bg, (0, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                player1.moveToPosition(player1.position - 4)

        spriteList.update()

        spriteList.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
