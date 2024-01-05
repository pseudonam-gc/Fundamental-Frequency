from pitches import * 
import pytest
import math
epsilon = 0.001

def test_audioLength():
    assert abs(audioLength('temp_audio/tf.mp3')-3.1085625) < epsilon
    with pytest.raises(FileNotFoundError):
        audioLength('temp_audio/non_file.mp3')

def test_pitch_acf():
    data = [math.sin(i)*300+300 for i in range(10000)]
    sampling_frequency = 44100
    time = 0

    #print (pitch_acf(data, sampling_frequency, time))
    assert abs(pitch_acf(data, sampling_frequency, time)-7018.5207456) < epsilon

def test_returnPitches():
    assert abs(sum([i.pitch for i in returnPitches('tf')])-31286.8590553) < epsilon
    assert abs(sum([i.time for i in returnPitches('tf')])-101.428571428) < epsilon
