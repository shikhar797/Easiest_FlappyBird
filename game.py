#importing all the modules
import pygame
import random
from random import choice
from os.path import join
import math

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snail Jump")
favicon = pygame.image.load(join('images', 'bluebird-downflap.png')).convert_alpha()
pygame.display.set_icon(favicon)

# Player class for moving the bird 
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'bluebird-downflap.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))
        self.gravity = 0

    def jump(self):
        keys = pygame.key.get_pressed()
        flap_sound.play()
        if keys[pygame.K_SPACE]:
            self.gravity = -10  # Apply upward force when space is pressed
        # elif pygame.mouse.get_just_pressed():
        #         self.gravity = -10
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
            self.gravity = -10

    def reset(self):
        # Reset the player's position and gravity
        self.rect.center = (window_width / 2, window_height / 2)
        self.gravity = 0
        
    def apply_gravity(self):
        self.gravity += 1  # Gravity effect (fall down)
        self.rect.y += self.gravity  # Update position with gravity

  
    def update(self):
        
        self.jump()
        self.apply_gravity()
        
#Pipe class to display [pipe] in the game
class Pipe(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=pygame.image.load(join('images', 'pipe-red.png')).convert_alpha()
        self.image=pygame.transform.scale(self.image,(self.image.width,self.image.height*2))
        self.rect=self.image.get_frect(center=pos)
        if self.rect.top<0:
            self.image=pygame.transform.rotate(self.image,180)
    
    def update(self):
        self.rect.x-=5
        if self.rect.right < 0:
            self.kill()
# Infinite scrolling background setup
tiles = 3
scroll = 0

# all the imports for game
start_btn = pygame.image.load(join('images', 'start_btn.png')).convert_alpha()
start_rect = start_btn.get_rect(center=(window_width / 2, window_height / 2))
bg_surf = pygame.image.load(join('images', 'background-day.png')).convert_alpha()
bg_surf = pygame.transform.scale(bg_surf, (window_width / 2, window_height))
game_restart = pygame.image.load(join('images', 'restart.png')).convert_alpha()
flap_sound=pygame.mixer.Sound(join('sounds','flap.mp3'))
flap_sound.set_volume(0.02)
hit_sound=pygame.mixer.Sound(join('sounds','hit.wav'))

#pipe event 
pipe_event=pygame.event.custom_type()
pygame.time.set_timer(pipe_event,400)

# Sprite group setup
all_sprites = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()
# Create player sprite and pipe sprites
player = Player(all_sprites)
pipe=Pipe((0,0,),(all_sprites,pipe_sprites))

# Start screen function
def start(start_btn, start_rect):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    return True
        
        # Drawing the restart button
        screen.fill('orange')
        screen.blit(start_btn, start_rect)
        pygame.display.update()

# Game over screen
def GameOver():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Exit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                game_restart_rect = game_restart.get_rect(center=(window_width / 2, window_height / 2))
                if game_restart_rect.collidepoint(mousePos):
                    return True   # Restart the game loop

        # Drawing the restart button
        screen.fill('red')
        game_restart_rect = game_restart.get_rect(center=(window_width / 2, window_height / 2))
        screen.blit(game_restart, game_restart_rect)
        pygame.display.update()

# def display_score():
#         font=pygame.font.Font(None,120)
#         font_surf=font.render(str(math.ceil((pygame.time.get_ticks())/1000)),True,(240,240,240))
#         font_rect=font_surf.get_frect(midbottom=(window_width/2,window_height-50))
#         pygame.draw.rect(screen,'grey',font_rect.inflate(20,20),1,1)
#         screen.blit(font_surf,font_rect)
#         pygame.display.update()  

# Main game loop
running = start(start_btn, start_rect)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pipe_event:
            x = window_width + random.randint(0, 100)  # Start from just off the right edge of the screen
            y = random.choice((random.randint(-100,0),random.randint(window_height,window_height+100)))
            Pipe((x,y),(all_sprites,pipe_sprites))  
        
        # Check if player is out of bounds (game over) and Call GameOver, which may reset or end the game
        if player.rect.y > window_height or player.rect.y < 0:
           running = GameOver()  
           start_time=pygame.time.get_ticks()/1000  
           player.reset()
        #check for the collision
        elif pygame.sprite.spritecollideany(player, pipe_sprites):
               hit_sound.play() 
               running = GameOver()   
               player.reset()

    # Infinite scrolling background
    for i in range(0, tiles):
        screen.blit(bg_surf, (i * window_width / 2 + scroll, 0))
    scroll -= 5
    if abs(scroll) > window_width / 2:
        scroll = 0

    # Update and draw all sprites
    start_time=pygame.time.get_ticks()/1000
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()
