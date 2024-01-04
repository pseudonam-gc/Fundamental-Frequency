#import sox
from mutagen.mp3 import MP3
import time
import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks

def audioLength(path):
    try: 
        audio = MP3(path)
        return audio.info.length
    except:
        return 0

def generateImage(filename, durationLimit=5):
    matplotlib.use('Agg')
    # Code from https://scicoding.com/pitchdetection/

    # Load data and sampling frequency from the data file

    # check duration of audio
    actualDuration = audioLength(f'temp_audio/{filename}.mp3')
    if actualDuration < durationLimit:
        data, sampling_frequency = librosa.load(f'temp_audio/{filename}.mp3', duration=actualDuration)
    else:
        data, sampling_frequency = librosa.load(f'temp_audio/{filename}.mp3', duration=durationLimit)

    #T = 1/sampling_frequency # Sampling period
    #N = len(data) # Signal length in samples
    #t = N / sampling_frequency # Signal length in seconds

    #frame_size = 5000
    frame_size = 5000
    step = 30
    pitches = []

    def find_pitch(d, t):
        if step*t+frame_size >= len(d):
            return 0
        data = d[step*t:step*t+frame_size]
        auto = sm.tsa.acf(data, nlags=frame_size)
        peaks = find_peaks(auto)[0] # Find peaks of the autocorrelation

        lag = (peaks[-1]-peaks[0])/(len(peaks)-1)
        pitch = sampling_frequency / lag # Transform lag into frequency
        return (pitch)

    for i in range(0, len(data), step):
        f = find_pitch(data, i)
        if f != 0:
            if i / sampling_frequency * step < durationLimit:
                pitches.append((i / sampling_frequency * step, f))
            else:
                break

    fig, ax = plt.subplots()
    # set the x ticks
    #ax.set_xticks(np.arange(0, len(pitches), len(pitches)/10))
    #ax.set_yticks(np.arange(200, 600))
    plt.plot(*zip(*pitches))
    plt.xlabel('time (s)')
    plt.ylabel('pitch (Hz)')


    # return plt as an image
    plt.savefig(f'temp_images/{filename}.png')
    return pitches

    # save plt as fe.png

generateImage('tf')