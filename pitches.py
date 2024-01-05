#import sox
import time
import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from mutagen.mp3 import MP3
from scipy.signal import find_peaks
from collections import namedtuple

# a named tuple to store the time and pitch of a note
timed_pitch = namedtuple('timed_pitch', ['time', 'pitch'])

# hyperparameters, can be tuned.
# frame_size is the number of later points to consider when calculating the autocorrelation
# we only calculate the autocorrel. every step points for time reasons
frame_size = 5000
step = 30

def pitch_acf(data, sampling_frequency, time): # uses autocorrelation to find pitch
    global frame_size, step
    if step*time+frame_size >= len(data):
        raise IndexError
    data = data[step*time:step*time+frame_size] # find the data in the relevant timerame
    auto = sm.tsa.acf(data, nlags=frame_size) # calculate autocorrelation
    peaks = find_peaks(auto)[0] # Find peaks of the autocorrelation

    lag = (peaks[-1]-peaks[0])/(len(peaks)-1) # find the average distance between peaks
    pitch = sampling_frequency / lag # transform lag into frequency
    return (pitch)

def audioLength(path):
    try: 
        audio = MP3(path)
        return audio.info.length
    except:
        raise FileNotFoundError

def returnPitches(filename, durationLimit=5):
    matplotlib.use('Agg')
    # Code from https://scicoding.com/pitchdetection/
    # check duration of audio
    actualDuration = audioLength(f'temp_audio/{filename}.mp3')
    # load audio into data, find sampling_frequency
    if actualDuration < durationLimit:
        data, sampling_frequency = librosa.load(f'temp_audio/{filename}.mp3', duration=actualDuration)
    else:
        data, sampling_frequency = librosa.load(f'temp_audio/{filename}.mp3', duration=durationLimit)
    
    pitches = []

    for i in range(0, len(data), step):
        # check if an index error is raised
        try:
            f = pitch_acf(data, sampling_frequency, i)
            if i / sampling_frequency * step < durationLimit:
                pitches.append(timed_pitch(i / sampling_frequency * step, f))
            else:
                break
        except IndexError:
            break

    # plots pitches, but this feature will be unused as we will be returning the pitches instead
    fig, ax = plt.subplots()
    plt.plot(*zip(*pitches))
    plt.xlabel('time (s)')
    plt.ylabel('pitch (Hz)')

    # return plt as an image
    plt.savefig(f'temp_images/{filename}.png')
    return pitches
