import random as rand

class color:
    def __init__(self):
        self.green = 15, 200, 50
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.noise_color = self.green

    def randomize_noise_color(self):
        self.noise_color = rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255)