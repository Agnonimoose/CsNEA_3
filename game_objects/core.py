import pygame, math
from data.constants import *



class GameObject(pygame.sprite.Sprite):
    def __init__(self, position, id, width=30, height=80):
        super().__init__()
        self.id = id
        self.position = list(position) 
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)  
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY
        self.position[1] += self.velocity_y
        max_velocity = 10
        self.velocity_y = min(self.velocity_y, max_velocity)

    def apply_friction(self):
        if self.velocity_x < 0:
            self.velocity_x += FRIC
        elif self.velocity_x > 0:
            self.velocity_x -= FRIC
        self.position[0] += self.velocity_x

    def check_collisions(self, world):
        # print(f"Object pos: {self.rect.centerx}, {self.rect.centery}")
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

    def update_rect(self):
        self.rect.topleft = self.position

    def check_falling_off(self, world):
        test_rect = self.rect.copy()
        test_rect.y += 1
        self.on_ground = False
        for rect in world.physics_rects_around_rect(self.rect):
            if test_rect.colliderect(rect):
                self.on_ground = True
                break
    
    def getDistance(self, other, this = None):
        if this == None:
            this = self.position
        
        return math.sqrt((this[0] - other[0])**2 + (this[1] - other[1])**2)

