import pygame
import sys, random, os.path

pygame.init()
window = pygame.display.set_mode((480,850))

clock = pygame.time.Clock()

game_font = pygame.font.Font("04B_19.ttf", 40)

#physics
gravity = 0.25
bird_mov = 0

#scores
score = 0

if not os.path.isfile("highscore.txt"):
    high_score_mem = open('highscore.txt', 'w')
    high_score_mem.write('0')
    high_score = high_score_mem.readline()
    high_score = int(high_score)
    high_score_mem.close()
else:
    high_score_mem = open('highscore.txt', 'r')
    high_score = high_score_mem.readline()
    high_score = int(high_score)
    high_score_mem.close()


background = pygame.image.load('sprites/background-day.png').convert()
background = pygame.transform.scale2x(background)

ground = pygame.image.load('sprites/base.png').convert()
ground = pygame.transform.scale2x(ground)
ground_x = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_img = bird_frames[bird_index]
bird_shape = bird_img.get_rect(center = (100, 325))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_img = pygame.image.load('sprites/pipe-green.png')
pipe_img = pygame.transform.scale2x(pipe_img)
pipes = []
CREATEPIPE = pygame.USEREVENT
pygame.time.set_timer(CREATEPIPE, 1200)
pipe_heights = [400, 500, 600]


game_over = False

def draw_ground():
    window.blit(ground, (ground_x,650))
    window.blit(ground, (ground_x + 480,650))

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_mov * 2, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_shape = new_bird.get_rect(center = (100, bird_shape.centery))
    return new_bird, new_bird_shape

def create_pipe():
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_img.get_rect(midtop = (500, random_height))
    top_pipe = pipe_img.get_rect(midbottom = (500, random_height - 300))
    return bottom_pipe, top_pipe

def pipe_mov(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 780:
            window.blit(pipe_img, pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            window.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_shape.colliderect(pipe):
            return True

    if bird_shape.top <= -100 or bird_shape.bottom >= 650:
        return True

    return False

# def get_score(score):
#     for pipe in pipes:
#         if not bird_shape.colliderect(pipe):
#             score += 1
#     return score

def score_display(game_state):
    if game_state == 'main_game':

        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (240, 100))
        window.blit(score_surface, score_rect)

    if game_state == 'game_over':

        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (240, 100))
        window.blit(score_surface, score_rect)

        game_over_text = game_font.render("Game Over", True, (255,255,255))
        game_over_text_rect = game_over_text.get_rect(center = (240, 400))
        window.blit(game_over_text, game_over_text_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (240, 200))
        window.blit(high_score_surface, high_score_rect)

def update_highscore(score, high_score):
    if score > high_score:
        high_score = score
        high_score_mem = open('highscore.txt', 'w')
        high_score_mem.write(str(int(high_score)))
        high_score_mem.close()
    return high_score



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_mov = 0
                bird_mov -= 10
            if event.key == pygame.K_SPACE and game_over == True:
                game_over = False
                pipes.clear()
                bird_shape.center = (100, 325)
                bird_mov = 0
                score = 0

        if event.type == CREATEPIPE:
            pipes.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_img, bird_shape = bird_animation()

    window.blit(background, (0,-128))

    if not game_over:
        #bird
        bird_mov += gravity
        rotated_bird = rotate_bird(bird_img)
        bird_shape.centery += bird_mov
        window.blit(rotated_bird, bird_shape)
        game_over = check_collision(pipes)

        #pipes
        pipes = pipe_mov(pipes)
        draw_pipes(pipes)

        #score
        score += .008
        score_display('main_game')

    else:
        high_score = update_highscore(score, high_score)
        score_display('game_over')
        
    #ground
    ground_x -= 1
    draw_ground()
    if ground_x <= -480:
        ground_x = 0

    pygame.display.update()
    clock.tick(120)