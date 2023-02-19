import pygame
import pygame.gfxdraw
import noise_data as nd
import generation_functions as gf
import draw_functions as df
import input_handler as ih
import color as c

class game_control:
    def __init__(self, width=256, height=256, scale=1):
        pygame.init()
        pygame.key.set_repeat(200, 20)

        self.scale = scale
        self.size = self.width, self.height = width * scale, height * scale
        self.screen = pygame.display.set_mode(self.size)
        self.text = pygame.font.Font("fonts\shittypixel1.ttf", 18)
        # for moving around

        self.generation_variables = nd.generation_variables(self.width, 4, .5, .2, 50)
        
        # generates the starting chunks at coordinate 0
        self.starting_chunk_1d = nd.chunk(0, self.generation_variables)
        self.starting_chunk_2d = nd.chunk(0, self.generation_variables, True)

        # a list of chunks
        chunks_1d = [self.starting_chunk_1d]
        chunks_2d = [self.starting_chunk_2d]

        self.draw_variables = nd.draw_variables()
        self.map_1d = nd.map(width, chunks_1d, 1)
        self.map_2d = nd.map(width, chunks_2d, 2)
        self.input = ih.input_handler(self, self.draw_variables, self.map_1d, self.map_2d)
        self.colors = c.color()
        self.draw = df.draw(self.screen, self.colors)
    
    def on_user_update(self):
        if self.draw_variables.regen:   
            print("regenerating...")
            self._regen() 
            print("regenerated")

        if self.draw_variables.refresh: 
            print("refreshing...")
            self._refresh()
            print("refreshed")

    def draw_event(self):
        self.screen.fill(self.colors.black)
        self._draw_noise()

        if (self.draw_variables.show_debug):
            self._draw_debug_menu()
        
        # refresh the display
        pygame.display.flip()
    
    def _draw_debug_menu(self):
        cur_x = self.map_1d.x
        cur_z = self.map_1d.z
        text_coords = self.text.render(
            "X (A/D): " + str(cur_x) + " | Z (W/D): " + str(cur_z), False, self.colors.white)
        text_octaves = self.text.render(
            "octaves (O): " + str(self.generation_variables.octaves), False, self.colors.white)
        text_base = self.text.render(
            "base ([/]): " + str(self.generation_variables.min_height)[0:4], False, self.colors.white)
        text_variability = self.text.render(
            "variability (-/=): " + str(self.generation_variables.variability), False, self.colors.white)
        text_bias = self.text.render(
            "scaling_bias (Q/E): " + str(self.generation_variables.scaling_bias)[0:4], False, self.colors.white)
        text_speed = self.text.render(
            "speed (,/.): " + str(self.draw_variables.speed), False, self.colors.white)

        self.screen.blit(text_coords, (5, self.height - 18))
        self.screen.blit(text_octaves, (5, self.height - 36))
        self.screen.blit(text_base, (5, self.height - 54))
        self.screen.blit(text_variability, (5, self.height - 72))
        self.screen.blit(text_bias, (5, self.height - 90))
        self.screen.blit(text_speed, (5, self.height - 108))


    def _draw_noise(self):
        if self.draw_variables.draw_seed:
            self.draw.draw_pure_noise()
        if self.draw_variables.generation_mode == 1:
            for chunk in self.map_1d.chunks:
                self.draw.draw_noise_1d(chunk, self.map_1d)
        elif self.draw_variables.generation_mode == 2:
            for chunk in self.map_2d.chunks:
                self.draw.draw_noise_2d_side(chunk, self.map_2d)

    def _regen(self):
        if self.draw_variables.generation_mode == 1:
            for i, chunk in enumerate(self.map_1d.chunks):
                self.map_1d.chunks[i] = nd.chunk(chunk.coordinate, self.generation_variables)
        elif self.draw_variables.generation_mode == 2:
            if self.draw_variables.full_refresh: 
                for i, chunk in enumerate(self.map_2d.chunks):
                    self.map_2d.chunks[i] = nd.chunk(chunk.coordinate, self.generation_variables)
            else:
                self.map_2d.chunks[-1] = nd.chunk(self.map_2d.chunks[-1].coordinate, self.generation_variables)
        
        self.draw_variables.regen = False

    def _refresh(self):
        if self.draw_variables.generation_mode == 1:
            for chunk in self.map_1d.chunks:
                chunk.noise = gf.generate_noise_1d(chunk)
        elif self.draw_variables.generation_mode == 2:  # only refreshing the latest chunk for 2d
            if self.draw_variables.full_refresh:
                for chunk in self.map_2d.chunks:
                    chunk.noise = gf.generate_noise_2d(chunk)
            else:
                self.map_2d.chunks[-1].noise = gf.generate_noise_2d(self.map_2d.chunks[-1])
        self.draw_variables.full_refresh = False
        self.draw_variables.refresh = False

        