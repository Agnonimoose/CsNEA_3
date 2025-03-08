import pygame, os
from data.constants import *
from game_objects import *




# class Item(pygame.sprite.Sprite):
#     def __init__(self, id, position=[0, 0]):
#         super().__init__()
#         self.id = id
#         self.position = position
#         self.image = pygame.Surface((30, 80))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = position
        
#         self.on_ground = False
#         self.velocity_y = 0
#         self.velocity_x = 0
#         self.static = False

#         self.heldBy = None

#     def interaction(self, player):
#         if len(player.toolbox) < 4:  # Only collect if inventory not full
#             player.toolbox.append(self)
#             self.kill()  # Remove from world
    
#     def draw(self, buffer, offset):
#         # self.updateRect(camera_offset)
#         # buffer.blit(self.image, camera.apply(self)) 
#         if self.heldBy == None:
#             buffer.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1])) 
           
#     def updateRect(self, camera_offset):
#         # self.rect.topleft = self.original_position - camera_offset
#         pass
       
#     def apply_gravity(self):
#         x, y = self.position
#         if not self.on_ground:
#             self.velocity_y += GRAVITY
#         y += self.velocity_y
#         self.position = [x, y]
#         max_velocity = 10
#         self.velocity_y = min(self.velocity_y, max_velocity)

#     # def check_collisions(self, platforms, camera_offset):
#     #     # pygame.draw.rect(BUFFER, (255, 0, 0), self.rect, 2)  # Player collision box
        

#     #     for platform in platforms:
#     #         if self.rect.colliderect(platform.rect):
#     #             print("collided at -> ", platform.name, " velocity_y -> ", self.velocity_y, " postion ", self.position)
                
#     #             if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
#     #                 self.rect.bottom = platform.rect.top
#     #                 self.velocity_y = 0
#     #                 self.on_ground = True
#     #                 self.standing_on = platform

#     #             elif self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right:
#     #                 if self.position[0] < platform.rect.centerx:  
#     #                     self.rect.right = platform.rect.left
#     #                 elif self.position[0] > platform.rect.centerx:  
#     #                     self.rect.left = platform.rect.right
#     #                 self.rect.y = self.position[1]
                                        
#     #             self.position = self.rect.topleft

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


#     def update(self, world):
#         if not self.heldBy:
#             self.apply_gravity()
#             self.check_collisions(world)
#             self.update_rect()


        
#     def update_rect(self):
#         self.rect.x = self.position[0]
#         self.rect.y = self.position[1]
#         self.rect.topleft = self.position
    
#     def interaction(self):
#         print("generic interaction")
    
#     def pickup(self, player):
#         try:
#             self.heldBy = player
#             self.static = True
#             self.velocity_y = 0
#             self.on_ground = False
#             return self.id
#         except:
#             return None
    
#     def drop(self):
#         self.static = False
#         self.heldBy = None
    
class Item(GameObject):
    def __init__(self, id, position=(0, 0), width=30, height=80):
        super().__init__(position, id, width, height)
        self.id = id
        self.image.fill(RED) 
        self.static = False
        self.heldBy = None

    def interaction(self, player):
        if len(player.toolbox) < 4:  
            player.toolbox.append(self)
            self.kill()  

    def draw(self, buffer, offset):
        if self.heldBy is None:
            buffer.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))

    def update(self, world):
        if not self.heldBy:
            self.apply_gravity()
            self.check_collisions(world)
            self.update_rect()

    def interaction(self):
        print("generic interaction")

    def pickup(self, player):
        try:
            self.heldBy = player
            self.static = True
            self.velocity_y = 0
            self.on_ground = False
            return self.id
        except:
            return None

    def drop(self):
        self.static = False
        self.heldBy = None   
    