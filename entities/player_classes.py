from .base_classes import *
import time

font = pygame.font.Font(None, 24)  # Default font, size 24


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

    def update(self, world, items):
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
        

        self.check_collisions(world)
        self.check_falling_off(world)
        self.apply_gravity()
        self.apply_friction()
        self.update_image()
        self.update_rect()

class Alien(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, phaseAbilityDuration=10, shapeShiftState="default"):
        super().__init__(speed, position, keys)  # calls the player's constructor
        self.playerType = "alien"
        self.phaseAbilityDuration = phaseAbilityDuration 
        self.shapeShiftState = shapeShiftState
        self.image = pygame.image.load("assets/alien_still.png")  
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def phaseThroughWalls(self):
        pass

    def shapeShift(self):
        pass

class Astronaut(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, oxygenLevel=100, toolbox=None, currentEnvironment="space_station"):
        super().__init__(speed, position, keys) 
        self.playerType = "astronaut"
        self.baseSpeed = speed 
        self.oxygenLevel = oxygenLevel     
        self.toolbox = toolbox if toolbox is not None else []  
        self.currentEnvironment = currentEnvironment  
        self.rfid_use = False 
        self.rfid_detectable = []  
        self.lastDepletionTime = time.time()
        
        self.show_inventory = False
        self.inventory_open = False
        self.inventory_size = 4  
        self.selected_slot = 0

        self.image = pygame.image.load("assets/astronaut_still.png")
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.original_image = self.image.copy()

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
        
    def draw_inventory(self, buffer, offset):
        if self.show_inventory:

            
            # Inventory panel dimensions
            panel_width = 150
            panel_height = 50
            slot_size = 32
            
            # Position above player's head
            # inv_x = self.rect.x - panel_width//2 + self.rect.width//2
            # inv_y = self.rect.y - panel_height - 20
            
            inv_x = self.rect.x - offset[0] - panel_width//2 + self.rect.width//2
            inv_y = self.rect.y - offset[1] - panel_height - 20
            
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


    def draw(self, world, items, offset, BUFFER):
        self.update(world, items)
        
        
        BUFFER.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))

        # ox_bar_x = screen_pos.x + (self.rect.width - self.oxygen_bar_width) // 2
        # ox_bar_y = screen_pos.y - 10 
        ox_bar_x = self.rect.x - offset[0] + (self.rect.width - self.oxygen_bar_width) // 2
        ox_bar_y = self.rect.y - offset[1] - 10 
         
        pygame.draw.rect(BUFFER, GREY, (ox_bar_x, ox_bar_y, self.oxygen_bar_width, self.oxygen_bar_height), border_radius=5)
        pygame.draw.rect(BUFFER, DARK_BLUE, (ox_bar_x, ox_bar_y, self.oxygen_bar_width * (self.oxygen / self.oxygen_max), self.oxygen_bar_height), border_radius=5)

        ox_text = f"Oxygen: {self.oxygen}/{self.oxygen_max}"
        ox_text_surface = font.render(ox_text, True, BLACK)  
        ox_text_x = ox_bar_x + (self.oxygen_bar_width - ox_text_surface.get_width()) // 2
        ox_text_y = ox_bar_y - 15  
        # BUFFER.blit(ox_text_surface, (ox_text_x, ox_text_y))

        hp_bar_x = self.rect.x - offset[0] + (self.rect.width - self.hp_bar_width) // 2
        hp_bar_y = self.rect.y - offset[1] - 20 
        pygame.draw.rect(BUFFER, RED, (hp_bar_x, hp_bar_y, self.hp_bar_width, self.hp_bar_height), border_radius=5)
        pygame.draw.rect(BUFFER, GREEN, (hp_bar_x, hp_bar_y, self.hp_bar_width * (self.player_hp / self.player_max_hp), self.hp_bar_height), border_radius=5)

        hp_text = f"HP: {self.player_hp}/{self.player_max_hp}"
        text_surface = font.render(hp_text, True, BLACK)  
        text_x = hp_bar_x + (self.hp_bar_width - text_surface.get_width()) // 2
        text_y = hp_bar_y - 15  
        # BUFFER.blit(text_surface, (text_x, text_y))
        
        # pygame.draw.rect(BUFFER, RED, (self.rect.x - offset[0], self.rect.y - offset[1], self.rect.width, self.rect.height), 5)
