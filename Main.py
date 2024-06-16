from http.client import TOO_MANY_REQUESTS
from json import load
import time 
import Scripts.entity as Entity
import Scripts.tilemap as TMap
import sys

from Scripts.utils import Animation, Textbox, image_load, images_load, Textbox, Messagebox
import pygame
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("kairagan Alpha 0.1.1")
        self.game_font = pygame.font.Font("data/FFFFORWA.TTF",8)
        self.Screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()
        self.timer = 3600;
        self.time=0;
        self.camera_shift = [0,0]
        self.assets = {
            'decor': images_load('tiles/decor'),
            'surface': images_load('tiles/surface'),
            'glass': images_load('tiles/glass'),
            'large_decor': images_load('tiles/large_decor'),
            'player':image_load('entities/player.png'),
            'Jumper': images_load('functional_blocks/jumper'),
            'Exit': images_load('functional_blocks/Exit'),
            'player/idle':Animation(images_load("entities/player/idle"),duration=6),
            'player/run':Animation(images_load("entities/player/run"),duration=4),
            'player/jump':Animation(images_load("entities/player/jump"))
        }
        self.movement = [0, 0]
        self.tilemap = TMap.Tilemap(self)
        self.player = Entity.Player(self,self.tilemap.player_pos,(self.assets['player'].get_width(),self.assets['player'].get_height()))
        self.tilemap.load("data/Maps/map1.json")
        self.next_level= False
        self.level = 1;
        self.display.blit(image_load("background.png"),(-50,-30))
    
    def load_next_level(self):
        for i in range(0,1800):
            self.Screen.fill((5,31,57),(320-i,240-i,i,i))
            pygame.display.update()
        self.level+=1
        try:
            self.tilemap.load("data/Maps/map"+str(self.level)+".json")
            self.player.pos = self.tilemap.player_pos
        except:
            EndMassage = Messagebox("End Of Game",(20,20))
            EndMassage.render(self)
        self.next_level =False
    
    def reload(self):
        Deathbox = Textbox((180,240),"You're die",32,120,280)
        self.player.pos = self.tilemap.player_pos
        for i in range(0,1800):
            self.Screen.fill((5,31,57),(320-i,200-i,i,i))
            Deathbox.render(self.Screen,0)

            pygame.display.update()
            
        self.player.is_death = False
        self.tilemap.load("data/Maps/map"+str(self.level)+".json")
        


    def menu(self):
        menu_pos = 0
        self.display.blit(self.game_font.render("Kairagan",False,(255,142,128)),(10,10))
        start_button = Textbox((20,70),"Start")
        level_button = Textbox((20,110),"Level_editor")
        exit_button = Textbox((20,150),"Exit")
        while True:
            menu_pos=menu_pos%3
            menu_elements = ["Start","Level","Exit"]
            start_button.render(self.display,False)
            level_button.render(self.display,False)
            exit_button.render(self.display,False)
            match menu_pos:
                case 0:
                    start_button.render(self.display,True)
                case 1:
                    level_button.render(self.display,True)
                case 2:
                    exit_button.render(self.display,True)

            for event in pygame.event.get():
                match event.type:
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_DOWN:
                                menu_pos+=1
                            case pygame.K_UP:
                                menu_pos-=1
                            case pygame.K_SPACE:
                                print(menu_elements[menu_pos])
                                match menu_elements[menu_pos]:
                                    case "Start":
                                        self.run()
                                    case "Level":
                                        import editor
                                    case "Exit":
                                        pygame.quit()
                                        sys.exit()
            self.Screen.blit(pygame.transform.scale(self.display,self.Screen.get_size()),(0,0))                            
            pygame.display.update()
    
    def hud(self):
        if self.timer == 0:
            EndMessage = Messagebox("You fail mission and spaceship was completly breoken!!!",(20,20))
            self.player.is_death = True
            self.level = 1
            self.timer = 3600
            EndMessage.render()
        self.time= (self.time+1)%61
        self.timer-=self.time//60
        timer_text = Textbox((15,35),"Spaceship life time:"+str(self.timer),widht=150)
        timer_text.render(self.display,0)
        
        for i in range(0,self.player.stamina):
            pygame.draw.rect(self.display,(197,58,157),(15,10,(i/360)*100+1,10))
        pygame.draw.rect(self.display,(74,36,128),(15,10,100,10),1)
        self.display.blit(self.game_font.render("stamina:",False,(74,36,128)),(15,10))
    
    def camera_load(self):
        match self.tilemap.camera_info:
            case "only_x":
                self.camera_shift[0] = int(self.player.pos[0])-self.display.get_width()//2
                if self.camera_shift[0]<0:
                    self.camera_shift[0]=0 
            case "only_y":
                self.camera_shift[1] = (int(self.player.pos[1])-self.display.get_height()//2)
                if self.camera_shift[1]>0:
                    self.camera_shift[1]=0 
            case "free":
                self.camera_shift = ((int(self.player.pos[0])-self.display.get_width()//2),(int(self.player.pos[1])-self.display.get_height()//2))
    
    def run(self):
        intro = Messagebox("You woke up ahead of time. 230 years earlier.The cryocapsule blinks alarmingly: the ship is in trouble, the energy core is failing.You are the chief engineer of the expedition to Earth, the last hope of the crew. Survive and repair the core. Time is against you, engineer." ,(20,20))
        intro.render(self)
        intro = Messagebox("X - dash, Arrows keys - move,Escape - menu" ,(20,20))
        intro.render(self)
        while True:
            if self.next_level:
                self.load_next_level()
            if self.player.is_death:
                self.reload()
            self.display.fill((5,31,57))
            self.player.update(self.tilemap,self.movement)
            self.tilemap.render(self.display,self.camera_shift)
            self.player.render(self.display,self.camera_shift)
            self.tilemap.fun_render(self.display,self.camera_shift)
            self.hud()
            self.camera_load()
            for event in pygame.event.get():
                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    case pygame.KEYDOWN:

                        match event.key:

                            case pygame.K_LEFT:
                                self.movement[0] =-1

                            case pygame.K_RIGHT:
                                self.movement[0] = 1

                            case pygame.K_SPACE:
                                self.player.jump()
                            case pygame.K_x:
                                self.player.Phantom_dash()

                            case pygame.K_DOWN:
                                self.movement[1] = 1
                            case pygame.K_ESCAPE:
                                self.menu()
                                
                    case pygame.KEYUP:

                            match event.key:

                                case pygame.K_LEFT:
                                    self.movement[0] = 0

                                case pygame.K_RIGHT:
                                    self.movement[0] = 0     

                
            self.clock.tick(60)
            self.Screen.blit(pygame.transform.scale(self.display,self.Screen.get_size()),(0,0))
            pygame.display.update()
Game().menu()