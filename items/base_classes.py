import pygame, os
RED   = (255, 0, 0)
GRAVITY = 0.5



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
    