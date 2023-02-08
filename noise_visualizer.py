import perlin_noise as perlin
import sys
import pygame
import pygame.gfxdraw
import random as rand

pygame.init()
pygame.key.set_repeat(200, 20)

scale = 1
size = s_width, s_height = 256 * scale, 256 * scale
screen = pygame.display.set_mode(size)
font_object = pygame.font.Font("shittypixel1.ttf", 18)

green = 15, 200, 50
green_a = 15, 200, 50, 100
black = 0, 0, 0
white = 255, 255, 255
noise_color = green
octaves = 4
# between 0 and 1
min_height = .5
scaling_bias = 1.8
# higher means more variable
variability = 50

seed = perlin.gen_seed(s_width, min_height, variability)
draw_seed = False
generation_mode = 1  # 1 - 1D, 2 - 2D, 3 - 2D (lines), 4 - 2D (blend)
visual_2d_mode = False

coords = c_x, c_y = 0, 1
y_0 = s_height - 1
speed = 5

# for 2D
min_heights = seed
c_z = 1
seed_2d = perlin.gen_seed_2d(s_width, min_heights, variability)

noise_1d = seed
noise_2d = seed_2d
noise_2d_alt = seed_2d
noise_2d_blend = seed_2d

pos_chunks = 0
neg_chunks = 0
pos_chunks_2d = 0
neg_chunks_2d = 0

# a list of tuples: (the noise, the seed, and the chunk coordinate)
chunks_1d = [[noise_1d, seed, 0]]
chunks_2d = [[noise_2d, seed_2d, 0]]

surf = pygame.display.get_surface()

# generates 1d noise and saves it
def generate_noise_1d(seed=seed):
    return perlin.gen_perlin_noise_1D(s_width, seed, octaves, scaling_bias)

# generates 2d noise and saves it
def generate_noise_2d(seed=seed_2d):
    return perlin.gen_perlin_noise_2D(s_width, seed, octaves, scaling_bias)


def generate_noise_2d_alt(seed=noise_2d_alt):
    return perlin.gen_perlin_noise_2D_lines(s_width, seed, octaves, scaling_bias)


def generate_noise_2d_blend():
    return perlin.add_maps(s_width, noise_2d, noise_2d_alt)


def draw_noise_1d(chunk=chunks_1d[0]):
    chunk_noise = chunk[0]
    chunk_x = chunk[2]
    for i in range(s_width):
        y = chunk_noise[i]
        x = i + (c_x + (chunk_x * s_width))
        y_2 = y_0 - (y * y_0)
        pygame.draw.line(surf, noise_color, (x, y_0), (x, y_2))


def draw_noise_2d(chunk=chunks_2d[0]):
    # Top down
    if visual_2d_mode:
        for x in range(s_width):
            for y in range(s_height):
                grey_value = chunk[x, y] * 255
                col = grey_value, grey_value, grey_value
                pygame.gfxdraw.pixel(surf, x, y, col)
    else:  # 1D Slices
        temp_1d_chunk = [chunk[0][c_z], chunk[1][c_z], chunk[2]]
        draw_noise_1d(temp_1d_chunk)
        # for i in range(s_width):
        #    y = chunk_noise[i]
        #    x = i + (c_x + (chunk_x * s_width))
        #    pygame.draw.line(surf, noise_color, (i, (y_0)), (i, (y_0) - chunk_noise[c_z, i] * (y_0)))


def draw_pure_noise():
    for i in range(s_width):
        pygame.draw.line(surf, green, (i, (y_0)), (i, (y_0) - seed[i] * (y_0)))


noise_1d = generate_noise_1d()
noise_2d = generate_noise_2d()
noise_2d_alt = generate_noise_2d_alt()
noise_2d_blend = generate_noise_2d_blend()

chunks_1d[0][0] = noise_1d
chunks_2d[0][0] = noise_2d

refresh = True
full_refresh = False
regen = False
show_debug = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Keyboard events:
        elif event.type == pygame.KEYDOWN:
            # R - randomize the seeds and regenerate the map - a hard refresh
            if pygame.key.get_pressed()[pygame.K_r]:
                if generation_mode == 2:
                    full_refresh = True
                regen = True
            # SPACE - soft Refresh
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                refresh = True
            # F5 - toggle debug menu
            if pygame.key.get_pressed()[pygame.K_F5]:
                show_debug = not show_debug
            # C - randomize the color
            if pygame.key.get_pressed()[pygame.K_c]:
                noise_color = rand.randint(0, 255), rand.randint(
                    0, 255), rand.randint(0, 255)
            # O - increase the octave count
            if pygame.key.get_pressed()[pygame.K_o]:
                octaves += 1
                if octaves > 9:
                    octaves = 1
                refresh = True
            # 1 - switch to 1D noise generation
            if pygame.key.get_pressed()[pygame.K_1]:
                generation_mode = 1
            # 2 - switch to 2D noise generation
            if pygame.key.get_pressed()[pygame.K_2]:
                generation_mode = 2
            # 3 - switch to alternative 2D noise generation
            if pygame.key.get_pressed()[pygame.K_3]:
                generation_mode = 3
            # 4 - switch to blended 2D noise generation
            if pygame.key.get_pressed()[pygame.K_4]:
                generation_mode = 4
            # N - toggle between pure noise and perlin noise
            if pygame.key.get_pressed()[pygame.K_n]:
                draw_seed = not draw_seed
            # Q - lower scaling bias
            if pygame.key.get_pressed()[pygame.K_q]:
                scaling_bias -= .2
                if scaling_bias < .2:
                    scaling_bias = .2
                refresh = True
            # E - raise scaling bias
            if pygame.key.get_pressed()[pygame.K_e]:
                scaling_bias += .2
                refresh = True
            # . - increase speed
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                if speed < 50:
                    speed += 1
            # , - lower speed
            if pygame.key.get_pressed()[pygame.K_COMMA]:
                speed = max(1, speed - 1)
            # A - move to the left
            if pygame.key.get_pressed()[pygame.K_a]:
                c_x += 1 * speed
            # D - move to the right
            if pygame.key.get_pressed()[pygame.K_d]:
                c_x -= 1 * speed
            # RIGHT - add new chunk to the right
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if generation_mode == 1:
                    new_seed = perlin.gen_seed(
                        s_width, min_height, variability)
                    new_noise = generate_noise_1d(generate_noise_1d(new_seed))
                    pos_chunks += 1
                    chunks_1d.append([new_noise, new_seed, pos_chunks])
                elif generation_mode == 2:
                    new_seed = perlin.gen_seed_2d(
                        s_width, min_heights, variability)
                    new_noise = generate_noise_2d(new_seed)
                    pos_chunks_2d += 1
                    chunks_2d.append([new_noise, new_seed, pos_chunks_2d])
                refresh = True
            # RIGHT - add new chunk to the left
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if generation_mode == 1:
                    new_seed = perlin.gen_seed(
                        s_width, min_height, variability)
                    new_noise = generate_noise_1d(generate_noise_1d(new_seed))
                    neg_chunks -= 1
                    chunks_1d.append([new_noise, new_seed, neg_chunks])
                elif generation_mode == 2:
                    new_seed = perlin.gen_seed_2d(
                        s_width, min_heights, variability)
                    new_noise = generate_noise_2d(new_seed)
                    neg_chunks_2d -= 1
                    chunks_2d.append([new_noise, new_seed, neg_chunks_2d])
                refresh = True
            # ] - raise the min_height
            if pygame.key.get_pressed()[pygame.K_RIGHTBRACKET]:
                min_height += .1
                min_height = min(min_height, 1)
                min_heights = perlin.gen_seed(s_width, min_height, variability)
                regen = True
                refresh = True
            # [ - lower the min_height
            if pygame.key.get_pressed()[pygame.K_LEFTBRACKET]:
                min_height -= .1
                min_height = max(min_height, 0)
                min_heights = perlin.gen_seed(s_width, min_height, variability)
                regen = True
                refresh = True
            # + - raise the variability
            if pygame.key.get_pressed()[pygame.K_EQUALS]:
                variability += 1
                variability = min(variability, 100)
                regen = True
                refresh = True
            # - - lower the variability
            if pygame.key.get_pressed()[pygame.K_MINUS]:
                variability -= 1
                variability = max(variability, 0)
                regen = True
                refresh = True
            # Only happens for 2d noise
            if generation_mode != 1:
                # W - increase c_z
                if pygame.key.get_pressed()[pygame.K_w]:
                    speed_adjusted = int(speed / 2)
                    c_z += speed_adjusted
                    if c_z > s_width - 1:
                        c_z = min(c_z - s_width, 1)
                if pygame.key.get_pressed()[pygame.K_s]:
                    speed_adjusted = int(speed / 2)
                    c_z -= speed_adjusted
                    if c_z < 1:
                        c_z = max(s_width + c_z - 1, s_width - 1)
                # toggles 2d grayscale visualization
                if pygame.key.get_pressed()[pygame.K_f]:
                    visual_2d_mode = not visual_2d_mode

    if regen:
        print("generating seeds...")
        if generation_mode == 1:
            for chunk in chunks_1d:
                chunk[1] = perlin.gen_seed(s_width, min_height, variability)
        elif generation_mode == 2:
            if full_refresh:  # only generate for all the chunks when user has hit R
                for chunk in chunks_2d:
                    chunk[1] = perlin.gen_seed_2d(
                        s_width, min_heights, variability)
            else:
                chunks_2d[-1][1] = perlin.gen_seed_2d(
                    s_width, min_heights, variability)
        elif generation_mode == 3:
            seed_2d = perlin.gen_seed_2d(s_width)
        regen = False
        print("seeds generated...")
        refresh = True

    if refresh:
        print("refreshing...")
        if generation_mode == 1:
            for chunk in chunks_1d:
                chunk[0] = generate_noise_1d(chunk[1])
        elif generation_mode == 2:  # only refreshing the latest chunk for 2d bc its slow
            if full_refresh:
                for chunk in chunks_2d:
                    chunk[0] = generate_noise_2d(chunk[1])
            else:
                chunks_2d[-1][0] = generate_noise_2d(chunk[1])
        elif generation_mode == 3:
            noise_2d_alt = generate_noise_2d_alt()
        elif generation_mode == 4:
            noise_2d_blend = generate_noise_2d_blend()

        full_refresh = False
        refresh = False
        print("refreshed")

    screen.fill(black)
    if draw_seed:
        draw_pure_noise()
    if generation_mode == 1:
        for chunk in chunks_1d:
            draw_noise_1d(chunk)
    elif generation_mode == 2:
        for chunk in chunks_2d:
            draw_noise_2d(chunk)
    elif generation_mode == 3:
        draw_noise_2d(noise_2d_alt)
    elif generation_mode == 4:
        draw_noise_2d(noise_2d_blend)

    if (show_debug):
        text_coords = font_object.render(
            "X (A/D): " + str(c_x) + " | Z (W/D): " + str(c_z), False, white)
        text_octaves = font_object.render(
            "octaves (O): " + str(octaves), False, white)
        text_base = font_object.render(
            "base ([/]): " + str(min_height), False, white)
        text_variability = font_object.render(
            "variability (-/=): " + str(variability), False, white)
        text_bias = font_object.render(
            "scaling_bias (Q/E): " + str(scaling_bias)[0:4], False, white)
        text_speed = font_object.render(
            "speed (,/.): " + str(speed), False, white)

        screen.blit(text_coords, (5, s_height - 18))
        screen.blit(text_octaves, (5, s_height - 36))
        screen.blit(text_base, (5, s_height - 54))
        screen.blit(text_variability, (5, s_height - 72))
        screen.blit(text_bias, (5, s_height - 90))
        screen.blit(text_speed, (5, s_height - 108))

    # refresh the display
    pygame.display.flip()