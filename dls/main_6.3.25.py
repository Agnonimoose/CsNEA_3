import time, os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

import pygame, sys
from pygame.locals import *
import random, time, math
import json
# from network import Network 
from menu import menu
from level_select import level_menu
from lost_screen import lost_screen

with open("character_config.json", "r") as config_file:
    CHARACTER_CONFIG = json.load(config_file)
    

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

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
color_light = (170,170,170)  
color_dark = (100,100,100) 
GREY = (125, 121, 121)
DARK_BLUE = (18, 25, 87) 

font = pygame.font.Font(None, 24)  # Default font, size 24


#Other Variables for use in the program
LEVEL_WIDTH = 1000 
LEVEL_HEIGHT = 800
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
ACC = 0.5
FRIC = -0.12
GRAVITY = 0.5
TILE_SIZE = 32
GRID_WIDTH = LEVEL_WIDTH // TILE_SIZE
GRID_HEIGHT = LEVEL_HEIGHT // TILE_SIZE

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
OXYGEN_DECREASE_EVENT = pygame.USEREVENT + 1


BUFFER = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def drawWindow(BUFFER):
    BUFFER.fill(WHITE)
    pygame.display.set_caption("Game")

clientNumber = 0

ASTR_KEYS = {
    "left": K_a,  
    "right": K_d,  
    "up": K_w,
    "interact" : K_SPACE
}

ALIEN_KEYS = {
    "left": K_LEFT,  
    "right": K_RIGHT,  
    "up": K_UP,
    "interact" : K_KP_ENTER
}

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


camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)

class Character(pygame.sprite.Sprite):
    def __init__(self, characterType, position=(0, 0)):
        self.position = position  # (x, y) coordinates of the players
        self.speed = CHARACTER_CONFIG.get(characterType, {}).get("speed", 5) # movement speed
        self.velocity_y = 0
        self.characterType = characterType

        self.image = pygame.Surface((30, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.jumping = False
        self.on_ground = False
        self.rect_checker = None
        self.standing_on = None

    def move(self, direction):
        x, y = self.position
        if direction == "none":
            return
        elif direction == 'up':
            self.jump()
        else:
            if direction == 'down':
                y -= self.speed
            elif direction == 'left':
                x -= self.speed
            elif direction == 'right':
                x += self.speed

            self.position = (x, self.position[1])  
            self.update_rect()


    def jump(self):
        # print("jumping -> self.jumping ", self.jumping, " self.on_ground -> ", self.on_ground)
        # if (self.jumping == False ) and (self.on_ground == True):
        #     self.jumping = True
        if self.on_ground == True:
            self.velocity_y = -10
            self.on_ground = False
            self.standing_on = None

    def apply_gravity(self):
        x, y = self.position
        if not self.on_ground:
            self.velocity_y += GRAVITY
        y += self.velocity_y
        self.position = (x, y)
        max_velocity = 10
        self.velocity_y = min(self.velocity_y, max_velocity)


    def check_collisions(self, platforms, camera_offset):
        # pygame.draw.rect(BUFFER, (255, 0, 0), self.rect, 2)  # Player collision box
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                print("collided at -> ", platform.name, " velocity_y -> ", self.velocity_y, " position ", self.position)
                
                #this section checks if the player hits the ground while falling and resets their y velocity to 0
                # if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                #     self.rect.bottom = platform.rect.top
                #     self.velocity_y = 0                 
                #     self.on_ground = True
                #     self.standing_on = platform
                
                # elif self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right:
                #     if self.position[0] < platform.rect.centerx:  
                #         self.rect.right = platform.rect.left
                #     elif self.position[0] > platform.rect.centerx:  
                #         self.rect.left = platform.rect.right
                #     self.rect.y = self.position[1]
                                        
                # self.position = self.rect.topleft
                
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.standing_on = platform
                    
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 10:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

                if self.rect.right > platform.rect.left and not self.rect.left > platform.rect.left:
                    self.rect.right = platform.rect.left

                elif self.rect.left < platform.rect.right and not self.rect.right < platform.rect.right:
                    self.rect.left = platform.rect.right

        
        if self.on_ground and self.velocity_y == 0:
            if self.check_falling_off() == True:
                self.on_ground = False
                self.standing_on = None

                    
    def check_falling_off(self):
        if not self.standing_on:
            return True
        self.check_rect = self.rect.copy()
        self.check_rect.y += 1  
        # self.standing_on.up
        if self.check_rect.colliderect(self.standing_on.rect):
            return False
        return True  

    def update_rect(self):
        # print("updating rec")
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.rect.topleft = self.position

    def getDistance(self, other, this = None):
        if this == None:
            this = self.position
        
        return math.sqrt((this[0] - other[0])**2 + (this[1] - other[1])**2)


class Player(Character):
    def __init__(self, speed, position=(0, 0), keys=ASTR_KEYS):
        super().__init__("player", position) # calls the character's constructor 
        self.width = 30
        self.height = 40
        self.left = False
        self.right = True
        self.KEYS = keys

    def takeDamage(self):
        pass

    def check_collisions(self, tilemap, camera_offset):
        self.on_ground = False
        for tile in tilemap:
            if self.rect.colliderect(tile.rect):
                print(f"Collision with tile at {tile.x}, {tile.y}")  # Debug statement
                
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = tile.rect.bottom
                self.velocity_y = 0

                # Call tile interaction if it's a pressure plate
                tile.interact(self)  # This assumes tile has an interact method

        
    def interact(self, items):
        for item in items:
            print(f'item {item.id} found at {item.position}, my postion at {self.position} our distance = {self.getDistance(item.position)}')
            # if self.getDistance(item.position) < 25:
            if self.getDistance(item.position) < 31:
                print("can interact with item!")
                item.interaction(self)


    def interactWithObject(self, obj):
        pass

    def updatePlayerState(self):
        pass

    def update(self, platforms, items, camera_offset):
        pressed_keys = pygame.key.get_pressed()
        key_strokes = []
        if pressed_keys[self.KEYS["left"]]:
            key_strokes.append("left")
        if pressed_keys[self.KEYS["right"]]:
            key_strokes.append("right")
        if pressed_keys[self.KEYS["up"]]:
            key_strokes.append("up")
            
        for direction in key_strokes:
            self.move(direction)
        
        if pressed_keys[self.KEYS["interact"]]:
            self.interact(items)
            
        self.apply_gravity()
        self.check_collisions(platforms, camera_offset)
        self.update_rect()


class Enemy(Character):
    def __init__(self, position=(0, 0)):
        super().__init__("enemy", position)

        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

class Alien(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, phaseAbilityDuration=10, shapeShiftState="default"):
        super().__init__(speed, position, keys)  # calls the player's constructor
        self.playerType = "alien"
        self.phaseAbilityDuration = phaseAbilityDuration 
        self.shapeShiftState = shapeShiftState
        self.image = pygame.image.load("assets/alien_still.png")  
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def phaseThroughWalls(self):
        pass

    def shapeShift(self):
        pass

class Astronaut(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, oxygenLevel=100, toolbox=None, currentEnvironment="space_station"):
        super().__init__(speed, position, keys)  # calls the player's constructor
        self.playerType = "astronaut"
        self.baseSpeed = speed             # base speed (used on the space station, matches the alien's)
        self.oxygenLevel = oxygenLevel     
        self.toolbox = toolbox if toolbox is not None else []  # toolbox is an empty list, updates as the player gets items
        self.currentEnvironment = currentEnvironment  # this is the environment of the level (Space station or Planet), this affects speed
        self.rfid_use = False  # boolean flag for RFID scanner usage
        self.rfid_detectable = []  # list to store detected items or enemies
        self.lastDepletionTime = time.time() #tracks the time oxygen was last depleted
        
        self.show_inventory = False
        self.inventory_open = False
        self.inventory_size = 4  
        self.selected_slot = 0

        self.image = pygame.image.load("assets/astronaut_still.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        self.player_max_hp = 100
        self.player_hp = 100
        self.hp_bar_width = 50
        self.hp_bar_height = 5
        
        self.oxygen_max = 100
        self.oxygen = 100
        self.oxygen_bar_width = 50
        self.oxygen_bar_height = 5

    def oxygenDeplete(self, oxygenLevel):
        currentTime = time.time()
        if currentTime - self.lastDepletionTime >= 2: #compares the last time oxygen was depleted to the current time
            if self.oxygenLevel > 0: #oxygen cannot deplete if it is at 0
                oxygenLevel -= 1
        return oxygenLevel
        #oxygen is depleted by 1% every 2 seconds, will stop depleting after it reaches 0
        
    def draw_inventory(self, buffer, camera):
        if self.show_inventory:
            # Calculate screen position
            screen_pos = camera.apply(self)
            
            # Inventory panel dimensions
            panel_width = 150
            panel_height = 50
            slot_size = 32
            
            # Position above player's head
            inv_x = screen_pos.x - panel_width//2 + self.rect.width//2
            inv_y = screen_pos.y - panel_height - 20
            
            # Draw background
            pygame.draw.rect(buffer, DARK_BLUE, (inv_x, inv_y, panel_width, panel_height), border_radius=5)
            pygame.draw.rect(buffer, GREY, (inv_x, inv_y, panel_width, panel_height), 2, border_radius=5)
            
            # Draw slots
            slot_spacing = 5
            start_x = inv_x + slot_spacing
            for i in range(4):
                slot_rect = pygame.Rect(start_x + i*(slot_size+slot_spacing), inv_y + slot_spacing, slot_size, slot_size)
                pygame.draw.rect(buffer, color_light, slot_rect, border_radius=3)
                
                # Draw items if present
                if i < len(self.toolbox):
                    item_img = pygame.transform.scale(self.toolbox[i].image, (slot_size, slot_size))
                    buffer.blit(item_img, slot_rect.topleft)
                    
        pressed_keys = pygame.key.get_pressed()
            
        # Add inventory toggle
        if pressed_keys[K_e]:
            if not self.inventory_open:
                self.show_inventory = not self.show_inventory
                self.inventory_open = True
        else:
            self.inventory_open = False

    def repairObject(self): #use tools to repair or interact with objects
        pass

    def replenishOxygen(self): #called whenever the astronaut interacts with an oxygen refill station
        if self.interactWithObject(OxygenPump) == True:
            oxygenLevel = 100
        return oxygenLevel

    def scanWithRFID(self, items_on_screen):
        self.rfid_detectable = items_on_screen

        overlay = "\n".join(f"Detected: {item}" for item in self.rfid_detectable)
        print("RFID Scan Results:\n" + overlay)
        pygame.time.wait(1000) # duration of the scan
        self.rfid_use = False # finishes the scan


    def draw(self, platforms, items, camera_offset, BUFFER, camera):
        self.update(platforms, items, camera_offset)
        
        screen_pos = camera.apply(self)

        BUFFER.blit(self.image, screen_pos)  # Draw player sprite at adjusted position

        ox_bar_x = screen_pos.x + (self.rect.width - self.oxygen_bar_width) // 2
        ox_bar_y = screen_pos.y - 10  
        pygame.draw.rect(BUFFER, GREY, (ox_bar_x, ox_bar_y, self.oxygen_bar_width, self.oxygen_bar_height), border_radius=5)
        pygame.draw.rect(BUFFER, DARK_BLUE, (ox_bar_x, ox_bar_y, self.oxygen_bar_width * (self.oxygen / self.oxygen_max), self.oxygen_bar_height), border_radius=5)

        ox_text = f"Oxygen: {self.oxygen}/{self.oxygen_max}"
        ox_text_surface = font.render(ox_text, True, BLACK)  
        ox_text_x = ox_bar_x + (self.oxygen_bar_width - ox_text_surface.get_width()) // 2
        ox_text_y = ox_bar_y - 15  
        # BUFFER.blit(ox_text_surface, (ox_text_x, ox_text_y))

        hp_bar_x = screen_pos.x + (self.rect.width - self.hp_bar_width) // 2
        hp_bar_y = screen_pos.y - 20 
        pygame.draw.rect(BUFFER, RED, (hp_bar_x, hp_bar_y, self.hp_bar_width, self.hp_bar_height), border_radius=5)
        pygame.draw.rect(BUFFER, GREEN, (hp_bar_x, hp_bar_y, self.hp_bar_width * (self.player_hp / self.player_max_hp), self.hp_bar_height), border_radius=5)

        hp_text = f"HP: {self.player_hp}/{self.player_max_hp}"
        text_surface = font.render(hp_text, True, BLACK)  
        text_x = hp_bar_x + (self.hp_bar_width - text_surface.get_width()) // 2
        text_y = hp_bar_y - 15  
        # BUFFER.blit(text_surface, (text_x, text_y))


class World:
    def __init__(self, load=True, level=1):
        self.level = level
        self.background = None
        self.ambientSound = None
        self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.itemTypes = {
                "Item": Item,
                 "Money": Money,
                 "OxygenPump": OxygenPump,
                 'PressurePlate': PressurePlate,
                 'BareRock': BareRock,
                 'MossyRock': MossyRock
                 }
        self.tilemap = []
        self.loadWorld(level)

    def loadWorld(self, level):
        with open("world.json", "r") as config_file:
            WORLD_CONFIG = json.load(config_file)
            
        # Load tilemap layers
        self.tilemap = WORLD_CONFIG[str(level)]['tiles']
        #self.item_layer = WORLD_CONFIG[str(level)]
        self.entity_layer = WORLD_CONFIG[str(level)]["entities"]
        
        # Generate platforms from tilemap
        print(self.tilemap)
        for key, value in self.tilemap.items(): 
            print(key,value)
        '''            # for x, tile in enumerate(row):
            #     print('tile', x, tile)
            #     if tile == 1:  # Platform tile
            #         print('yay found platform')
            #         platform = Platform(x*TILE_SIZE, y*TILE_SIZE, 
            #                           TILE_SIZE, TILE_SIZE)
            #         self.platforms.add(platform)
        
        # Load items
        # for y, row in enumerate(self.item_layer):
        #     for x, tile in enumerate(row):
        #         if tile == 2:  # Oxygen pump
        #             self.items.add(OxygenPump("oxy", (x*TILE_SIZE, y*TILE_SIZE)))
        #         elif tile == 3:  # Pressure plate
        #             self.items.add(PressurePlate("plate", (x*TILE_SIZE, y*TILE_SIZE)))
        '''
        # Load entities
        self.ast_start = self.entity_layer["astronaut"]["pos"]
        self.alien_start = self.entity_layer["alien"]["pos"]
        





        # self.ast_start = None
        # self.alien_start = None

    #     if load == True:
    #         self.loadWorld(self.level)

    # def loadWorld(self, level):
    #     with open("world.json", "r") as config_file:
    #         WORLD_CONFIG = json.load(config_file)

    #     self.background = pygame.image.load(WORLD_CONFIG[level]["background"])
        
    #     for platform_name, platform_data in WORLD_CONFIG[level]["platforms"].items():
    #         self.platforms.add(Platform(*platform_data, name = platform_name))
            
    #     for item_name, item_data in WORLD_CONFIG[level]["items"].items():
    #         self.items.add(self.itemTypes[WORLD_CONFIG[level]["items"][item_name]["type"]](item_name, WORLD_CONFIG[level]["items"][item_name]["position"]))

    #     self.ast_start = WORLD_CONFIG[level]["astronaut"]["position"]
    #     self.alien_start = WORLD_CONFIG[level]["alien"]["position"]

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


class Item(pygame.sprite.Sprite):
    def __init__(self, id, position=(0, 0)):
        super().__init__()
        self.id = id
        self.position = position
        self.image = pygame.Surface((30, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        self.on_ground = False
        self.velocity_y = 0
        self.static = False

        self.heldBy = None

    def interaction(self, player):
        if len(player.toolbox) < 4:  # Only collect if inventory not full
            player.toolbox.append(self)
            self.kill()  # Remove from world
    
    def draw(self, buffer, camera_offset, camera):
        self.updateRect(camera_offset)
        buffer.blit(self.image, camera.apply(self)) 
           
    def updateRect(self, camera_offset):
        # self.rect.topleft = self.original_position - camera_offset
        pass
       
    def apply_gravity(self):
        x, y = self.position
        if not self.on_ground:
            self.velocity_y += GRAVITY
        y += self.velocity_y
        self.position = (x, y)
        max_velocity = 10
        self.velocity_y = min(self.velocity_y, max_velocity)

    def check_collisions(self, platforms, camera_offset):
        # pygame.draw.rect(BUFFER, (255, 0, 0), self.rect, 2)  # Player collision box
        

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                print("collided at -> ", platform.name, " velocity_y -> ", self.velocity_y, " postion ", self.position)
                
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.standing_on = platform

                elif self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right:
                    if self.position[0] < platform.rect.centerx:  
                        self.rect.right = platform.rect.left
                    elif self.position[0] > platform.rect.centerx:  
                        self.rect.left = platform.rect.right
                    self.rect.y = self.position[1]
                                        
                self.position = self.rect.topleft

    def update(self, platforms, camera_offset):
        if not self.static:
            self.apply_gravity()
            self.check_collisions(platforms, camera_offset)
        elif self.heldBy != None:
            self.position = self.heldBy.rect.topright
        self.check_collisions(platforms, camera_offset)
        self.update_rect()
        
    def update_rect(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.rect.topleft = self.position
    
    def interaction(self):
        print("generic interaction")
    
    def pickup(self, player):
        self.heldBy = player
        self.static = True
        self.velocity_y = 0
        self.on_ground = False
    
    def drop(self):
        self.static = False
        self.heldBy = None
    
class Money(Item):
    def __init__(self, id, position=(0, 0)):
        super().__init__(id, position)
        self.image = pygame.image.load("assets/pouch.png")  
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.type = "money"

    def interaction(self, player):
        if self.heldBy != player:
            self.pickup(player)
        else:
            self.drop()

class OxygenPump(Item):
    def __init__(self, id, position=(0, 0)):
        super().__init__(id, position)
        self.image = pygame.image.load("assets/oxygen_station.png")  
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.type = "money"

        
    def interaction(self, player):
        if player.playerType == "astronaut":
            player.oxygen = 100
            
class BareRock(Item):
    def __init__(self, id, position=(0, 0)):
        super().__init__(id, position)
        self.image = pygame.image.load("assets/bare_rock.png")  
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.weight = 2
        self.type = 'rock'

    def interaction(self, player):
        if self.heldBy != player:
            self.pickup(player)
        else:
            self.drop()
            
class MossyRock(Item):
    def __init__(self, id, position=(0, 0)):
        super().__init__(id, position)
        self.image = pygame.image.load("assets/mossy_rock.png")  
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.weight = 4
        self.type = 'rock'

    def interaction(self, player):
        if self.heldBy != player:
            self.pickup(player)
        else:
            self.drop()
            
class PressurePlate(Item):
    def __init__(self, id, position=(0, 0)):
        super().__init__(id, position)
        self.image = pygame.image.load('assets/pressure_plate.png')
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.weight = 0
        self.type = "money"

    
    def interaction(self, world):
        self.weight = 0
        for item in  world.items:
            if item.type == 'rock':
                if item.rect.centerx >= self.rect.left and item.rect.centerx < self.rect.right:
                    self.weight += item.weight
        print('Current weight =', self.weight)
    



# platforms = pygame.sprite.Group()
# #                       X    Y    L    H
# platforms.add(Platform(0, 380, 1000, 20, name="ground"))
# # Elevated platforms
# platforms.add(Platform(200, 300, 200, 20, name="platform1"))
# platforms.add(Platform(500, 250, 200, 20, name="platform2"))
# platforms.add(Platform(300, 200, 200, 20, name="platform3"))
# platforms.add(Platform(700, 300, 200, 20, name="right_platform"))

# items = pygame.sprite.Group()
# # Place items on platforms
# items.add(Money("money1", (300, 250)))          # On platform1
# items.add(OxygenPump("oxygen1", (550, 200)))    # On platform2
# items.add(Money("money2", (750, 280)))          # On right_platform

# #Setting up Sprites        
# AstrChar = Astronaut(position=(200, 100), keys=ASTR_KEYS)
# AlienChar = Alien(position=(220, 100), keys=ALIEN_KEYS)
 





class Tile:
    def __init__(self, x, y, tile_type, variant):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.variant = variant
        self.rect = pygame.Rect((x * TILE_SIZE)-50, (y * TILE_SIZE)-900, TILE_SIZE, TILE_SIZE)

    def draw(self):
        if self.tile_type == "ground":
            color = GREY
        elif self.tile_type == "pressure_plate":
            color = RED
        else:
            color = (255, 255, 255)  # Default to white

        pygame.draw.rect(BUFFER, color, self.rect)

    def interact(self, player):
        """ Handle interaction with the player (e.g., trigger pressure plate action). """
        if self.tile_type == "pressure_plate":
            print("Player interacted with a pressure plate!")
            # Add behavior specific to the pressure plate, like changing something in the game
            # For example, activating a door or reducing oxygen
            player.oxygen -= 1  # As an example interaction


# Loading tilemap from JSON file
def load_tilemap(data):
    with open(data, "r") as file:
        data = json.load(file)
    
    tiles = []
    for key, tile_info in data["level_1"]["tiles"].items():
        x, y = map(int, key.split(";"))  # Assuming the key is in the format "x;y"
        tile_type = tile_info["type"]
        variant = tile_info["variant"]
        tile = Tile(x, y, tile_type, variant)
        tiles.append(tile)
    return tiles


# Drawing the tilemap
def draw_tilemap(tiles):
    for tile in tiles:
        tile.draw()  # Use the Tile class's draw method to render it



def main_game(level):
    run = True

    world = World(level=level)
    AstrChar = Astronaut(position=world.ast_start, keys=ASTR_KEYS)
    AlienChar = Alien(position=world.alien_start, keys=ALIEN_KEYS)

    clock.tick(FPS)
   
    drawWindow(BUFFER)
    # Game Loop
    pygame.time.set_timer(OXYGEN_DECREASE_EVENT, 1000)

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == OXYGEN_DECREASE_EVENT:
                if AstrChar.oxygen > 9:
                    AstrChar.oxygen -= 1

        BUFFER.fill(WHITE)

        camera_offset = pygame.math.Vector2(0, 0)
        camera_offset = update_camera(AstrChar, camera_offset)

        tiles = load_tilemap("world.json")

        draw_tilemap(tiles)

        player = Player(speed=5)

        player.check_collisions(tilemap=tiles, camera_offset=camera_offset)

        # Draw both characters
        AstrChar.draw(world.platforms, world.items, camera_offset, BUFFER, camera)
        AstrChar.draw_inventory(BUFFER, camera)

        AlienChar.update(world.platforms, world.items, camera_offset)

        BUFFER.blit(AlienChar.image, camera.apply(AlienChar))

        pygame.display.update()
        clock.tick(FPS)

        # BUFFER.fill(WHITE)

        # BUFFER.blit(background, (0,0))
        
        # network = Network()
        # data = network.send(f"{AstrChar.position[0]},{AstrChar.position[1]}")
        # AlienChar.position = [int(val) for val in data.split(",")]
        # print(f'AstrChar.oxygen = {AstrChar.oxygen}')
        if AstrChar.oxygen <= 0:
            print("ASTRO OUT OF OXYGEN!")
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