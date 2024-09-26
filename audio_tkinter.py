import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyaudio
import numpy as np
import queue
import threading

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

# Audio queue
audio_queue = queue.Queue()


def audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        audio_queue.put(data)

    stream.stop_stream()
    stream.close()
    p.terminate()


def update_plot():
    try:
        data = audio_queue.get_nowait()
        # Update time domain plot
        line1.set_ydata(data)
        # Compute and update frequency domain plot
        fft_data = np.fft.fft(data)
        fft_freq = np.fft.fftfreq(len(fft_data), 1 / RATE)
        line2.set_data(fft_freq[:CHUNK // 2], np.abs(fft_data)[:CHUNK // 2])
        ax2.relim()
        ax2.autoscale_view()
        canvas.draw()
    except queue.Empty:
        pass
    root.after(10, update_plot)


# Set up the GUI
root = tk.Tk()
root.title("Real-Time Audio Plot")

fig = Figure(figsize=(10, 8))

# Subplot for time domain data
ax1 = fig.add_subplot(211)
x = np.linspace(0, CHUNK-1, CHUNK)
line1, = ax1.plot(x, np.zeros(CHUNK))
ax1.set_title("Time Domain")
ax1.set_ylim(-30000, 30000)

# Subplot for frequency domain data
ax2 = fig.add_subplot(212)
ax2.set_yscale('log')
line2, = ax2.plot([], [], 'r')
ax2.set_title("Frequency Domain")
ax2.set_xlim(0, RATE // 4)
ax2.set_ylim(100, 10000000)  # May need to adjust depending on the magnitude of FFT

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Start the audio thread
thread = threading.Thread(target=audio_stream)
thread.daemon = True
thread.start()

# Start the GUI update
update_plot()

root.mainloop()
