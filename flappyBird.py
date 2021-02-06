import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    score_surface = game_font.render(str(score),True,(255,255,255))
    score_rect = score_surface.get_rect(center = (288,100))
    screen.blit(score_surface,score_rect)

pygame.init()    #  initialise pygame
screen = pygame.display.set_mode((576, 1024))   # on initialise la taille de l'écran de jeu, la display surface
clock = pygame.time.Clock()  # pour definr la frame
fnt = "FlappybirdyRegular-KaBW.ttf"
game_font = pygame.font.Font(fnt, 40)
# Game variable
gravity = 0.25   # pour que l'oiseau tombe il faut lui appliqué le principe de gravité
bird_movement = 0
game_active = True
score = 0
high_score = 0

# backgroung image
bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()    # on charge l'arrière plan du jeu
bg_surface = pygame.transform.scale2x(bg_surface)        # cette methode multiplie la taille de l'image par 2 pour l'adapté a la taille de la display surface

# floor image
floor_surface = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# bird image

bird_downflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
# bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100,512))

# pipe image
pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT # event trigger by timer
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

while True: # on définie la boucle de jeu
    for  event in pygame.event.get(): # loop pour quiter le jeu et fermer la fenetre
        if event.type == pygame.QUIT: #fermer pygame
            pygame.quit()
            sys.exit() #pour s'assurer que le jeu arrete de tourner en arrière plan , ne pas oublier d'import sys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface , bird_rect = bird_animation()

    # on affiche la surface du bg sur la display surface avec la methode blit()
    screen.blit(bg_surface,(0,0))

    if game_active:
        # Birds movements
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        # pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score_display()

    #floor
    floor_x_pos -= 1   #la position x du sol est icrementé a chaque loop de wihle ce qui fais avancer le sol
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0



    pygame.display.update()
    clock.tick(120)   # nombre de frame pour le jeu

# todo finir le score et le highe score