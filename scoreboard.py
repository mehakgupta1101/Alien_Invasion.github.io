import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score) #turning the numerical value of score into string
        #rounding the score
        rounded_score = round(self.stats.score, -1) #-1 will round the score to the nearest 10
        score_str = "{:,}".format(rounded_score) #inserting commas in the score

        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color) #converting the score into image

        # Display the score at the top right of the screen.
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 #placing the score to the right  set its right edge 20 pixels from the right edge of the screen
        self.score_rect.top = 20 # place the top edge 20 pixels down from the top of the screen

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx # center the high score rect horizontally
        self.high_score_rect.top = self.score_rect.top # set its top attribute to match the top of the score image

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group() #creates an empty group to hold ship instances
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)






    def show_score(self):
        """Draw scores and level to the screen."""
        self.screen.blit(self.score_img, self.score_rect) #draws the score image onscreen at the location score_rect specifies.
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score() #to update the high score's image
