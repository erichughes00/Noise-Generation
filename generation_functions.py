import perlin_noise as perlin
import noise_data as nd

def generate_noise_1d(chunk: nd.chunk):
    return perlin.gen_perlin_noise_1D(chunk.size, chunk.seed, chunk.generation_variables.octaves, chunk.generation_variables.scaling_bias)

def generate_noise_2d(chunk: nd.chunk):
    return perlin.gen_perlin_noise_2D(chunk.size, chunk.seed, chunk.generation_variables.octaves, chunk.generation_variables.scaling_bias)

def generate_noise_2d_alt(chunk: nd.chunk):
    return perlin.gen_perlin_noise_2D_lines(chunk.size, chunk.seed, chunk.generation_variables.octaves, chunk.generation_variables.scaling_bias)

def generate_noise_2d_blend(size: int, chunk_1: nd.chunk, chunk_2: nd.chunk):
    return perlin.add_maps(size, chunk_1.noise, chunk_2.noise)

def generate_seed_1d(generation_vars: nd.generation_variables):
    return perlin.gen_seed(generation_vars.size, generation_vars.min_height, generation_vars.variability)

def generate_seed_2d(generation_vars: nd.generation_variables):
    return perlin.gen_seed_2d(generation_vars.size, generation_vars.min_height, generation_vars.variability)