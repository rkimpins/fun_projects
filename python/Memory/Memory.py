# Memory Version 3
# This version is the complete game

from uagame import Window
import pygame, time
from pygame.locals import *
from random import shuffle
import time

# User-defined functions

def main():

    window = Window('Memory', 500, 400)
    window.set_auto_update(False)   
    game = Game(window)
    game.play()
    window.close()

# User-defined classes
class Tile:
    window = None
    size = None
    color = None
    width = None
    image_unflipped = None

    @classmethod
    def set_window(cls, window):
        cls.window = window
        cls.surface = cls.window.get_surface()

    @classmethod
    def set_size(cls, size):
        cls.size = size

    @classmethod
    def set_color(cls, color):
        cls.color = color

    @classmethod
    def set_width(cls, width):
        cls.width = width

    @classmethod
    def set_image_unflipped(cls, image_unflipped):
        cls.image_unflipped = image_unflipped

    def __init__(self, position, image, flipped):
        self.position = position
        self.image = image
        self.flipped = flipped
        self.rect = Rect(position[0], position[1], Tile.size[0], Tile.size[1])
        
    def __eq__(self, other):
        if self.image == other.image:
            return True
        return False
               
    def draw(self):
        if self.flipped:
            Tile.surface.blit(self.image, self.rect)
        else:
            Tile.surface.blit(Tile.image_unflipped, self.rect)
        pygame.draw.rect(Tile.window.get_surface(), Tile.color, self.rect, Tile.width)

    def clicked(self, click_pos):  
        if self.rect.collidepoint(click_pos):
            self.flipped = True
            return True

class Scoreboard:
    #An object in this class represents a complete game.
    def __init__(self, position, color, score, window):
        self.position = position
        self.color = color
        self.score = score
        self.window = window

    def draw(self):
        self.window.draw_string(str(self.score), self.position[0], self.position[1]) 

class Game:
    # An object in this class represents a complete game.

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object

        self.window = window
        self.bg_color = pygame.Color('black')
        self.window.set_font_size(40)
        self.pause_time = 0.0001 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        self.window_size = (self.window.get_width(), self.window.get_height()) 
        self.start_time = time.time()
        self.last_tiles_clicked = []
        # make a random list of images with each occuring twice
        images = []
        self.image_unflipped = pygame.image.load('image0.bmp')
        for image in range(1, 9):
            images.append(pygame.image.load('image'+str(image)+'.bmp'))
        images += images
        shuffle(images)

        tile_height = self.window_size[1]//4
        tile_width = tile_height
        tile_size = [tile_width, tile_height]
        tile_color = pygame.Color('black')
        tile_border_width = 2
        flipped = False

        # make list of position coordinates
        tile_positions = []
        for i in range(4):
            for j in range(4):
                temp_width = tile_width*(j)
                temp_height = tile_height*(i)
                tile_positions.append((temp_width, temp_height))

        # Set Tile class attributes
        Tile.set_window(window)
        Tile.set_size(tile_size)
        Tile.set_color(tile_color)
        Tile.set_width(tile_border_width)
        Tile.set_image_unflipped(self.image_unflipped)

        # create tiles
        self.tiles = []
        for index in range(len(images)):
            self.tiles.append(Tile(tile_positions[index], images[index], flipped))

        # create Scoreboard
        position_scoreboard = [self.window_size[0] - self.window.get_string_width('0'), 0]
        color_scoreboard = pygame.Color('white')
        score = 0
        self.scoreboard = Scoreboard(position_scoreboard, color_scoreboard, score, window)



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
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        elif event.type == MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)

    def handle_mouse_down(self, event):
        click_pos = event.pos
        for tile in self.tiles:
            if tile.clicked(click_pos):
                self.last_tiles_clicked.append(tile)
             
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.window.clear()
        for tile in self.tiles:
            tile.draw()
        self.scoreboard.draw()   
        self.window.update()

    def update(self):
        # Update the game objects.
        # - self is the Game to update

        seconds_passed = int(time.time() - self.start_time)
        self.scoreboard.score = seconds_passed

        self.scoreboard.position[0] = self.window_size[0] - self.window.get_string_width(str(self.scoreboard.score))
        
             
        if len(self.last_tiles_clicked) == 2:
            if id(self.last_tiles_clicked[0]) == id(self.last_tiles_clicked[1]):
                del(self.last_tiles_clicked[1])            
            else:
                if self.last_tiles_clicked[0] != self.last_tiles_clicked[1]:
                    time.sleep(0.5)
                    self.last_tiles_clicked[0].flipped = False
                    self.last_tiles_clicked[1].flipped = False
                self.last_tiles_clicked = []
                
        
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        for tile in self.tiles:
            if not tile.flipped:
                return
        self.continue_game = False

main()
