
import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False,"down": False,"left": False,"right": False}

        self.flip = False
        self.action = ""
        self.anim_offset = (-3,-3)
        self.set_action("idle")

    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type+'/'+self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self,tilemap, movement=(0,0), gravity=0.1,dash = False):
        self.collisions = {"up": False,"down": False,"left": False,"right": False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        
        self.pos[0]+=frame_movement[0]
        entity_rect = self.rect()
        if not dash:
            for rect in tilemap.physics_tiles_around(self.pos):
                if entity_rect.colliderect(rect):
                    if frame_movement[0] > 0:
                        entity_rect.right = rect.left
                        self.collisions["right"] = True 
                    if frame_movement[0] < 0:
                        entity_rect.left  = rect.right
                        self.collisions["left"] = True 
                    self.pos[0] = entity_rect.x
                 

        if not dash:
            self.pos[1]+=frame_movement[1]
        entity_rect = self.rect()
        if not dash:
            for rect in tilemap.physics_tiles_around(self.pos):
                if entity_rect.colliderect(rect):
                    if frame_movement[1] > 0:
                        entity_rect.bottom  = rect.top
                        self.collisions["down"] = True
                    if frame_movement[1] < 0:
                        entity_rect.top = rect.bottom
                        self.collisions["up"] = True 
                    self.pos[1] =entity_rect.y

        
        self.velocity[1] = min(5,self.velocity[1]+gravity)

        if self.velocity[0]<0:
            self.velocity[0] = min(0,self.velocity[0]+gravity)
        else:
            self.velocity[0] = max(0,self.velocity[0]-gravity)

        if movement[0]>0:
            self.flip = False
        if movement[0]<0:
            self.flip = True

        if self.collisions["up"] or self.collisions["down"]:
            self.velocity[1] = 0

        self.animation.update()
  
    def render(self,display,shift = (0,0)):
        display.blit(pygame.transform.flip(self.animation.img(), self.flip, False),(self.pos[0]-shift[0]+self.anim_offset[0],self.pos[1]-shift[1]+self.anim_offset[1]))
        
    
class Player(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)
        self.air_time = 0
        self.stamina = 360
        self.wall_grap = True
        self.dashing = 0
        self.dash = False
        self.is_death = False
    def update(self,tilemap,movement=(0,0)):
        super().update(tilemap, movement=movement,dash=self.dash)

        self.air_time+=1
        if self.wall_grap:
            self.stamina-=1

        if self.collisions['down']:
            self.air_time = 0
            self.wall_grap = False
            self.stamina = 360

        if self.air_time>4:
            self.set_action('jump')

        if self.collisions["right"] or self.collisions["left"] and self.air_time>4:
            self.wall_grap =False
            
            if self.stamina >0:

                self.velocity[1] = 0
                self.wall_grap = True

        if self.dashing>0:
            self.dashing = max(0,self.dashing-1)
        if self.dashing<0:
            self.dashing = min(0,self.dashing+1) 

        if self.dashing!=0:
            self.velocity[0] = abs(self.dashing)/self.dashing*8
            if abs(self.dashing) == 1:
                self.velocity[0]*=0.01
                self.dash = False
                entity_rect = self.rect()
                for rect in tilemap.physics_tiles_around(self.pos):
                    if entity_rect.colliderect(rect):
                        self.is_death = True

       
        elif movement[0]!=0:
            self.set_action('run')
        else:
            self.set_action('idle')
    def jump(self):

        if self.wall_grap == True:

            if self.collisions["right"]:
                self.stamina-=60
                self.velocity[1] = -3
                self.velocity[0] = -2

            if self.collisions["left"]:
                self.stamina-=60
                self.velocity[1] = -3
                self.velocity[0] = 2

        else:
            if self.air_time<5:
                self.velocity[1] = -3

    def Phantom_dash(self):
        if self.dashing==0 and self.stamina>0:
            self.stamina-=360
            if self.flip:
                self.dashing = -10
            else: 
                self.dashing = 10
            self.dash =True