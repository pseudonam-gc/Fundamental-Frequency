## Fundamental Frequency Finder

This project's goal is to find the fundamental frequencies of a given audio file, which is the lowest pitch detected. Autocorrelation is the primary function used, but other options may be added in the future for comparison and contrast. The freqeuncies of each timestamp are then plotted on a logarithmic graph, which also displays the estimated note values at each given time. There are three given examples, but users can also upload their own MP3s. 

Note that fundamental frequency detection is still largely an open problem, and may perform suboptimally with polyphony (multiple notes being played at once) or audio noise.

The program is written in Python and uses Librosa for audio processing and Statsmodels for autocorrelation. It auto-deploys to DockerHub and Render, and is available at [https://fundfrequency.kiok.org/](https://fundfrequency.kiok.org/). The website (as well as generated graphs) may take a minute to load at first, as the CPU is not very powerful, but subsequent requests should be much faster.

## Usage

The program can be run by executing `python3 app.py` in the terminal. 