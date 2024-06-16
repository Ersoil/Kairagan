from json import load
from socket import gaierror
import Scripts.tilemap as TMap
import sys
from Scripts.utils import Animation, image_load, images_load, Textbox, Messagebox
import pygame
RENDER_SCALE = 2.0
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Editor")
        self.Screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()
        self.camera_shift = [0,0]
        self.assets = {
            'decor': images_load('tiles/decor'),
            'glass': images_load('tiles/glass'),
            'surface': images_load('tiles/surface'),
            'Jumper': images_load('functional_blocks/jumper'),
            'Exit': images_load('functional_blocks/Exit'),
            'large_decor': images_load('tiles/large_decor'),
        }

        self.level = "map1.json"
        self.camera_info = ["only_x","only_y","free"]
        self.camera_type = 0
        self.tilemap = TMap.Tilemap(self)
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.Clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.player_position = (50,50)
        self.tilemap.eload("data/Maps/map1.json")

    def ui(self):
        level_info = Textbox((10,20),self.level)
        camera_info = Textbox((120,20),self.camera_info[self.camera_type])
        level_info.render(self.display,0)
        camera_info.render(self.display,0)

    def run(self):
        intro = Messagebox("L - level info edit, O - save level, LKM/RKM - tiles add/delete, alt - offgrid_tiles",(20,20))
        intro.render(self) 
        ui_enable = True
        level_edit = False
        level_select = 0;
        while True:
            self.display.fill((5,31,57))
            self.scroll[0]+=(self.movement[1]-self.movement[0])
            self.scroll[1]+=(self.movement[3]-self.movement[2])
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
        
            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            self.tilemap.render(self.display,shift = render_scroll)

            if ui_enable:
                self.ui()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0]/ RENDER_SCALE, mouse_pos[1]/RENDER_SCALE)
            tile_pos = (int((mouse_pos[0]+self.scroll[0])//self.tilemap.tile_size),int((mouse_pos[1]+self.scroll[1])//self.tilemap.tile_size))
            
            if self.Clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0])+";"+str(tile_pos[1])] = {"type": self.tile_list[self.tile_group],"variant": self.tile_variant, "pos": tile_pos}

            if self.right_clicking and self.ongrid:
                tile_loc = str(str(tile_pos[0])+";"+str(tile_pos[1]))
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            if self.right_clicking and not self.ongrid:
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(tile["pos"][0]-self.scroll[0],tile["pos"][1]-self.scroll[1],tile_img.get_width(),tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos[0],mouse_pos[1]):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img,mouse_pos)

            for event in pygame.event.get():
                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.MOUSEBUTTONDOWN:
                        
                        if event.button == 1:
                                self.Clicking = True
                                if not self.ongrid:
                                    self.tilemap.offgrid_tiles.append({"type": self.tile_list[self.tile_group],"variant": self.tile_variant, "pos":(mouse_pos[0]+self.scroll[0],mouse_pos[1]+self.scroll[1])})
                        
                        if event.button == 3:
                                self.right_clicking = True
                        
                        if level_edit:
                            level_select= level_select%60
                            if self.shift:
                                
                                if event.button==5:
                                    self.camera_type+=1
                                    self.camera_type = self.camera_type% len(self.camera_info)
                                
                                if event.button==4:
                                    self.camera_type-=1
                                    self.camera_type = self.camera_type% len(self.camera_info)
                            
                            elif event.button == 5:
                                level_select+=1
                                self.level = "map"+ str(level_select)+ ".json"
                            
                            elif event.button ==4:
                                level_select-=1
                                self.level = "map"+ str(level_select)+ ".json"
                        if self.shift:
                            
                            if event.button == 4:
                                self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                            
                            if event.button == 5:
                                self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                        else:
                            
                            if event.button == 4:
                                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                                self.tile_variant = 0
                            
                            if event.button == 5:
                                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                                self.tile_variant = 0

                    case pygame.MOUSEBUTTONUP:

                        if event.button == 1:
                                self.Clicking = False
                        
                        if event.button == 3:
                                self.right_clicking = False

                    case pygame.KEYDOWN:

                        match event.key:

                            case pygame.K_a:
                                self.movement[0] = 5

                            case pygame.K_d:
                                self.movement[1] = 5

                            case pygame.K_w:
                                self.movement[2] = 5

                            case pygame.K_s:
                                self.movement[3] = 5
                            case pygame.K_o:
                                self.tilemap.save("data/Maps/"+self.level,self.camera_info[self.camera_type],list(self.player_position))
                            case pygame.K_p:
                                self.player_position = (tile_pos[0]*self.tilemap.tile_size,tile_pos[1]*self.tilemap.tile_size)
                            case pygame.K_LALT:
                                self.ongrid = False

                            case pygame.K_ESCAPE:
                                import Main

                            case pygame.K_LSHIFT:
                                self.shift = True

                            case pygame.K_h:
                                ui_enable = not ui_enable

                            case pygame.K_l:
                                level_edit = not level_edit
                                
                    case pygame.KEYUP:

                        match event.key:

                            case pygame.K_a:
                                self.movement[0] = 0

                            case pygame.K_d:
                                self.movement[1] = 0

                            case pygame.K_w:
                                self.movement[2] = 0

                            case pygame.K_s:
                                self.movement[3] = 0

                            case pygame.K_LALT:
                                self.ongrid = True

                            case pygame.K_LSHIFT:
                                self.shift = False    
                
            self.clock.tick(60)
            self.Screen.blit(pygame.transform.scale(self.display,self.Screen.get_size()),(0,0))
            pygame.display.update()
Editor().run()