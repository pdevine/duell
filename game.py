
import os.path

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
    def __init__(self, actionType='resting'):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.actions = {
            'resting' : {
                'offset' : 0,
                'updateFrameCount' : 100,
                'frames' : 2,
                },
            'walking' : {
                'offset' : 1,
                'updateFrameCount' : 30,
                'frames' : 4,
                },
            'attacking' : {
                'offset' : 2,
                'updateFrameCount' : 15,
                'frames' : 3,
                },
            'dying' : {
                'offset' : 3,
                'updateFrameCount' : 15,
                'frames' : 3,
                }
        }

        self.imageSheet, rect = loadImage('player1.png')
        self.rect = pygame.Rect(0, 0, 128, 128)

        self.setAction(actionType)

        self.updateCycle = 0
        self.updateCounter = 0

    def setAction(self, actionType):

        assert actionType in self.actions.keys()

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
            self.images.append(surface)

        self.image = self.images[0]

        self.frames = actionData['frames']
        self.updateFrameCount = actionData['updateFrameCount']

    def update(self):
        if self.updateCycle % self.updateFrameCount == 0:
            self.updateCounter += 1
            if self.updateCounter >= self.frames:
                self.updateCounter = 0

            self.image = self.images[self.updateCounter]

        self.updateCycle += 1


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

    card = Card()
    player1 = Player()
    player1.rect.x = 200
    player1.rect.y = 200

    player2 = Player('walking')
    player2.rect.x = 400
    player2.rect.y = 200

    player3 = Player('dying')
    player3.rect.x = 0
    player3.rect.y = 200

    player4 = Player('attacking')
    player4.rect.x = 100
    player4.rect.y = 400

    spriteList = pygame.sprite.Group(card, player1, player2, player3, player4)

    while True:
        screen.blit(bg, (0, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        spriteList.update()

        spriteList.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
