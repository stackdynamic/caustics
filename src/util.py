import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class WaveData:
    # Global variables used regardless of data passed in (TODO: encapsulate these into wave_data)
    light_direction = normalize(np.array([1, -1, .5]))  # Vector direction of light
    # The size of the water plane used for refraction relative to the collision plane
    photon_range_multiplier = np.array([1, 1])
    # The step used for the points on the water surface (1 is no skipping, 2 is every other, etc.)
    refraction_step = .5
    # Ratio between refractive index of the first medium and the second (air/water)
    refractive_ratio = .85

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

    def __str(self):
        return "\n".join(f"{key}: {value}" for key, value in self.__dict__.items())
