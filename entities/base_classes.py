import pygame, json, math
from pygame.locals import *
from data.constants import *

with open("data/character_config.json", "r") as config_file:
    CHARACTER_CONFIG = json.load(config_file)
    
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
0

class Character(pygame.sprite.Sprite):
    def __init__(self, characterType, position=[0, 0]):
        self.position = position  # (x, y) coordinates of the players
        self.speed = CHARACTER_CONFIG.get(characterType, {}).get("speed", 5) # movement speed
        self.velocity_y = 0
        self.velocity_x = 0
        self.characterType = characterType

        self.image = pygame.Surface((30, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.direction = "right" 
        self.original_image = self.image.copy()
        
        self.jumping = False
        self.on_ground = False
        self.rect_checker = None

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
                self.velocity_x -= self.speed
                self.direction = "left"
                if self.velocity_x < -10:
                    self.velocity_x = -10
            elif direction == 'right':
                self.velocity_x += self.speed
                if self.velocity_x > 10:
                    self.velocity_x = 10
                self.direction = "right"
                    


    def jump(self):
        # print("jumping -> self.jumping ", self.jumping, " self.on_ground -> ", self.on_ground)
        # if (self.jumping == False ) and (self.on_ground == True):
        #     self.jumping = True
        # print(f"jumping! self.on_ground = {self.on_ground}")
        if self.on_ground == True:
            # print(f"negging velo {self.velocity_y}")
            self.velocity_y = -10
            self.on_ground = False

    def apply_gravity(self):
        x, y = self.position
        if not self.on_ground:
            self.velocity_y += GRAVITY
        y += self.velocity_y
        self.position = [x, y]
        max_velocity = 10
        self.velocity_y = min(self.velocity_y, max_velocity)

    def apply_friction(self):
        x, y = self.position
        if self.velocity_x < 0:
            self.velocity_x += FRIC
        elif self.velocity_x > 0:
            self.velocity_x -= FRIC
        x += self.velocity_x
        self.position = [x, y]


    def check_collisions(self, world):
        self.collisions = {'up': False, 'down': False,
                    'right': False, 'left': False}
        
        # print(f"Character pos: {self.rect.centerx}, {self.rect.centery}")
        entity_rect_x = self.rect.copy()
        entity_rect_x.x += self.velocity_x
        
        for rect in world.physics_rects_around_rect(self.rect):
            # print("CHECKING RECT X RECT!")
            if entity_rect_x.colliderect(rect):
                # print("x collision found")
                if self.velocity_x > 0:
                    entity_rect_x.right = rect.left
                    self.collisions['right'] = True
                    self.velocity_x = 0
                if self.velocity_x < 0:
                    entity_rect_x.left = rect.right
                    self.collisions['left'] = True
                    self.velocity_x = 0
                self.position[0] = entity_rect_x.x
                
        # entity_rect = self.rect.copy()
        entity_rect_y = self.rect.copy()
        entity_rect_y.y += self.velocity_y


            
        for rect in world.physics_rects_around_rect(self.rect):
            # print("CHECKING RECT Y RECT!")
            if entity_rect_y.colliderect(rect):
                # print("y collision found!")
                if self.velocity_y > 0:
                    entity_rect_y.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity_y = 0
                    self.on_ground = True
                if self.velocity_y < 0:
                    entity_rect_y.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity_y = 0
                self.position[1] = entity_rect_y.y


                    
    def check_falling_off(self, world):
        test_rect = self.rect.copy()
        test_rect.y += 1 #test one pixel below the player.
        self.on_ground = False
        for rect in world.physics_rects_around_rect(self.rect):
            if test_rect.colliderect(rect):
                self.on_ground = True
                break

    def update_rect(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
    def update_image(self):
        if self.direction == "left":
            self.image = pygame.transform.flip(self.original_image, True, False)  # Flip horizontally
        else:
            self.image = self.original_image.copy()  
    
    def getDistance(self, other, this = None):
        if this == None:
            this = self.position
        
        return math.sqrt((this[0] - other[0])**2 + (this[1] - other[1])**2)




        