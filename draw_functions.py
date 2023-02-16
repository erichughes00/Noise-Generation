import perlin_noise as perlin
import noise_data as nd
import pygame
import pygame.gfxdraw
import game_control
import color as c

class draw:
    def __init__(self, surface:pygame.Surface, controller:game_control.game_control):
        self.surface = surface
        self.controller = controller

    def draw_noise_1d(self, chunk:nd.chunk):
        chunk_noise = chunk.noise
        chunk_x = chunk.coordinate
        for i in range(chunk.generation_variables.size):
            y = chunk_noise[i]
            x = i + (self.controller.x + (chunk_x * chunk.generation_variables.size))
            y_2 = self.controller.y_0 - (y * self.controller.y_0)
            pygame.draw.line(self.surface, c.noise_c, (x, self.controller.y_0), (x, y_2))

    def draw_noise_2d(self, chunk:nd.chunk):
        # Top down
        if self.controller.visual_2d_mode:
            for x in range(chunk.generation_variables.size):
                for y in range(chunk.generation_variables.size):
                    grey_value = chunk[x, y] * 255
                    col = grey_value, grey_value, grey_value
                    pygame.gfxdraw.pixel(self.surface, x, y, col)
        else:  # 1D Slices
            temp_1d_chunk = nd.chunk(chunk.coordinate, chunk.generation_variables, False, chunk.seed, chunk.noise)
            self.draw_noise_1d(temp_1d_chunk)

    def draw_pure_noise(self, chunk:nd.chunk):
        for i in range(self.controller.width):
            pygame.draw.line(self.surface, c.green, (i, (self.controller.y_0)),
                             (i, (self.controller.y_0) - chunk.seed[i] * (self.controller.y_0)))
