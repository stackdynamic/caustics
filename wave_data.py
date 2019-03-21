class WaveData:
    def __init__(self, water_depth, intensity_multiplier, scale, impact_range, N, frequency, W, direction, amplitude, steepness, k, width, height):
        self.water_depth = water_depth
        self.intensity_multiplier = intensity_multiplier
        self.scale = scale
        self.impact_range = impact_range
        self.N = N
        self.frequency = frequency
        self.W = W
        self.direction = direction
        self.amplitude = amplitude
        self.steepness = steepness
        self.k = k
        self.width = width
        self.height = height

    def __str__(self):
        return "\n".join(f"{key}: {value}" for key, value in self.__dict__.items())
