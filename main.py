# A simple caustics generator
from PIL import Image
import numpy as np
from util import WaveData as wd
import wave
from util import normalize
import time
import multiprocessing
import random
import math


water_depth = -5
intensity_multiplier = 10
scale = 8
impact_range = 0
N = 10
frequency = []
direction = []
W = []
amplitude = []
steepness = []
random.seed(1234)
for i in range(N):
    frequency.append(random.uniform(0.001, 0.25))
    angle = random.uniform(0, math.pi * 2)
    direction.append(normalize(np.array([math.cos(angle), math.sin(angle)])))
    W.append(random.uniform(0.25, 0.75))
    amplitude.append(random.uniform(0.5, 1.5))
    steepness.append(random.uniform(0.25, 0.5))
k = 6 / 5

fps = 30
length = 10000
height = 1024  # Height of the image in pixels
width = height  # Width of the image in pixels
frame_count = 1 # fps * length // 1000

GenerateCaustic = wave.GenerateCaustic
Process = multiprocessing.Process
data = wd(
    water_depth,
    intensity_multiplier,
    scale,
    impact_range,
    N, frequency,
    W,
    direction,
    amplitude,
    steepness,
    k,
    width,
    height
)


def GetFrames(lower, upper):
    for i in range(lower, upper):
        name = "frames/caustic{}.png".format(i)
        try:
            open(name, 'r')
        except FileNotFoundError:
            im = Image.new('L', (height, width))
            dat = GenerateCaustic(data, i / fps)
            im.putdata(dat)
            im.save(name)


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        start_time = time.time()
        processes = []
        process_count = int(input("Enter # of available process: "))
        for i in range(process_count):
            lower = i * frame_count // process_count
            upper = (i + 1) * frame_count // process_count
            print("Process-" + str(i), "from: " + str(lower), "to: " + str(upper))
            p = Process(target=GetFrames, args=(lower, upper))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()
        GetFrames(frame_count - frame_count % process_count, frame_count)
        print(time.time() - start_time)
