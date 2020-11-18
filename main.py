import pygame
from pygame.locals import *
from ball import Ball
from player import Player
import pandas as pd

fps = 60 #fps

screen_w = 600 #screen width
screen_h = 480 #screen height

#Colors 

white = "#ffffff"
lime_green = "#00FF00"
black = "#000000"
light_blue = "#728cd4"

offset = 20 #player screen offset


player_pos_x = screen_w - offset  #player x position
player_pos_y = screen_h/2 #player y position
player_width = 16 #playet width
player_height = 64 #player height

main_player = Player(player_pos_x,player_pos_y, light_blue, player_width, player_height)

ball_pos_x = screen_w/2 #ball x position
ball_pos_y = screen_h/2 #ball y position



main_ball = Ball(ball_pos_x, ball_pos_y, white)


border_color = lime_green
border_size = 20

top_limit = border_size + 1
bottom_limit = screen_h - top_limit - player_height

pygame.init()

delta_time = pygame.time.Clock()

screen_size = (screen_w, screen_h)

screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Fake Pong") 

background = pygame.Surface(screen_size)

pong = pd.read_csv("game.csv") #read file
pong = pong.drop_duplicates() #clean it

X = pong.drop(columns=" player.y")
Y = pong[' player.y']

from sklearn.neighbors import KNeighborsRegressor

clf = KNeighborsRegressor(n_neighbors=3) #nearest neighbors 

clf = clf.fit(X, Y)

df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

def game_loop():

    vy = 0 #y velocity for player
    vx = 0 #x velocity for player


    is_running = True

    #/// Used for data collection///
    #sample = open("game.csv","w")

    #print("ball.x, ball.y, ball.vx, ball.vy, player.y", file=sample)
    #///

    while is_running:

        to_predict = df.append({'x': main_ball.x, 'y' : main_ball.y, 'vx' : main_ball.vx, 'vy' : main_ball.vy}, ignore_index=True)

        should_move =  clf.predict(to_predict)[0] #predicting player.y

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                # Event keys down

                if event.key == pygame.K_ESCAPE:
                    is_running = False
                
                if event.key == pygame.K_r: #restart
                    pass

                # Controles
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    vy = -1
                    vx = 0
                
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    vy = 1
                    vx = 0

            if event.type == pygame.KEYUP:
                #Event keys up

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    vy = 0
                    vx = 0
                
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    vy = 0
                    vx = 0

        #Limit player movment
        if main_player.y <= top_limit: 
            main_player.y = top_limit
        
        elif main_player.y >= bottom_limit:
            main_player.y = bottom_limit
                
        main_player.AI_update(should_move) #comment this if you want to play

        #main_player.update(vx,vy)  #uncomment this if you want to play

        #Ball movments
        if main_ball.x + main_ball.size < border_size + offset + 10:
            main_ball.vx *= -1
        if main_ball.y + main_ball.size < border_size + offset + 10 or main_ball.y + main_ball.size > screen_h - border_size:
            main_ball.vy *= -1

        main_ball.update()

        #File writing data

        #print("{}, {}, {}, {}, {}".format(main_ball.x, main_ball.y, main_ball.vx, main_ball.vy, main_player.y), file=sample)

        background.fill(pygame.Color(black)) #background fill

        #Collision player and ball

        if main_player.x < main_ball.x + main_ball.size and main_player.x + main_player.width > main_ball.x:
            if  main_player.y < main_ball.y + main_ball.size and main_player.y + main_player.height > main_ball.y:
                main_ball.vx = -1


        draw_border()  #drawing border

        draw_player() #drawing player

        draw_ball() #drawing ball

        screen.blit(background, (0, 0)) #placing background

        pygame.display.update() #game update

        delta_time.tick(fps) #setting the fps



def draw_border():
    
    top_border = pygame.draw.rect(background,border_color,(0, 0, screen_w, border_size))
    bottom_border = pygame.draw.rect(background,border_color,(0, screen_h - border_size, screen_w, border_size))
    left_border = pygame.draw.rect(background,border_color,(0, border_size, border_size, screen_h))

def draw_player():
    
    new_player = pygame.draw.rect(background,main_player.color,(main_player.x, main_player.y, main_player.width, main_player.height))

def draw_ball():
    new_ball = pygame.draw.circle(background,main_ball.color,(main_ball.x,main_ball.y),main_ball.size)



game_loop()
