import perlin_noise as perlin
import noise_data as nd
import pygame
import pygame.gfxdraw
import color as c

class draw:
    def __init__(self, surface:pygame.Surface, color:c.color):
        self.surface = surface
        self.color = color

    def draw_noise_1d(self, chunk:nd.chunk, map:nd.map):
        chunk_noise = chunk.noise
        chunk_x = chunk.coordinate
        for i in range(chunk.generation_variables.size):
            y = chunk_noise[i]
            x = i + (map.x + (chunk_x * chunk.generation_variables.size))
            y_2 = map.y_0 - (y * map.y_0)
            pygame.draw.line(self.surface, self.color.noise_color, (x, map.y_0), (x, y_2))

    def draw_noise_2d_side(self, chunk:nd.chunk, map:nd.map):
        temp_1d_chunk = nd.chunk(chunk.coordinate, chunk.generation_variables, False, chunk.seed, chunk.noise)
        self.draw_noise_1d(temp_1d_chunk, map)
    
    def draw_noise_2d_top(self, chunk:nd.chunk):
        for x in range(chunk.generation_variables.size):
                for y in range(chunk.generation_variables.size):
                    grey_value = chunk[x, y] * 255
                    col = grey_value, grey_value, grey_value
                    pygame.gfxdraw.pixel(self.surface, x, y, col)

    def draw_pure_noise(self, chunk:nd.chunk, map:nd.map):
        for i in range(self.controller.width):
            pygame.draw.line(self.surface, c.green, (i, (map.y_0)),
                             (i, (map.y_0) - chunk.seed[i] * (map.y_0)))
