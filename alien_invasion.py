#importing modules
import sys
from time import sleep #importing sleep() function from time module to pause the game for a second when the ship is hit
import pygame
from settings import Settings #importing Settings class from settings module
from game_stats import GameStats #importing GameStats class from game_stats module
from ship import Ship #importing Ship class from Ship module
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

#creating a class
class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() #Initialize background settings
        self.settings = Settings() #creating an instance of Settings class
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #fullscreenwindow
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #creating a display game window
        pygame.display.set_caption("Alien Invasion by Mehak Gupta")
        self.stats = GameStats(self) #creating an instance of GameStats class to store statistics
        self.sb = Scoreboard(self) #creating an instance of Scoreboard class to store statistics
        self.ship = Ship(self) #creating an instance of Ship class
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() #making a group to jold fleet of aliens

        self._create_fleet() #helper method

        # Make the Play button
        self.play_button  = Button(self, "Play") #creates an instance of button class and label it as a play but does not draw button to the screen

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events() #helper method

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets() #helper method
                self._update_aliens() #helper method

            self._update_screen() #helper method

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get(): #event loop which triggers when any mouse or keyboard event occur
            if event.type == pygame.QUIT:
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: #triggers when user clicks anywhere on the screen
                mouse_pos = pygame.mouse.get_pos() #this function returns a tuple containg mouse cursor's x and y co-ordinates
                self._check_play_button(mouse_pos) #passing the values to this method

            elif event.type == pygame.KEYDOWN: #triggers when any key is pressed
                self._check_keydown_events(event) #helper method

            elif event.type == pygame.KEYUP: #triggers when any key is released
                self._check_keyup_events(event) #helper method

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialise_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Responded to keypresses"""
        if event.key == pygame.K_RIGHT: #check for the right key
            self.ship.moving_right = True #move the ship to the right
        elif event.key == pygame.K_LEFT: #check for the left key
            self.ship.moving_left = True #move the ship to the right
        elif event.key == pygame.K_q: #pressing q to quit the game
            sys.exit()
        elif event.key == pygame.K_SPACE: #triggers when spacebar is pressed
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Responded to keyreleases"""
        if event.key == pygame.K_RIGHT: #check for the right key
            self.ship.moving_right = False #ship will be motionless
        elif event.key == pygame.K_LEFT: #check for the left key
            self.ship.moving_left = False #move the ship to the right

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed: #limiting the no. of bullets
            new_bullet = Bullet(self) #making an instance of bullet
            self.bullets.add(new_bullet) #adding the bullets to the group using add() method

    def _update_bullets(self):
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  #if collision happened the it will add the score
                self.sb.prep_score() #to draw the updated image on the screen
                self.sb.check_high_score()

        #creating a new fleet after whole fleet is destroyed
        if not self.aliens: #checking wether the alien group is empty or not
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge,then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #looking for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens): #this function takes sprite(ship) and group(alien)
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self) #creating an instance of class Alien
        alien_width, alien_height = alien.rect.size #size attribute containes a tuple with width and height of a rect object
        available_space_x = self.settings.screen_width - (2 * alien_width) #checking for horizontal space available
        number_aliens_x = available_space_x // (2 * alien_width) #finding ht no. of aliens to fit into the screen

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create a full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): #this loop will create a alien in one row
                self._create_alien(alien_number, row_number) #helper method

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #pauses the game for a moment
            sleep(2)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
            """Check if any aliens have reached the bottom of the screen."""
            screen_rect = self.screen.get_rect()
            for alien in self.aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                    # Treat this the same as if the ship got hit.
                    self._ship_hit()
                    break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        #calling the blitme method
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #draw the alien on the screen using group's draw method
        self.aliens.draw(self.screen)

        ## Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai_game= AlienInvasion()
    ai_game.run_game()
