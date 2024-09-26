import numpy as np
import cv2
import pyaudio

# Constants
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WIDTH = CHUNK // 4
HEIGHT = 400
MIN_MAGNITUDE = 0.0001
MAX_MAGNITUDE = 1.0

# Additional dimensions for text and labels
FRAME_HEIGHT = HEIGHT + 125  # Extra space for title and labels
FRAME_WIDTH = WIDTH + 50    # Extra space for y-axis labels

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize the image
frame = np.ones((FRAME_HEIGHT, FRAME_WIDTH * 4, 3), dtype=np.uint8) * 255
cv2.putText(frame, 'Real-time Audio Spectrogram', (FRAME_WIDTH*4//2-175, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
cv2.putText(frame, f'Sampling rate: {RATE}Hz', (FRAME_WIDTH*4//2-175, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
cv2.putText(frame, 'Frequency (kHz)', (FRAME_WIDTH*4//2-100, 95+HEIGHT), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Initialize the spectrogram image
spectrogram_img = np.zeros((HEIGHT, WIDTH, 1), dtype=np.uint8)


def update_image(data):
    global spectrogram_img
    # Shift spectrogram up
    spectrogram_img[:-1] = spectrogram_img[1:]  # Shift image up

    # Compute FFT and update the last row
    fft_data = np.fft.rfft(np.frombuffer(data, dtype=np.float32))
    fft_magnitude = np.abs(fft_data)

    # Normalize using fixed maximum and minimum values for consistency
    if True:
        log_fft = np.log1p(fft_magnitude)
        normalized = (log_fft - np.log1p(MIN_MAGNITUDE)) / (np.log1p(MAX_MAGNITUDE) - np.log1p(MIN_MAGNITUDE))
        normalized = np.clip(normalized, 0, 1)  # Ensure values are within [0, 1]
        normalized = normalized[:len(normalized)//2]
        scaled_colors = np.array(normalized * 255, dtype=np.uint8)

    # Update last row of spectrogram image
    spectrogram_img[-1, :] = scaled_colors.reshape(-1, 1)  # Convert row to 2D for single channel

    # Apply color map
    colored_spectrogram = cv2.applyColorMap(spectrogram_img, cv2.COLORMAP_HOT)

    # Place the colored spectrogram in the frame
    frame[75:75+HEIGHT, 100:100+WIDTH*4] = cv2.resize(colored_spectrogram, (WIDTH * 4, HEIGHT), interpolation=cv2.INTER_CUBIC)


try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        update_image(data)
        cv2.imshow('Spectrogram with Labels', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    cv2.destroyAllWindows()
