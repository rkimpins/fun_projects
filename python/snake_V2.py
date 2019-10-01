
# Snake Version 2
# Try implementing better side collision, self collision, and class attributes

from uagame import Window
import pygame, time, random
from pygame.locals import *
import pygame.key


def main():

    window = Window('Pong', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()
class Snake:
    # An object in this class represents a sqaure which is the snakes head
    
    def __init__(self, size, position, color, direction, p_position, max_bodies, window):
        self.size = size
        self.position = position
        self.color = color
        self.window = window
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.direction = direction
        self.p_position = p_position
        self.max_bodies = max_bodies
        for index in range(self.max_bodies):
            self.p_position.append(position)
        
    def draw(self):
        # Draw the snake
        # -self is the snake to draw
        pygame.draw.rect(self.window.get_surface(),self.color, self.rect)
    
    def move(self):
        self.rect.move_ip(self.direction[0], self.direction[1])
        self.p_position.append(self.rect.center)        

class Body:
    
    def __init__(self, size, position, color, number, window):
        self.size = size
        self.position = position
        self.color = color
        self.window = window
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.number = number
    
    def draw(self):
        # Draw this segment of the snake
        # -self is the snake body segment to draw
        pygame.draw.rect(self.window.get_surface(), self.color, self.rect)
        
    def move(self, snake_head):
        self.rect.center = snake_head.p_position[len(snake_head.p_position)-self.number]
        
class Dot():
    # An object in this class represents a dot, or the snakes food/points
    
    def __init__(self, size, center, shift, color, window_size, window):
        self.size = size
        self.center = center
        self.shift = shift
        self.color = color
        self.window_size = window_size
        self.window = window
        self.gap_size = 2*self.shift
    
    def draw(self):
        pygame.draw.circle(self.window.get_surface(), self.color, self.center, self.size) 
    
    def random_pos(self):
        new_x = random.randint(0, self.window_size[0]/self.gap_size)*self.gap_size + self.shift
        new_y = random.randint(0, self.window_size[1]/self.gap_size)*self.gap_size + self.shift
        if new_x and new_y < 30:
            self.random_pos()
        self.center = [new_x, new_y]
        
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
        self.pause_time = 0.1
        pygame.key.set_repeat(20,20)
        self.close_clicked = False
        self.continue_game = True
        self.window_size = (self.window.get_width(), self.window.get_height())
        
        # Scoreboard creation
        position_scoreboard_left = [0,0]
        score = 0
        size = 72
        self.scoreboard_left = Scoreboard(position_scoreboard_left, size, color, score, window)
        
        # Snake creation
        self.size_snake = [10,10]
        self.position_snake = [50,50]
        direction = [self.size_snake[1], 0]
        p_position = []
        self.max_bodies = 100
        self.snake_head = Snake(self.size_snake, self.position_snake, color, direction, p_position, self.max_bodies, window)

        # Dot creation
        self.size_dot = 5
        self.shift_dot = self.size_snake[0]//2
        self.center_dot = [100+self.shift_dot,100+self.shift_dot]
        self.dot = Dot(self.size_dot, self.center_dot, self.shift_dot, color, self.window_size, window)
        self.bodies = []
        for index in range(self.max_bodies):
            self.bodies.append(Body(self.size_snake, self.position_snake, color, index + 1, window))
        
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
        
        # Players moving snake
        if event.type == KEYDOWN and self.continue_game:
            if list_of_keys[K_s] and self.snake_head.direction[1] == 0:
                self.snake_head.direction[0] = 0
                self.snake_head.direction[1] = self.snake_head.size[1]
            if list_of_keys[K_w] and self.snake_head.direction[1] == 0:
                self.snake_head.direction[0] = 0
                self.snake_head.direction[1] = -self.snake_head.size[1]
            if list_of_keys[K_d] and self.snake_head.direction[0] == 0:
                self.snake_head.direction[1] = 0
                self.snake_head.direction[0] = self.snake_head.size[0]
            if list_of_keys[K_a] and self.snake_head.direction[0] == 0:
                self.snake_head.direction[1] = 0
                self.snake_head.direction[0] = -self.snake_head.size[0]
                
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.window.clear()
        self.scoreboard_left.draw()
        self.snake_head.draw()
        counter = 0
        for body in self.bodies:
            if counter <= self.scoreboard_left.score:
                body.draw()
                counter += 1
        self.dot.draw()
        self.window.update()

    def update(self):
        # Update the game objects.
        # - self is the Game to update
        self.snake_head.move()
        for body in self.bodies:
            body.move(self.snake_head)
        #self.body_1.move(self.snake_head)
        #self.body_2.move(self.snake_head)
        
        # Scoring system
        if self.snake_head.rect.collidepoint(self.dot.center[0],self.dot.center[1]):
            self.scoreboard_left.score_point()
            self.dot.random_pos()
        
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        future_center = []
        for index in range(2):            
            future_center.append(self.snake_head.rect.center[index] + self.snake_head.direction[index])
            if future_center[index] < 0 or self.window_size[index] < future_center[index]: 
                self.continue_game = False
    
    
            
main()