class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 960
        self.screen_height = 540
        self.bg_color = (230, 230, 230)

        #ship settings
        self.ship_speed = 1.5 #adjusting the speed that it will move 1.5pixels per cycle through the while loop
        self.ship_limit = 3

        #Bullet Settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_speed = 3
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 5 # no. of bullets allowed

        #Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 2.0

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50 #points get when an alien is shot down

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
