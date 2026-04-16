import random

class Game:
    def __init__(self, lives=3, bullets=2):
        self.max_lives = lives
        self.bullets = bullets
        self.reset()

    def reset(self):
        self.lives = self.max_lives
        self.reset_drum()

    def reset_drum(self):
        self.bullet_positions = random.sample(range(1, 7), self.bullets)
        self.current_position = 1
        self.alive = True

    def shot(self):
        if not self.alive:
            return "game over"
        
        if self.current_position in self.bullet_positions:
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
                return "fatal_boom"
            else:
                self.current_position += 1
                return "boom"
        else:
            self.current_position += 1
            return 'empty'
