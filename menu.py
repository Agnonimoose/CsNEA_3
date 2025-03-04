import pygame  
import sys  

pygame.init()  

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BUFFER = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.scale(pygame.image.load("assets/statebg.png"), 
                                   (SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 70 

# making text
smallfont = pygame.font.SysFont('Corbel',35)  
text = smallfont.render('quit' , True , WHITE) 

# button text 
play_text = smallfont.render('Play', True, WHITE)
quit_text = smallfont.render('Quit', True, WHITE)


def menu():
    while True:
        BUFFER.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
                button_y = (SCREEN_HEIGHT - (3 * BUTTON_SPACING)) // 2  
                
                if button_x <= mouse[0] <= button_x + BUTTON_WIDTH and button_y <= mouse[1] <= button_y + BUTTON_HEIGHT:
                    return "play"  

                if button_x <= mouse[0] <= button_x + BUTTON_WIDTH and button_y + BUTTON_SPACING <= mouse[1] <= button_y + BUTTON_SPACING + BUTTON_HEIGHT:
                    pygame.quit()
                    sys.exit()

        mouse = pygame.mouse.get_pos()

        button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        button_y = (SCREEN_HEIGHT - (3 * BUTTON_SPACING)) // 2  

        buttons = [
            ("Play", button_y),
            ("Quit", button_y + BUTTON_SPACING),
        ]

        for text, y in buttons:
            if button_x <= mouse[0] <= button_x + BUTTON_WIDTH and y <= mouse[1] <= y + BUTTON_HEIGHT:
                pygame.draw.rect(BUFFER, color_light, [button_x, y, BUTTON_WIDTH, BUTTON_HEIGHT])
            else:
                pygame.draw.rect(BUFFER, color_dark, [button_x, y, BUTTON_WIDTH, BUTTON_HEIGHT])

            text_surface = smallfont.render(text, True, WHITE)
            text_x = button_x + (BUTTON_WIDTH - text_surface.get_width()) // 2
            text_y = y + (BUTTON_HEIGHT - text_surface.get_height()) // 2
            BUFFER.blit(text_surface, (text_x, text_y))

        pygame.display.update()