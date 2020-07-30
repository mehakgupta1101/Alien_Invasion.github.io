import pygame
from pygame.sprite import Sprite #importing sprite from pygame.sprite module

class Bullet(Sprite): #creating a bullet child class inherited from parent class sprite
    """A class to manage bullets fired from the ship"""

    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) #making bullet from scratch at top left corner of the window
        self.rect.midtop = ai_game.ship.rect.midtop #placing the bullet at midtop

        #storing the value as decimal
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        #update the rect
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect) #draw.rect() function fills the part of the screen defined by the bullet’s rect with the color stored in self.color
