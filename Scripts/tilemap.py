
import json
import pygame
from Scripts.functional_blocks import functional_block,Jumper_block,Exit_block
NEIGBOURS = [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(0,0),(-1,1),(0,1),(1,1)]
PHYSICS_TILES = {"surface","Jumper"}
FUNC_BLOCKS = {"jumper"}
class Tilemap:

    def __init__(self,game,tsize=16):
        self.game = game
        self.tile_size = tsize;
        self.tilemap = {}
        self.functional_blocks = []
        self.offgrid_tiles = []
        self.camera_info = "only_x"
        self.player_pos = (50,50)

    def tiles_around(self,pos):
        tiles = []
        tile_loc = (int(pos[0]/self.tile_size),int(pos[1]/self.tile_size))
        for ne_tile in NEIGBOURS:
            check_loc = str(tile_loc[0]+ne_tile[0])+";"+str(tile_loc[1]+ne_tile[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles 
    
    def physics_tiles_around(self,pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0]*self.tile_size,tile["pos"][1]*self.tile_size,self.tile_size,self.tile_size))
        return rects

    def save(self,path,camera_info,player_pos):

        f = open(path,"w")
        json.dump({"tilemap": self.tilemap,"tile_size": self.tile_size, "offgrid": self.offgrid_tiles, "camera": camera_info,"player":player_pos},f)
        f.close()

    def load(self,path):
        self.functional_blocks.clear()
        f = open(path,"r")
        map_data = json.load(f)
        f.close()
        self.camera_info = map_data["camera"]
        self.player_pos = map_data["player"]

        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]
        
        for tile in self.tilemap:
            match self.tilemap[tile]["type"]:
                case "Jumper":
                    self.functional_blocks.append(Jumper_block(self.tilemap[tile]["pos"],self.game))
                case "Exit":
                    self.functional_blocks.append(Exit_block(self.tilemap[tile]["pos"],self.game))

    def eload(self,path):

        f = open(path,"r")
        map_data = json.load(f)
        f.close()
        if "camera" in map_data:
            self.camera_info = map_data["camera"]
        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]

    def render(self,surf,shift=(0,0)):

        for offtile in self.offgrid_tiles:
            surf.blit(self.game.assets[offtile["type"]][offtile["variant"]],(offtile["pos"][0]-shift[0],offtile["pos"][1]-shift[1]))

        for x in range(shift[0] // self.tile_size, (shift[0]+surf.get_width())//self.tile_size+1):
            for y in range(shift[1] // self.tile_size, (shift[1]+surf.get_height())//self.tile_size+1):
                loc = str(x)+";"+str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]*self.tile_size- shift[0],tile['pos'][1]*self.tile_size- shift[1]))
        
    def fun_render(self,surf,shift):
            for fb in self.functional_blocks:
                fb.update()
                fb.render()
