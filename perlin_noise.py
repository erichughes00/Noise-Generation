import random as rand
import numpy as np

# size is the size of the seed/chunk,
# base is the min_height (the value of the first element)
# variability is like compression, higher = less compressed


def gen_seed(size, base=None, variability=100):
    temp = np.random.rand(size)
    if base is None and variability == 100:
        return temp
    else:
        temp[0] = base
        for x in range(size):
            # downwards compression
            if temp[x] > (base + (variability/100)):
                temp[x] = base + (temp[x] * (variability/100))
            # upwards compression
            elif temp[x] < (base - (variability/100)):
                temp[x] = base - (temp[x] * (variability/100))
        return temp

# params are the same as gen_seed() except:
# base is an array of bases


def gen_seed_2d(size, base=None, variability=100):
    print("generating seed...")
    temp = np.random.rand(size, size)
    if base is None:
        return temp
    else:
        for x in range(size):
            temp[x, 0] = base[x]
        for y in range(1, size):
            for x in range(1, size):
                # downwards compression
                if temp[x, y] > (base[x] + (variability/100)):
                    temp[x, y] = base[x] + (temp[x, y] * (variability/100))
                # upwards compression
                elif temp[x, y] < (base[x] - (variability/100)):
                    temp[x, y] = base[x] - (temp[x, y] * (variability/100))
    return temp


def multiply_maps(size, map1, map2):
    output = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            output[x, y] = map1[x, y] * map2[x, y]
    return output


def add_maps(size, map1, map2, offset=0):
    output = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            temp = (map1[x, y] + map2[x, y])
            output[x, y] = min(temp - temp/2, 1)
    return output


def gen_perlin_noise_1D(output_size, seed, octaves=1, bias=2):
    output = np.zeros(output_size)

    for x in range(output_size):
        noise = 0
        scale = 1
        scaleAcc = 0

        for o in range(octaves):
            # size between samples in current octave is pitch
            # the pitch size starts as the size of the array, and gets halved for each octave
            pitch_size = output_size >> o
            # the x locations in the array of the samples we are interpolating between this iteration
            sample1 = (x // pitch_size) * pitch_size
            sample2 = (sample1 + pitch_size) % output_size
            # the actual values we are interpolating between
            noise1 = seed[sample1]
            noise2 = seed[sample2]
            # without this if statement, resulting noise texture will be tileable
            # if sample1 == sample2:
            #    noise2 = seed[output_size - 1]

            blend = (x - sample1) / pitch_size
            sample = (1 - blend) * noise1 + blend * noise2
            noise += sample * scale
            scaleAcc += scale
            scale = scale / bias
        output[x] = noise / scaleAcc
    return output


def gen_perlin_noise_2D_lines(output_size, seed_2d, octaves=1, bias=2):
    output = np.zeros((output_size, output_size))
    frames = np.zeros((output_size, output_size))
    print("point 1")
    # do the perlin algorithm on each seed of seed_2d so we have a list of random perlin noise
    for x in range(output_size):
        frames[x] = gen_perlin_noise_1D(output_size, seed_2d[x], octaves, bias)

    print("point 2")
    # Interpolate the 2nd dimension with our new list
    # we flip the list so we can do it again easier
    interpolate_deez_nuts = frames.T
    print("point 3")
    for y in range(output_size):
        output[y] = gen_perlin_noise_1D(
            output_size, interpolate_deez_nuts[y], octaves, bias)
    print("point 4")
    return output


def gen_perlin_noise_2D(output_size, seed, octaves=1, bias=2):
    print("start")
    output = np.zeros((output_size, output_size))

    for x in range(output_size):
        for y in range(output_size):
            noise = 0
            scale = 1
            scaleAcc = 0
            for o in range(octaves):
                # size between samples in current octave is pitch
                pitch_size = output_size >> o

                sample_x1 = (x // pitch_size) * pitch_size
                sample_y1 = (y // pitch_size) * pitch_size

                sample_x2 = (sample_x1 + pitch_size) % output_size
                sample_y2 = (sample_y1 + pitch_size) % output_size

                blend_x = (x - sample_x1) / pitch_size
                blend_y = (y - sample_y1) / pitch_size

                sample_t = (
                    1 - blend_x) * seed[sample_x1, sample_y1] + blend_x * seed[sample_x2, sample_y1]
                sample_b = (
                    1 - blend_x) * seed[sample_x1, sample_y2] + blend_x * seed[sample_x2, sample_y2]

                noise += (blend_y * (sample_b - sample_t) + sample_t) * scale
                scaleAcc += scale
                scale = scale / bias

            output[x, y] = noise / scaleAcc
    print("done")
    return output
