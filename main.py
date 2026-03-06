import pygame
import sys
import random

speed = 10

# window size
frame_size_x = 720
frame_size_y = 480

check_error = pygame.init()

if check_error[1] > 0:
    print(f"Errors {check_error[1]}")
else:
    print("Game Successfully init")

# init game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# color
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

fps_controller = pygame.time.Clock()

# one snake body block
square_size = 20

game_state = "START"
snake_dead = False


def start_screen():

    game_window.fill(black)

    title_font = pygame.font.SysFont("consolas",50)
    text_font = pygame.font.SysFont("consolas",20)

    title = title_font.render("Snake Game",True,green)
    text = text_font.render("Press SPACE to Start",True,white)

    game_window.blit(title,title.get_rect(center=(frame_size_x/2,frame_size_y/3)))
    game_window.blit(text,text.get_rect(center=(frame_size_x/2,frame_size_y/2)))

    pygame.display.update()


def game_over_screen():

    # dark overlay
    overlay = pygame.Surface((frame_size_x,frame_size_y))
    overlay.set_alpha(150)
    overlay.fill((0,0,0))
    game_window.blit(overlay,(0,0))

    font_big = pygame.font.SysFont("consolas",50)
    font_small = pygame.font.SysFont("consolas",20)

    over = font_big.render("GAME OVER",True,red)
    score_text = font_small.render("Score : "+str(score),True,white)

    restart = font_small.render("Press R to Restart | Q to Quit",True,white)

    game_window.blit(over,over.get_rect(center=(frame_size_x/2,frame_size_y/3)))
    game_window.blit(score_text,score_text.get_rect(center=(frame_size_x/2,frame_size_y/2)))
    game_window.blit(restart,restart.get_rect(center=(frame_size_x/2,frame_size_y/1.5)))

    pygame.display.update()


def init_vars():

    global head_pos, snake_body, food_pos, food_spawn
    global score, direction, speed, snake_dead

    direction = "RIGHT"

    # snake head start
    head_pos = [120,60]

    snake_body = [
        [120,60],
        [100,60],
        [80,60]
    ]

    score = 0
    speed = 10
    snake_dead = False

    food_spawn = True

    spawn_food()


# spawn food not on snake
def spawn_food():

    global food_pos

    while True:

        food_pos = [
            random.randrange(1,(frame_size_x//square_size))*square_size,
            random.randrange(1,(frame_size_y//square_size))*square_size
        ]

        if food_pos not in snake_body:
            break


init_vars()


def show_score(choice,color,font,size):

    score_font = pygame.font.SysFont(font,size)

    score_surface = score_font.render("Score : "+str(score),True,color)

    score_rect = score_surface.get_rect()

    if choice == 1:
        score_rect.midtop = (frame_size_x/10,15)
    else:
        score_rect.midtop = (frame_size_x/2,frame_size_y/1.25)

    game_window.blit(score_surface,score_rect)


# game loop
while True:


    # start screen
    if game_state == "START":

        start_screen()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    init_vars()
                    game_state = "PLAY"

        continue


    # game over screen
    if game_state == "GAME_OVER":

        game_over_screen()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    init_vars()
                    game_state = "PLAY"

                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        continue


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if ((event.key == pygame.K_UP or event.key == ord("w")) and direction != "DOWN"):
                direction = "UP"

            elif ((event.key == pygame.K_DOWN or event.key == ord("s")) and direction != "UP"):
                direction = "DOWN"

            elif ((event.key == pygame.K_LEFT or event.key == ord("a")) and direction != "RIGHT"):
                direction = "LEFT"

            elif ((event.key == pygame.K_RIGHT or event.key == ord("d")) and direction != "LEFT"):
                direction = "RIGHT"


    # moving / distance
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size


    # wall wrap
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size:
        head_pos[1] = 0


    # eating apple
    snake_body.insert(0,list(head_pos))

    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:

        score += 1

        # speed increase
        speed += score*0.1 if score < 10 else 0

        food_spawn = False

    else:
        snake_body.pop()


    # spawn food
    if not food_spawn:

        spawn_food()

        food_spawn = True


    # gfx
    game_window.fill(black)

    snake_color = blue if snake_dead else green

    for pos in snake_body:

        pygame.draw.rect(
            game_window,
            snake_color,
            pygame.Rect(
                pos[0]+2,
                pos[1]+2,
                square_size-2,
                square_size-2
            )
        )

    pygame.draw.rect(
        game_window,
        red,
        pygame.Rect(
            food_pos[0],
            food_pos[1],
            square_size,
            square_size
        )
    )


    # game end condition
    for block in snake_body[1:]:

        if head_pos == block:

            snake_dead = True
            game_state = "GAME_OVER"


    show_score(1,white,'consolas',20)

    pygame.display.update()

    fps_controller.tick(speed)