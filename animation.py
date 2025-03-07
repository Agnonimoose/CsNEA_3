import pygame

# Load sprite sheet
sprite_sheet = pygame.image.load("Astronaut-Sheet.png").convert_alpha()

# Function to extract frames from the sprite sheet
def get_frames(sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

idle_frames = get_frames(sprite_sheet, 16, 16, 1)
run_frames = get_frames(sprite_sheet, 16, 16, 4)
jump_frames = get_frames(sprite_sheet, 16, 16, 2)

# Displaying animations
current_frame = 0
clock = pygame.time.Clock()
while True:
    BUFFER.fill((0, 0, 0))
    BUFFER.blit(idle_frames[current_frame], (100, 100))
    current_frame = (current_frame + 1) % len(idle_frames)
    pygame.display.flip()
    clock.tick(10)  
