# Pong version 3

from uagame import Window
import pygame, time
from pygame.locals import *
import pygame.key


def main():

    window = Window('Pong', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()
    
class Scoreboard:
    # An object in this class represents a score keeping scoreboard
    
    def __init__(self, position, size, color, score, window):
        self.position = position
        self.size = size
        self.color = color
        self.score = score
        self.window = window
        
    def draw(self):
        self.window.draw_string(str(self.score), self.position[0], self.position[1])
    
    def score_point(self):
        self.score += 1

class Paddle:
    # An object in this class represents a colored rectangle
    
    def __init__(self, size, position, color, paddle_speed, window):
        self.size = size
        self.position = position
        self.color = color
        self.window = window
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.paddle_speed = paddle_speed
    
    def draw(self):
        # Draw the paddle
        # -self is the paddle to draw
        pygame.draw.rect(self.window.get_surface(), self.color, self.rect)
        self.position[1] = self.rect[1]
    
    def move_up(self):
        self.rect.move_ip(0,-self.paddle_speed)
        
    def move_down(self):
        self.rect.move_ip(0,self.paddle_speed)
class Ball:
    # An object in this class represents a colored circle.

    def __init__(self, center, radius, color, window, velocity):
        # Initialize a Ball.
        # - self is the Ball to initialize
        # - center is a list containing the x and y int
        # coords of the center of the Ball
        # - radius is the int pixel radius of the Ball
        # - color is the pygame.Color of the Ball
        # - window is the uagame window object

        self.center = center
        self.radius = radius
        self.color = color
        self.window = window
        self.velocity = velocity
        
    def draw(self):
        # Draw the Ball.
        # - self is the Ball to draw
        pygame.draw.circle(self.window.get_surface(), self.color, self.center, self.radius)

    def move(self):
        # Move the Ball.
        # - self is the Ball to move
        for index in range(0, 2):
            self.center[index] = (self.center[index] + self.velocity[index])        
        
            

class Game:
    # An object in this class represents a complete game.

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object

        self.window = window
        self.bg_color = pygame.Color('black')
        color = pygame.Color("white")
        self.window.set_font_size(72)
        self.pause_time = 0.04 # smaller is faster game
        pygame.key.set_repeat(20,20)
        self.close_clicked = False
        self.continue_game = True
        self.window_size = (self.window.get_width(), self.window.get_height())
        position_ball = [200,200]
        self.velocity = [10,3]
        self.ball_size = 4
        self.ball = Ball(position_ball, self.ball_size, color, window, self.velocity)
        
        self.size_paddle = (10,40)
        position_paddle_1 = [50, self.window.get_height() // 2 - self.size_paddle[1]//2]
        position_paddle_2 = [self.window.get_width()-60, self.window.get_height() // 2 - self.size_paddle[1]//2]
        self.paddle_speed = 10
        self.paddle_1 = Paddle(self.size_paddle, position_paddle_1, color, self.paddle_speed, window)
        self.paddle_2 = Paddle(self.size_paddle, position_paddle_2, color, self.paddle_speed, window)
        
        position_scoreboard_left = [0,0]
        position_scoreboard_right = [self.window.get_width() - self.window.get_string_width('0'), 0]
        score = 0
        size = 72
        self.scoreboard_left = Scoreboard(position_scoreboard_left, size, color, score, window)
        self.scoreboard_right = Scoreboard(position_scoreboard_right, size, color, score, window)
        
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) # set game velocity by pausing

    def handle_event(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
        list_of_keys = pygame.key.get_pressed()
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        
        # Players moving paddles
        if event.type == KEYDOWN and self.continue_game:
            if list_of_keys[K_a]:
                if self.paddle_1.rect[1] + self.size_paddle[1] < self.window_size[1]:
                    self.paddle_1.move_down()
            if list_of_keys[K_q]:
                if self.paddle_1.rect[1] > 0:
                    self.paddle_1.move_up()
            if list_of_keys[K_l]:
                if self.paddle_2.rect[1] + self.size_paddle[1] < self.window_size[1]:
                    self.paddle_2.move_down()
            if list_of_keys[K_p]:
                if self.paddle_2.rect[1] > 0:
                    self.paddle_2.move_up()            
            
        
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.window.clear()
        self.ball.draw()
        self.paddle_1.draw()
        self.paddle_2.draw()
        self.scoreboard_right.draw()
        self.scoreboard_left.draw()
        if not self.continue_game:
            pass
        self.window.update()

    def update(self):
        # Update the game objects.
        # - self is the Game to update
        self.ball.move()
        self.check_bounce()
       
        # Scoring system
        if self.ball.center[0] > self.window_size[0] - self.ball_size:
            self.scoreboard_left.score_point()
        if self.ball.center[0] < self.ball_size:
            self.scoreboard_right.score_point()        
        if self.scoreboard_right.score == 10:
            self.scoreboard_right.position[0] = self.window_size[0] - self.window.get_string_width('10')
        
            
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        if self.scoreboard_left.score == 11:
            self.continue_game = False
        if self.scoreboard_right.score == 11:
            self.continue_game = False
    
    def check_bounce(self):
        # Check if the ball needs to bounce off the paddle, then change velocity accordingly
        for index in range(0, 2):       
            # Bouncing off edges
            if self.ball.center[index] >= self.window_size[index] or self.ball.center[index] <= 0:
                self.ball.velocity[index] = -self.ball.velocity[index]
            
            # Bouncing off left paddle
            if self.paddle_1.position[0] + self.size_paddle[0] + self.velocity[0] <= self.ball.center[0] <= self.paddle_1.position[0] + self.size_paddle[0]:
                if self.paddle_1.position[1] <= self.ball.center[1] <= self.paddle_1.position[1] + self.size_paddle[1]:
                    if self.velocity[0] < 0:
                        self.velocity[0] = self.velocity[0] * -1
            # Bouncing off right paddle
            if self.paddle_2.position[0] <= self.ball.center[0] <= self.paddle_2.position[0] + self.velocity[0]:
                if self.paddle_2.position[1] <= self.ball.center[1] <= self.paddle_2.position[1] + self.size_paddle[1]:
                    if self.velocity[0] > 0:
                        self.velocity[0] = self.velocity[0] * -1                        

main()


