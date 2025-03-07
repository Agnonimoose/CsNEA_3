import time
import pygame, sys
from scripts.utils import load_image, load_images
from pygame.locals import *
import random, time, math
import json
# from network import Network 
from menu import menu
from level_select import level_menu
from lost_screen import lost_screen
from items import * 
from entities import * 
from data.constants import *

# Constants

# Tile types 
TILE_TYPES = {
    0: "air",
    1: "platform",
    2: "oxygen_pump",
    3: "pressure_plate"
}

pygame.init()
vec = pygame.math.Vector2 

#Setting up FPS 
FPS = 30
clock = pygame.time.Clock()





#Other Variables for use in the program


#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
OXYGEN_DECREASE_EVENT = pygame.USEREVENT + 1


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# BUFFER = pygame.Surface((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
BUFFER = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

def drawWindow(BUFFER):
    BUFFER.fill(WHITE)
    pygame.display.set_caption("Game")

clientNumber = 0


def update_camera(player, camera_offset): # Update the camera's offset based on the player's position
    global SCREEN_WIDTH, SCREEN_HEIGHT

    # Center the camera on the player
    camera_offset.x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_offset.y = player.rect.centery - SCREEN_HEIGHT // 2

    # Set camera to the bounds of the level
    camera_offset.x = max(0, min(camera_offset.x, LEVEL_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, LEVEL_HEIGHT - SCREEN_HEIGHT))

    return camera_offset

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - SCREEN_WIDTH), x)  # Right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)








class World:
    def __init__(self, load=True, level=1):
        self.level = level
        self.background = None
        self.ambientSound = None
        # self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.assets = {
            'decor': load_images('tiles/decor'),
            'stone': load_images('tiles/stone'),
            'ground': load_images('tiles/ground'),
            'grass': load_images('tiles/grass'),
            'ground': load_images('tiles/ground'),
            'large_decor': load_images('tiles/large_decor'),
            'pressure_plate': load_images('tiles/pressure_plate'),
            # 'player': load_image('entities/player.png'),
            # 'player/idle': Animation(load_images('entities/plaayer/idle'), img_dur=6),
            # 'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            # 'player/jump': Animation(load_images('entities/player/jump')),
            # 'player/slide': Animation(load_images('entities/player/slide')),
            # 'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }
        self.physicalTiles = {'grass', 'stone', 'ground'}
        self.itemTypes = {
                "Item": Item,
                 "Money": Money,
                 "OxygenPump": OxygenPump,
                 'PressurePlate': PressurePlate,
                 'BareRock': BareRock,
                 'MossyRock': MossyRock
                 }
        
        self.gameItems = {}


        self.tilemap = []
        self.neighbouring_offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1),
                    (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
        self.loadWorld(level)

    def loadWorld(self, level):
        with open("data/world.json", "r") as config_file:
            WORLD_CONFIG = json.load(config_file)
               
        # Load tilemap layers
        self.tilemap = WORLD_CONFIG[str(level)]["tilemap"]
        self.tilesize = WORLD_CONFIG[str(level)]["tilesize"]
        self.item_layer = WORLD_CONFIG[str(level)]["items"]
        self.entity_layer = WORLD_CONFIG[str(level)]["entities"]
        self.background = pygame.image.load(WORLD_CONFIG[str(level)]["background"])
        

        for y, row in enumerate(self.item_layer):
            for x, tile in enumerate(row):
                if tile == 2:  # Oxygen pump
                    self.items.add(OxygenPump("oxy", (x*TILE_SIZE, y*TILE_SIZE)))
                elif tile == 3:  # Pressure plate
                    self.items.add(PressurePlate("plate", (x*TILE_SIZE, y*TILE_SIZE)))



        # Load entities
        self.ast_start = self.entity_layer["astronaut"]
        self.alien_start = self.entity_layer["alien"]


        


    def renderWorld(self, BUFFER, offset = (0, 0), debug=False):
        if debug:
            for x in range(offset[0] // self.tilesize, (offset[0] + BUFFER.get_width()) // self.tilesize + 2):
                pygame.draw.line(BUFFER, (0, 255, 255), (x * self.tilesize - offset[0], 0),
                                (x * self.tilesize - offset[0], BUFFER.get_height()))
            for y in range(offset[1] // self.tilesize, (offset[1] + BUFFER.get_height()) // self.tilesize + 2):
                pygame.draw.line(BUFFER, (0, 255, 255), (0, y * self.tilesize - offset[1]),
                                (BUFFER.get_width(), y * self.tilesize - offset[1]))
        
        for x in range(offset[0] // self.tilesize, (offset[0] + BUFFER.get_width()) // self.tilesize + 1):
            for y in range(offset[1] // self.tilesize, (offset[1] + BUFFER.get_height()) // self.tilesize + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    # print(tile)
                    # print(offset)
                    BUFFER.blit(self.assets[tile['type']][tile['variant']], (
                        tile['pos'][0] * self.tilesize - offset[0], tile['pos'][1] * self.tilesize - offset[1]))

                    # tile_x = tile['pos'][0] * self.tilesize - offset[0]
                    # tile_y = tile['pos'][1] * self.tilesize - offset[1]
                    # rect = pygame.Rect(tile_x, tile_y, self.tilesize, self.tilesize)
                    # pygame.draw.rect(BUFFER, (255, 0, 0), rect, 1)  # Red rectangle, 1 pixel thick

    # def spawnItems(self, BUFFER, offset = (0, 0)):
    def spawnItems(self):
        for item in self.item_layer:
            self.gameItems[item["id"]] = self.itemTypes[item["type"]](item["id"], item["position"])

    def updateItems(self, buffer, offset):
        for id, item in self.gameItems.items():
            print("id = ", id)
            print("item = ", item)
            item.update(self)
            item.draw(buffer, offset)

    def tiles_around_pos(self, pos):
        tiles = []
        
        # tile_loc = (int(pos[0] // self.tilesize) + 1,
        #             int(pos[1] // self.tilesize))

        tile_loc = (int(pos[0] // self.tilesize),
                    int(pos[1] // self.tilesize))

        for offset in self.neighbouring_offsets:
            check_loc = str(tile_loc[0] + offset[0]) + \
                ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around_pos(self, pos):
        rects = []
        for tile in self.tiles_around_pos(pos):
            if tile['type'] in self.physicalTiles:
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tilesize, tile['pos'][1] * self.tilesize, self.tilesize, self.tilesize))
        return rects
    
    def tiles_around_rect(self, rect):  
        tiles = []

        top_left_tile = (rect.left // self.tilesize, rect.top // self.tilesize)
        bottom_right_tile = (rect.right // self.tilesize, rect.bottom // self.tilesize)


        for x in range(top_left_tile[0] - 1, bottom_right_tile[0] + 2):  
            for y in range(top_left_tile[1] - 1, bottom_right_tile[1] + 2): 
                tile_loc = str(x) + ';' + str(y)
                if tile_loc in self.tilemap:
                    tiles.append(self.tilemap[tile_loc])

        return tiles
    
    def physics_rects_around_rect(self, rect):
        rects = []
        for tile in self.tiles_around_rect(rect):
            if tile['type'] in self.physicalTiles:
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tilesize, tile['pos'][1] * self.tilesize, self.tilesize, self.tilesize))
        return rects

class Environment:
    def __init__(self, gravity, background, ambientSound):
        self.gravity = gravity

        
    def applyGravity(self, gravity):
        pass

    def loadLevel(self):
        pass

    def renderEnvironment(self):
        pass
 

# background = pygame.image.load("assets/bg.png") 

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name="none"):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.original_position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(topleft=(x, y))

    # def draw(self, buffer):
    #     buffer.blit(self.image, self.rect) 

    def draw(self, buffer, camera_offset, camera):
        self.updateRect(camera_offset)
        buffer.blit(self.image, camera.apply(self)) 

    def updateRect(self, camera_offset):
        # self.rect.topleft = self.original_position - camera_offset
        pass


 
def main_game(level):
    run = True

    world = World(level = level)
    AstrChar = Astronaut(position=world.ast_start, keys=ASTR_KEYS)
    # AlienChar = Alien(position=world.alien_start, keys=ALIEN_KEYS)
    world.spawnItems()
    clock.tick(FPS)


    drawWindow(BUFFER)
    bg_width, bg_height = world.background.get_size()

    pygame.time.set_timer(OXYGEN_DECREASE_EVENT, 1000)
    scroll = [0, 0]
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == OXYGEN_DECREASE_EVENT:
                if AstrChar.oxygen > 9:
                    AstrChar.oxygen -= 1
                for item in  world.items:
                    if item.id == 'pressureplate1':
                        item.interaction(world)

        scroll[0] += (AstrChar.rect.centerx -
                            BUFFER.get_width() / 2 - scroll[0]) / 30
        scroll[1] += (AstrChar.rect.centery -
                            BUFFER.get_height() / 2 - scroll[1]) / 30
        render_scroll = (int(scroll[0]), int(scroll[1]))

        BUFFER.fill(WHITE)
        # BUFFER.blit(world.background, (-camera_offset.x, -camera_offset.y))
        # BUFFER.blit(world.background, (-scroll[0], -scroll[1]))        

        for x in range(0, 2000, bg_width):
            for y in range(0, 1000, bg_height):
                BUFFER.blit(world.background, (x, y))

        world.renderWorld(BUFFER, offset=render_scroll)
        world.updateItems(BUFFER, render_scroll)
        # for item in world.items:
        #     # item.update(world.platforms, render_scroll)
        #     item.draw(BUFFER, render_scroll)

        # camera.update(AstrChar)

        # Draw both characters
        # AstrChar.draw(world.platforms, world.items, camera_offset, BUFFER, camera)
        # AstrChar.draw_inventory(BUFFER, camera)
        
        # AlienChar.update(world.platforms, world.items, camera_offset)
        
        
        
        AstrChar.draw(world, world.items, render_scroll, BUFFER)
        AstrChar.draw_inventory(BUFFER, render_scroll)
        

        
        SCREEN.blit(pygame.transform.scale(
            BUFFER, SCREEN.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)

        if AstrChar.oxygen <= 0:
            print("ASTO OUT OF OXYGEN!")
            return "loss"
            
if __name__ == "__main__":
    on = True
    while on:
        action = menu()
        
        if action == "play":
            level = level_menu()
            
            if level != "back":
                finished = main_game(level)
                
                if finished == "loss":
                    lost_menu = lost_screen()
                    if lost_menu == "continue":
                        pass