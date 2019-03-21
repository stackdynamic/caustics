import numpy as np
from util import normalize
import math
import sys


# Global variables used regardless of data passed in (TODO: encapsulate these into wave_data)
light_direction = normalize(np.array([1, -1, .5]))  # Vector direction of light
# The size of the water plane used for refraction relative to the collision plane
photon_range_multiplier = np.array([1, 1])
# The step used for the points on the water surface (1 is no skipping, 2 is every other, etc.)
refraction_step = .5
# Ratio between refractive index of the first medium and the second (air/water)
refractive_ratio = .85


def wave_function(point, data, time):
    return 2 * sum(
        data.amplitude[i] * math.pow(
            1 + math.sin(np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time),
            data.k
        ) for i in range(data.N)
    )


def pd_x(point, data, time):
    return -2 * sum(
        data.amplitude[i] * data.k * math.pow(
            1 + math.sin(np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time),
            data.k - 1
        ) * math.cos(
            np.dot(
                data.direction[i], point * data.W[i]
            ) + data.frequency[i] * time) * data.W[i] * data.direction[i][0]
        for i in range(data.N)
    )


def pd_z(point, data, time):
    return -2 * sum(
        data.amplitude[i] * data.k * math.pow(
            1 + math.sin(np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time),
            data.k - 1
        ) * math.cos(
            np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time
        ) * data.W[i] * data.direction[i][1]
        for i in range(data.N)
    )


def Refract(point, data, time, refractive_ratio, light_direction):
    # Finding normal with partial derrivatives
    point_xz = np.array([point[0], point[2]])
    normal = normalize(np.array([
        pd_x(point_xz, data, time),
        1,
        pd_z(point_xz, data, time)
    ]))
    # Source: www.starkeffects.com/snells-law-vector.shtml
    a = np.cross(normal, light_direction)
    refracted_dir = np.subtract(
        np.cross(normal, -a) * refractive_ratio,
        normal * math.sqrt(
            1 - (np.dot(normalize(a), normalize(a)) * refractive_ratio**2)
        )
    )
    scaling = (data.water_depth - point[1]) / refracted_dir[1]
    return np.add(refracted_dir * scaling, point)


def GenerateCaustic(data, time):
    intensities = [0] * data.height * data.width
    a = data.height * photon_range_multiplier[1] // 2
    b = data.width * photon_range_multiplier[0] // 2
    s = refraction_step

    z = -a
    while -a <= z < a:
        x = -b
        while -b <= x < b:
            y = wave_function(np.array([x / data.scale, z / data.scale]), data, time)
            face = np.array([x / data.scale, y, z / data.scale])
            hit = Refract(face, data, time, refractive_ratio, light_direction)
            i = (data.width - 1) / 2
            j = (data.height - 1) / 2
            if i >= hit[0] >= -i and j >= hit[2] >= -j:
                # No, these calls are not superflous.
                # Yes, this is still filth and is a shame to the human race.
                q = int(
                    round(
                        round(data.scale * hit[0] + i, 1)
                    ) + round(
                        round(data.scale * hit[2] + j) * data.width, 1)
                )
                if 0 < data.width + q < len(intensities):
                    intensity = data.intensity_multiplier
                    intensities[q] += intensity
            x += s
        z += s
    return [int(i) for i in intensities]
