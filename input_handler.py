import pygame
import noise_data as nd
import generation_functions as gf
import color


class input_handler:
    def __init__(self, colors:color.color, draw_variables:nd.draw_variables, map_1d:nd.map, map_2d:nd.map):
        self.colors = colors
        self.draw_variables = draw_variables
        self.map_1d = map_1d
        self.map_2d = map_2d

    def on_keyboard_press(self):
        # R - randomize the seeds and regenerate the map - a hard refresh
        if pygame.key.get_pressed()[pygame.K_r]:
            self._hard_refresh()

        # SPACE - soft Refresh
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._soft_refresh()

        # F5 - toggle debug menu
        if pygame.key.get_pressed()[pygame.K_p]:
            self._toggle_debug()

        # C - randomize the color
        if pygame.key.get_pressed()[pygame.K_c]:
            self._randomize_color()

        # O - increase the octave count
        if pygame.key.get_pressed()[pygame.K_o]:
            self._increase_octaves()

        # 1 - switch to 1D noise generation
        if pygame.key.get_pressed()[pygame.K_1]:
            self._set_generation_mode(1)

        # 2 - switch to 2D noise generation
        if pygame.key.get_pressed()[pygame.K_2]:
            self._set_generation_mode(2)

        # 3 - switch to alternative 2D noise generation
        #if pygame.key.get_pressed()[pygame.K_3]:
        #    self._set_generation_mode(3)

        # 4 - switch to blended 2D noise generation
        #if pygame.key.get_pressed()[pygame.K_4]:
        #    self._set_generation_mode(4)

        # N - toggle between pure noise and perlin noise
        if pygame.key.get_pressed()[pygame.K_n]:
            self.draw_variables.draw_seed = not self.draw_variables.draw_seed

        # Q - lower scaling bias
        if pygame.key.get_pressed()[pygame.K_q]:
            self._lower_scaling_bias()

        # E - raise scaling bias
        if pygame.key.get_pressed()[pygame.K_e]:
            self._raise_scaling_bias()

        # . - increase speed
        if pygame.key.get_pressed()[pygame.K_PERIOD]:
            self._increase_speed()

        # , - lower speed
        if pygame.key.get_pressed()[pygame.K_COMMA]:
            self._lower_speed()

        # A - move to the left
        if pygame.key.get_pressed()[pygame.K_a]:
            self._move_left()

        # D - move to the right
        if pygame.key.get_pressed()[pygame.K_d]:
            self._move_right()

        # RIGHT - add new chunk to the right
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self._add_chunk_right()

        # RIGHT - add new chunk to the left
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self._add_chunk_left()

        # ] - raise the min_height
        if pygame.key.get_pressed()[pygame.K_RIGHTBRACKET]:
            self._raise_min_height()

        # [ - lower the min_height
        if pygame.key.get_pressed()[pygame.K_LEFTBRACKET]:
            self._lower_min_height()

        # + - raise the variability
        if pygame.key.get_pressed()[pygame.K_EQUALS]:
            self._raise_variability()

        # - - lower the variability
        if pygame.key.get_pressed()[pygame.K_MINUS]:
            self._lower_variability()

        # Only happens for 2d noise
        if self.draw_variables.generation_mode != 1:
            # W - Move forwards
            if pygame.key.get_pressed()[pygame.K_w]:
                self._move_forward()

            # S - Move backwards
            if pygame.key.get_pressed()[pygame.K_s]:
                self._move_backward()

            # toggles 2d grayscale visualization
            if pygame.key.get_pressed()[pygame.K_f]:
               self.draw_variables.visual_2d_mode = not self.draw_variables.visual_2d_mode

    def _hard_refresh(self):
        if self.draw_variables.generation_mode == 2:
            self.draw_variables.full_refresh = True
        self.draw_variables.regen = True

    def _soft_refresh(self):
        self.draw_variables.refresh = True
    
    def _set_generation_mode(self, mode:int):
        self.draw_variables.generation_mode = mode

    def _regen(self):
        self.draw_variables.regen = True

    def _toggle_debug(self):
        self.draw_variables.show_debug = not self.draw_variables.show_debug

    def _randomize_color(self):
        self.colors.randomize_noise_color()

    def _increase_octaves(self):
        self.map_1d.chunks[0].generation_variables.octaves += 1
        if self.map_1d.chunks[0].generation_variables.octaves > 9:
            self.map_1d.chunks[0].generation_variables.octaves = 1
        self._update_all_chunks()
        self._soft_refresh()

    def _lower_scaling_bias(self):
        self.map_1d.chunks[0].generation_variables.scaling_bias -= .2
        if self.map_1d.chunks[0].generation_variables.scaling_bias < .2:
            self.map_1d.chunks[0].generation_variables.scaling_bias = .2
        self._update_all_chunks()
        self._soft_refresh()

    def _raise_scaling_bias(self):
        self.map_1d.chunks[0].generation_variables.scaling_bias += .2
        self._update_all_chunks()
        self._soft_refresh()

    def _increase_speed(self):
        if self.draw_variables.speed < 50:
            self.draw_variables.speed += 1

    def _lower_speed(self):
        self.draw_variables.speed = max(1, self.draw_variables.speed - 1)

    def _move_left(self):
        if self.draw_variables.generation_mode == 1:
            self.map_1d.x += 1 * self.draw_variables.speed
        else:
            self.map_2d.x += 1 * self.draw_variables.speed

    def _move_right(self):
        if self.draw_variables.generation_mode == 1:
            self.map_1d.x -= 1 * self.draw_variables.speed
        else:
            self.map_2d.x -= 1 * self.draw_variables.speed

    # direction should be either -1 for left or 1 for right
    def _add_chunk_right(self):
        if self.draw_variables.generation_mode == 1:
            self.map_1d.pos_chunks += 1
            new_chunk = nd.chunk(self.map_1d.pos_chunks, self.map_1d.chunks[0].generation_variables)
            self.map_1d.chunks.append(new_chunk)
        elif self.draw_variables.generation_mode == 2:
            self.map_2d.pos_chunks += 1
            new_chunk = nd.chunk(self.map_2d.pos_chunks, self.map_1d.chunks[0].generation_variables, True)
            self.map_2d.chunks.append(new_chunk)
        self._soft_refresh()

    def _add_chunk_left(self):
        if self.draw_variables.generation_mode == 1:
            self.map_1d.neg_chunks -= 1
            new_chunk = nd.chunk(self.map_1d.neg_chunks, self.map_1d.chunks[0].generation_variables)
            self.map_1d.chunks.append(new_chunk)
        elif self.draw_variables.generation_mode == 2:
            self.map_2d.neg_chunks -= 1
            new_chunk = nd.chunk(self.map_2d.neg_chunks, self.map_1d.chunks[0].generation_variables, True)
            self.map_2d.chunks.append(new_chunk)
        self._soft_refresh()

    def _raise_min_height(self):
        self.map_1d.chunks[0].generation_variables.min_height = min(
            self.map_1d.chunks[0].generation_variables.min_height + .1, 1)
        self._update_all_chunks()
        self.map_1d.chunks[-1].generation_variables.min_heights = gf.generate_seed_1d(
            self.map_1d.chunks[0].generation_variables)
        self._regen()

    def _lower_min_height(self):
        self.map_1d.chunks[0].generation_variables.min_height = max(
            self.map_1d.chunks[0].generation_variables.min_height - .1, 0)
        self._update_all_chunks()
        self.map_1d.chunks[0].generation_variables.min_heights = gf.generate_seed_1d(
            self.map_1d.chunks[0].generation_variables)
        self._regen()

    def _raise_variability(self):
        self.map_1d.chunks[0].generation_variables.variability += 1
        self.map_1d.chunks[0].generation_variables.variability = min(
            self.map_1d.chunks[0].generation_variables.variability, 100)
        self._update_all_chunks()
        self._regen()

    def _lower_variability(self):
        self.map_1d.chunks[0].generation_variables.variability -= 1
        self.map_1d.chunks[0].generation_variables.variability = max(
            self.map_1d.chunks[0].generation_variables.variability, 0)
        self._update_all_chunks()
        self._regen()

    def _move_forward(self):
        speed_adjusted = int(self.draw_variables.speed / 2)
        self.map_2d.z += speed_adjusted
        if self.map_2d.z > self.map_2d.size - 1:
            self.map_2d.z = min(self.map_2d.z - self.map_2d.size, 1)

    def _move_backward(self):
        speed_adjusted = int(self.draw_variables.speed / 2)
        self.map_2d.z += speed_adjusted
        if self.map_2d.z < 1:
            self.map_2d.z = max(
                self.map_2d.size + self.map_2d.z - 1, self.map_2d.size - 1)
    
    def _update_all_chunks(self):
        for i, chunk in enumerate(self.map_1d.chunks):
            if i == 0:
                continue
            self.map_1d.chunks[i].generation_variables = self.map_1d.chunks[0].generation_variables.copy()
