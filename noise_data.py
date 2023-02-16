import perlin_noise as perlin

class generation_variables:
    def __init__(self, size:int, octaves:int, min_height:float, scaling_bias:float, variability:int):
        self.size = size
        self.octaves = octaves
        self.min_height = min_height
        self.scaling_bias = scaling_bias
        self.variability = variability
        self.min_heights = None
        

class draw_variables:
    def __init__(self):
        self.visual_2d_mode = False
        self.draw_seed = False
        self.refresh = True
        self.full_refresh = False
        self.regen = False
        self.show_debug = False
        self.speed = 5
        self.generation_mode = 1

class chunk:
    def __init__(self, coordinate:int, generation_variables:generation_variables, is_2d=False, seed=None, noise=None):
        self.coordinate = coordinate
        self.is_2d = is_2d
        
        self.generation_variables = generation_variables

        if seed is None:
            self.seed = perlin.gen_seed(self.generation_variables.size, self.generation_variables.min_height, self.generation_variables.variability)
            if is_2d:
                self.generation_variables.min_heights = self.seed
                self.seed = perlin.gen_seed_2d(self.generation_variables.size, self.generation_variables.min_heights, self.generation_variables.variability)
                self.noise = perlin.gen_perlin_noise_2D(self.generation_variables.size, self.seed, self.generation_variables.octaves, self.generation_variables.scaling_bias)
            else:
                self.noise = perlin.gen_perlin_noise_1D(self.generation_variables.size, self.seed, self.generation_variables.octaves, self.generation_variables.scaling_bias)
        else:
            self.seed = seed
            self.noise = noise

class map:
    def __init__(self, size, chunks:list[chunk], generation_mode:int):
        self.size = size
        self.x = 0
        self.y = 1
        self.z = 1
        self.y_0 = self.size - 1
        self.chunks = chunks
        self.pos_chunks = 0
        self.neg_chunks = 0
        # 1 is for 1d, 2 is for 2d
        self.generation_mode = generation_mode