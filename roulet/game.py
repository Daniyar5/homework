import random

class Game:
    def __init__(self, lives=3, bullets_count=2):
        self.max_lives = lives
        self.bullets_count = bullets_count
        self.reset()

    def reset(self):
        self.lives = self.max_lives
        self.alive = True
        self.reload_cylinder()

    def reload_cylinder(self):
        self.bullet_positions = random.sample(range(1, 7), self.bullets_count)
        self.current_position = 1

    def shot(self):
        if not self.alive:
            return "game over"
        
        if self.current_position in self.bullet_positions:
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
            self.current_position += 1
            return "boom"
        else:
            self.current_position += 1
            return "empty"
