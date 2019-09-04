import numpy as np
from util import normalize
from util import WaveData as wd
import math
import sys


def wave_function(point, data, time):
    return 2 * sum(
        data.amplitude[i] * math.pow(
            1 + math.sin(np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time),
            data.k
        ) for i in range(data.N)
    )


def pd(point, data, time):
    x = 0
    y = 0
    for i in range(data.N):
        pd_comp = (
            data.amplitude[i] * data.k *
            math.pow(
                1 + math.sin(np.dot(
                    data.direction[i],
                    point * data.W[i]
                ) + data.frequency[i] * time),
                data.k - 1
            ) * math.cos(
                np.dot(data.direction[i], point * data.W[i]) + data.frequency[i] * time
            ) * data.W[i]
        )
        x += data.direction[i][0] * pd_comp
        y += data.direction[i][1] * pd_comp
    x *= -2
    y *= -2

    return x, y


def Refract(point, data, time):
    # Finding normal with partial derrivatives
    point_xz = np.array([point[0], point[2]])
    pd_x, pd_z = pd(point_xz, data, time)
    normal = normalize(np.array([pd_x, 1, pd_z]))
    # Source: www.starkeffects.com/snells-law-vector.shtml
    a = np.cross(normal, wd.light_direction)
    refracted_dir = np.subtract(
        np.cross(normal, -a) * wd.refractive_ratio,
        normal * math.sqrt(
            1 - (np.dot(normalize(a), normalize(a)) * wd.refractive_ratio**2)
        )
    )
    scaling = (data.water_depth - point[1]) / refracted_dir[1]
    return np.add(refracted_dir * scaling, point)


def GenerateCaustic(data, time):
    intensities = [0] * data.height * data.width
    a = data.height * wd.photon_range_multiplier[1] // 2
    b = data.width * wd.photon_range_multiplier[0] // 2
    z = -a
    while -a <= z < a:
        x = -b
        while -b <= x < b:
            y = wave_function(np.array([x / data.scale, z / data.scale]), data, time)
            face = np.array([x / data.scale, y, z / data.scale])
            hit = Refract(face, data, time)
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
            x += wd.refraction_step
        z += wd.refraction_step
    return [int(i) for i in intensities]
