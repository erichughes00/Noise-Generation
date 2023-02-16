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
        self.speed = 5

        self.generation_variables = nd.generation_variables(self.width, 4, .5, .2, 50)
        
        # generates the starting chunks at coordinate 0
        self.starting_chunk_1d = nd.chunk(0, self.generation_variables)
        self.starting_chunk_2d = nd.chunk(0, self.generation_variables, True)
 
        self.x, self.y, self.z = 0, 1, 1
        # the bottom of the window
        self.y_0 = self.height - 1

        # Counters  for
        self.chunk_counters = self.pos_chunks, self.neg_chunks, self.pos_chunks_2d, self.neg_chunks_2d = 0, 0, 0, 0

        # a list of chunks
        self.chunks_1d = [self.starting_chunk_1d]
        self.chunks_2d = [self.starting_chunk_2d]

        # 1 - 1D, 2 - 2D, 3 - 2D (lines), 4 - 2D (blend)
        self.generation_mode = 1

        self.visual_2d_mode = False
        self.draw_seed = False
        self.refresh = True
        self.full_refresh = False
        self.regen = False
        self.show_debug = False
        self.input = ih.input_handler(self)
        self.draw = df.draw(self.screen, self)
        self.colors = c.color()
    
    def on_user_update(self):
        if self.regen:   
            print("regenerating...")
            self._regen() 
            print("regenerated")

        if self.refresh: 
            print("refreshing...")
            self._refresh()
            print("refreshed")

    def draw_event(self):
        self.screen.fill(c.black)
        self._draw_noise()

        if (self.show_debug):
            self._draw_debug_menu()
        
        # refresh the display
        pygame.display.flip()
    
    def _draw_debug_menu(self):
        text_coords = self.text.render(
            "X (A/D): " + str(self.x) + " | Z (W/D): " + str(self.z), False, c.white)
        text_octaves = self.text.render(
            "octaves (O): " + str(self.generation_variables.octaves), False, c.white)
        text_base = self.text.render(
            "base ([/]): " + str(self.generation_variables.min_height), False, c.white)
        text_variability = self.text.render(
            "variability (-/=): " + str(self.generation_variables.variability), False, c.white)
        text_bias = self.text.render(
            "scaling_bias (Q/E): " + str(self.generation_variables.scaling_bias)[0:4], False, c.white)
        text_speed = self.text.render(
            "speed (,/.): " + str(self.speed), False, c.white)

        self.screen.blit(text_coords, (5, self.height - 18))
        self.screen.blit(text_octaves, (5, self.height - 36))
        self.screen.blit(text_base, (5, self.height - 54))
        self.screen.blit(text_variability, (5, self.height - 72))
        self.screen.blit(text_bias, (5, self.height - 90))
        self.screen.blit(text_speed, (5, self.height - 108))


    def _draw_noise(self):
        if self.draw_seed:
            self.draw.draw_pure_noise()
        if self.generation_mode == 1:
            for chunk in self.chunks_1d:
                self.draw.draw_noise_1d(chunk)
        elif self.generation_mode == 2:
            for chunk in self.chunks_2d:
                self.draw.draw_noise_2d(chunk)


    def _regen(self):
        if self.generation_mode == 1:
            for chunk in self.chunks_1d:
                chunk = nd.chunk(chunk.coordinate, self.generation_variables)
        elif self.generation_mode == 2:
            if self.full_refresh: 
                for chunk in self.chunks_2d:
                    chunk = nd.chunk(chunk.coordinate, self.generation_variables)
            else:
                self.chunks_2d[-1] = nd.chunk(chunk.coordinate, self.generation_variables)
        
        self.regen = False

    def _refresh(self):
        if self.generation_mode == 1:
            for chunk in self.chunks_1d:
                chunk.noise = gf.generate_noise_1d(chunk.seed)
        elif self.generation_mode == 2:  # only refreshing the latest chunk for 2d bc its slow
            if self.full_refresh:
                for chunk in self.chunks_2d:
                    chunk.noise = gf.generate_noise_2d(chunk.seed)
            else:
                self.chunks_2d[-1].noise = gf.generate_noise_2d(self.chunks_2d[-1].seed)
        self.full_refresh = False
        self.refresh = False

        