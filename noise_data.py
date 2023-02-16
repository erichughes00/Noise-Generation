import perlin_noise as perlin
import generation_functions as gf

class generation_variables:
    def __init__(self, size:int, octaves:int, min_height:float, scaling_bias:float, variability:int):
        self.size = size
        self.octaves = octaves
        self.min_height = min_height
        self.scaling_bias = scaling_bias
        self.variability = variability
        self.min_heights = None

class chunk:
    def __init__(self, coordinate:int, generation_variables:generation_variables, is_2d=False, seed=None, noise=None):
        self.coordinate = coordinate
        self.is_2d = is_2d
        
        self.generation_variables = generation_variables

        if seed == None:
            self.seed = perlin.gen_seed(self.generation_variables.size, self.generation_variables.min_height, self.generation_variables.variability)
            if is_2d:
                self.generation_variables.min_heights = self.seed
                self.seed = perlin.gen_seed_2d(self.generation_variables.size, self.generation_variables.min_heights, self.generation_variables.variability)
                self.noise = gf.generate_noise_2d(self)
            else:
                self.noise = gf.generate_noise_1d(self)
        else:
            self.seed = seed
            self.noise = noise

