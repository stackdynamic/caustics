# A simple caustics generator
from PIL import Image
import numpy as np
from wave_data import WaveData as wd
import wave
from util import normalize
import time
import multiprocessing


water_depth = -5
intensity_multiplier = 5
scale = 9
impact_range = 0
N = 2
frequency = [0.01, 0.02, 0.05]
W = [1 / 4, 4 / 9, 9 / 16]
direction = [normalize(np.array([-1, -1 / 4])),
             normalize(np.array([1, 1])),
             normalize(np.array([1, 1 / 16]))]
amplitude = [4, 9 / 4, 16 / 9]
steepness = [0.3, 0.4, 0.5]
k = 6 / 5

fps = 5
length = 1000
height = 512  # Height of the image in pixels
width = height  # Width of the image in pixels
frame_count = fps * length // 1000

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


def GetFrames(lower, upper, frames):
    for i in range(lower, upper):
        im = Image.new('L', (height, width))
        dat = GenerateCaustic(data, i/fps)
        im.putdata(dat)
        frames[i] = im


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        start_time = time.time()
        processes = []
        frames = manager.list([None] * frame_count)
        process_count = int(input("Enter # of available process: "))
        for i in range(process_count):
            lower = i * frame_count // process_count
            upper = (i + 1) * frame_count // process_count
            print("Process-" + str(i), "from: " + str(lower), "to: " + str(upper))
            p = Process(target=GetFrames, args=(lower, upper, frames))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()
        GetFrames(frame_count - frame_count % process_count, frame_count, frames)
        frames[0].save("Caustic.gif",
                       save_all=True,
                       append_images=frames[1:],
                       duration=1 / fps,
                       loop=0)
        print(time.time() - start_time)
