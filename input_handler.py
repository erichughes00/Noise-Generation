import pygame
import game_control
import noise_data as nd
import generation_functions as gf


class input_handler:
    def __init__(self, controller: game_control.game_control):
        self.controller = controller
        self.colors = self.controller.colors
        self.generation_variables = self.controller.generation_variables

    def on_keyboard_press(self):
        # R - randomize the seeds and regenerate the map - a hard refresh
        if pygame.key.get_pressed()[pygame.K_r]:
            self._hard_refresh()

        # SPACE - soft Refresh
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._soft_refresh()

        # F5 - toggle debug menu
        if pygame.key.get_pressed()[pygame.K_F5]:
            self._toggle_debug()

        # C - randomize the color
        if pygame.key.get_pressed()[pygame.K_c]:
            self._randomize_color()

        # O - increase the octave count
        if pygame.key.get_pressed()[pygame.K_o]:
            self._increase_octaves()

        # 1 - switch to 1D noise generation
        if pygame.key.get_pressed()[pygame.K_1]:
            self.controller.generation_mode = 1

        # 2 - switch to 2D noise generation
        if pygame.key.get_pressed()[pygame.K_2]:
            self.controller.generation_mode = 2

        # 3 - switch to alternative 2D noise generation
        if pygame.key.get_pressed()[pygame.K_3]:
            self.controller.generation_mode = 3

        # 4 - switch to blended 2D noise generation
        if pygame.key.get_pressed()[pygame.K_4]:
            self.controller.generation_mode = 4

        # N - toggle between pure noise and perlin noise
        if pygame.key.get_pressed()[pygame.K_n]:
            self.controller.draw_seed = not self.controller.draw_seed

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
            self._add_chunk(1)

        # RIGHT - add new chunk to the left
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self._add_chunk(-1)

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
        if self.controller.generation_mode != 1:
            # W - Move backwards
            if pygame.key.get_pressed()[pygame.K_w]:
                self._move_forward()

            # S - Move backwards
            if pygame.key.get_pressed()[pygame.K_s]:
                self._move_backward()

            # toggles 2d grayscale visualization
            if pygame.key.get_pressed()[pygame.K_f]:
                self.controller.visual_2d_mode = not self.controller.visual_2d_mode

    def _hard_refresh(self):
        if self.controller.generation_mode == 2:
            self.controller.full_refresh = True
        self.controller.regen = True

    def _soft_refresh(self):
        self.controller.refresh = True

    def _regen(self):
        self.controller.regen = True

    def _toggle_debug(self):
        self.controller.show_debug = not self.controller.show_debug

    def _randomize_color(self):
        self.colors.randomize_noise_color()

    def _increase_octaves(self):
        self.generation_variables.octaves += 1
        if self.generation_variables.octaves > 9:
            self.generation_variables.octaves = 1
        self._soft_refresh()

    def _lower_scaling_bias(self):
        self.generation_variables.scaling_bias -= .2
        if self.generation_variables.scaling_bias < .2:
            self.generation_variables.scaling_bias = .2
        self._soft_refresh()

    def _raise_scaling_bias(self):
        self.generation_variables.scaling_bias += .2
        self._soft_refresh()

    def _increase_speed(self):
        if self.controller.speed < 50:
            self.controller.speed += 1

    def _lower_speed(self):
        self.controller.speed = max(1, self.controller.speed - 1)

    def _move_left(self):
        self.controller.x += 1 * self.controller.speed

    def _move_right(self):
        self.controller.x -= 1 * self.controller.speed

    # direction should be either -1 for left or 1 for right
    def _add_chunk(self, direction: int):
        if self.controller.generation_mode == 1:
            self.controller.pos_chunks += direction
            new_chunk = nd.chunk(
                self.controller.size, self.controller.pos_chunks, self.generation_variables)
            self.controller.chunks_1d.append(new_chunk)
        elif self.controller.generation_mode == 2:
            self.controller.pos_chunks_2d += direction
            new_chunk = nd.chunk(
                self.controller.size, self.controller.pos_chunks, self.generation_variables, True)
            self.controller.chunks_2d.append(new_chunk)
        self._soft_refresh()

    def _raise_min_height(self):
        self.generation_variables.min_height = min(
            self.generation_variables.min_height + .1, 1)
        self.generation_variables.min_heights = gf.generate_seed_1d(
            self.generation_variables)
        self._regen()

    def _lower_min_height(self):
        self.generation_variables.min_height = max(
            self.generation_variables.min_height - .1, 0)
        self.generation_variables.min_heights = gf.generate_seed_1d(
            self.generation_variables)
        self._regen()

    def _raise_variability(self):
        self.generation_variables.variability += 1
        self.generation_variables.variability = min(
            self.generation_variables.variability, 100)
        self._regen()

    def _lower_variability(self):
        self.generation_variables.variability -= 1
        self.generation_variables.variability = max(
            self.generation_variables.variability, 0)
        self._regen()

    def _move_forward(self):
        speed_adjusted = int(self.controller.speed / 2)
        self.controller.z += speed_adjusted
        if self.controller.z > self.controller.width - 1:
            self.controller.z = min(
                self.controller.z - self.controller.width, 1)

    def _move_backward(self):
        speed_adjusted = int(self.controller.speed / 2)
        self.controller.z += speed_adjusted
        if self.controller.z < 1:
            self.controller.z = max(
                self.controller.width + self.controller.z - 1, self.controller.width - 1)

    def _get_chunks(self):
        if self.controller.generation_mode == 1:
            return self.controller.chunks_1d
        elif self.controller.generation_mode == 2:
            return self.controller.chunks_2d
