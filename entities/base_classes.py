import pygame, json, math
from pygame.locals import *
from data.constants import *
from game_objects import *

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

# class Character(pygame.sprite.Sprite):
#     def __init__(self, characterType, position=[0, 0]):
#         self.position = position  # (x, y) coordinates of the players
#         self.speed = CHARACTER_CONFIG.get(characterType, {}).get("speed", 5) # movement speed
#         self.velocity_y = 0
#         self.velocity_x = 0
#         self.characterType = characterType

#         self.sprite_sheet = None
#         self.frame_width = 0
#         self.frame_height = 0
#         self.animation_frames = None
#         self.current_frame = 0
#         self.walking_animation_speed = 0
#         self.frame_count = 0
        
#         self.image = pygame.Surface((30, 80))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = position
#         self.direction = "right" 
#         self.original_image = self.image.copy()
        
        
        
        
#         self.jumping = False
#         self.on_ground = False
#         self.rect_checker = None

#     def slice_sprite_sheet(self):
#         frames = []
#         num_frames = self.sprite_sheet.get_width() // self.frame_width
#         for i in range(num_frames):
#             frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
#             frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
#             frames.append(frame)
#         return frames

#     def move(self, direction):
#         x, y = self.position
#         if direction == "none":
#             return
#         elif direction == 'up':
#             self.jump()
#         else:
#             if direction == 'down':
#                 y -= self.speed
#             elif direction == 'left':
#                 self.velocity_x -= self.speed
#                 self.direction = "left"
#                 if self.velocity_x < -10:
#                     self.velocity_x = -10
#             elif direction == 'right':
#                 self.velocity_x += self.speed
#                 if self.velocity_x > 10:
#                     self.velocity_x = 10
#                 self.direction = "right"
                    
#     def jump(self):
#         if self.on_ground == True:
#             self.velocity_y = -10
#             self.on_ground = False

#     def apply_gravity(self):
#         x, y = self.position
#         if not self.on_ground:
#             self.velocity_y += GRAVITY
#         y += self.velocity_y
#         self.position = [x, y]
#         max_velocity = 10
#         self.velocity_y = min(self.velocity_y, max_velocity)

#     def apply_friction(self):
#         x, y = self.position
#         if self.velocity_x < 0:
#             self.velocity_x += FRIC
#         elif self.velocity_x > 0:
#             self.velocity_x -= FRIC
#         x += self.velocity_x
#         self.position = [x, y]

#     def check_collisions(self, world):
#         self.collisions = {'up': False, 'down': False,
#                     'right': False, 'left': False}
        
#         # print(f"Character pos: {self.rect.centerx}, {self.rect.centery}")
#         entity_rect_x = self.rect.copy()
#         entity_rect_x.x += self.velocity_x
        
#         for rect in world.physics_rects_around_rect(self.rect):
#             # print("CHECKING RECT X RECT!")
#             if entity_rect_x.colliderect(rect):
#                 # print("x collision found")
#                 if self.velocity_x > 0:
#                     entity_rect_x.right = rect.left
#                     self.collisions['right'] = True
#                     self.velocity_x = 0
#                 if self.velocity_x < 0:
#                     entity_rect_x.left = rect.right
#                     self.collisions['left'] = True
#                     self.velocity_x = 0
#                 self.position[0] = entity_rect_x.x
                
#         # entity_rect = self.rect.copy()
#         entity_rect_y = self.rect.copy()
#         entity_rect_y.y += self.velocity_y


            
#         for rect in world.physics_rects_around_rect(self.rect):
#             # print("CHECKING RECT Y RECT!")
#             if entity_rect_y.colliderect(rect):
#                 # print("y collision found!")
#                 if self.velocity_y > 0:
#                     entity_rect_y.bottom = rect.top
#                     self.collisions['down'] = True
#                     self.velocity_y = 0
#                     self.on_ground = True
#                 if self.velocity_y < 0:
#                     entity_rect_y.top = rect.bottom
#                     self.collisions['up'] = True
#                     self.velocity_y = 0
#                 self.position[1] = entity_rect_y.y
               
#     def check_falling_off(self, world):
#         test_rect = self.rect.copy()
#         test_rect.y += 1 #test one pixel below the player.
#         self.on_ground = False
#         for rect in world.physics_rects_around_rect(self.rect):
#             if test_rect.colliderect(rect):
#                 self.on_ground = True
#                 break

#     def update_rect(self):
#         self.rect.x = self.position[0]
#         self.rect.y = self.position[1]
    
#     def animate(self):
#         print("animating! -> frame_count = ", self.frame_count, " len(self.animation_frames) -> ", len(self.animation_frames))
#         self.frame_count += 1
#         if self.frame_count >= 60 // self.walking_animation_speed:
#             self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
#             self.original_image = self.animation_frames[self.current_frame]
#             self.original_image = pygame.transform.scale(self.original_image, (30,40))
#             self.frame_count = 0
    
#     def update_image(self):
#         if self.velocity_x == 0:
#             self.current_frame = 0
#             self.original_image = self.animation_frames[self.current_frame]
#             self.original_image = pygame.transform.scale(self.image, (30,40))
#         else:
#             self.animate()
            
#         if self.direction == "left":
#             # self.animate()
#             self.image = pygame.transform.flip(self.original_image, True, False) 
#         else:
#             self.image = self.original_image.copy()  
    
#     def getDistance(self, other, this = None):
#         if this == None:
#             this = self.position
        
#         return math.sqrt((this[0] - other[0])**2 + (this[1] - other[1])**2)



class Character(GameObject):
    def __init__(self, characterType, id, position=(0, 0), width=30, height=80):
        super().__init__(position, id, width, height)
        self.characterType = characterType
        self.speed = CHARACTER_CONFIG.get(characterType, {}).get("speed", 5)
        self.direction = "right"
        self.original_image = self.image.copy()

        self.sprite_sheet = None
        self.frame_width = 0
        self.frame_height = 0
        self.animation_frames = None
        self.current_frame = 0
        self.walking_animation_speed = 0
        self.frame_count = 0

        self.jumping = False
        self.rect_checker = None

    def slice_sprite_sheet(self):
        frames = []
        num_frames = self.sprite_sheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def move(self, direction):
        if direction == "none":
            return
        elif direction == 'up':
            self.jump()
        else:
            if direction == 'down':
                self.position[1] -= self.speed
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
        if self.on_ground:
            self.velocity_y = -10

    def apply_friction(self):
        if self.velocity_x < 0:
            self.velocity_x += FRIC
        elif self.velocity_x > 0:
            self.velocity_x -= FRIC
        self.position[0] += self.velocity_x

    def update(self, world):
        self.apply_gravity()
        self.check_collisions(world)
        self.update_rect()

    def animate(self):
        self.frame_count += 1
        if self.frame_count >= 60 // self.walking_animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.original_image = self.animation_frames[self.current_frame]
            self.original_image = pygame.transform.scale(self.original_image, (30, 40))
            self.frame_count = 0

    def update_image(self):
        if self.velocity_x == 0:
            self.current_frame = 0
            self.original_image = self.animation_frames[self.current_frame]
            self.original_image = pygame.transform.scale(self.image, (30, 40))
        else:
            self.animate()

        if self.direction == "left":
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image.copy()
        