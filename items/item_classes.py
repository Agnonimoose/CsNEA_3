from .base_classes import *

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
    
