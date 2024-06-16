
from Scripts.utils import Animation, images_load
import pygame
class functional_block:

    def __init__(self,type,pos,game,tile_size=16):
        self.pos = (pos[0]*tile_size,pos[1]*tile_size)
        self.type = type
        self.tile_size = tile_size
        self.game = game
        self.player = self.game.player
        self.animation =  Animation(self.game.assets[self.type].copy())
        self.active = False
        
    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1]-2,self.animation.img().get_width(),self.animation.img().get_height())
    def render(self):
        self.game.display.blit(self.animation.img(),(self.pos[0]-self.game.camera_shift[0],self.pos[1]-self.game.camera_shift[1]))
        if self.active:
            self.game.display.blit(self.animation.img(),(self.pos[0]-self.game.camera_shift[0],self.pos[1]-self.game.camera_shift[1]))
            self.animation.update()
            

class Jumper_block(functional_block):

    def __init__(self,pos,game):
        super().__init__("Jumper",pos,game)

    def update(self):
        if self.player.collisions["down"] and self.rect().colliderect(self.player.rect()):
            self.player.velocity[1]= -4.5
            self.active = True

class Exit_block(functional_block):

    def __init__(self,pos,game):
        super().__init__("Exit",pos,game)

    def update(self):
        if self.rect().colliderect(self.player.rect()):
            self.game.next_level = True

    def render(self):
        self.game.display.blit(self.animation.img(),(self.pos[0]-self.game.camera_shift[0],self.pos[1]-self.game.camera_shift[1]))
        self.animation.update()
    
        
