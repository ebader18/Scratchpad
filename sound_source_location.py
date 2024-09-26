from scipy.io import wavfile
import numpy as np

def calculate_tdoa(signal1, signal2, fs):
    corr = np.correlate(signal1, signal2, 'full')
    delay = np.argmax(corr) - (len(signal1) - 1)
    time_delay = delay / float(fs)
    return time_delay

signals = []
sample_rates = []
for i in range(1, 9):
    sr, data = wavfile.read(f'audio{i}.wav')
    signals.append(data)
    sample_rates.append(sr)

assert len(set(sample_rates)) == 1, "All audio files should have the same sample rate"
sample_rate = sample_rates[0]

tdoa = calculate_tdoa(signals[0], signals[1], sample_rate)
print(f'The time delay between signal 1 and signal 2 is: {tdoa} seconds.')
