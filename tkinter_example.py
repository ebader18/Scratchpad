import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Load an image using OpenCV
        cv_image = cv2.imread(file_path)
        # Convert the color from BGR to RGB
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        # Convert the OpenCV image to PIL format
        pil_image = Image.fromarray(cv_image)
        # Convert to Tkinter format
        global tk_image
        tk_image = ImageTk.PhotoImage(image=pil_image)
        # Update the image label
        image_label.config(image=tk_image)


def plot_graph():
    # Data for plotting
    t = list(range(100))
    s = [i**0.5 for i in t]

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='Example plot: Square root graph')
    ax.grid()

    # Embedding the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def on_checkbox_change():
    print("Checkbox is selected" if var_checkbox.get() else "Checkbox is deselected")


def on_radio_change():
    print(f"Selected option: {var_radio.get()}")


root = tk.Tk()
root.title("Tkinter and OpenCV Example")

# Create a frame for the buttons and inputs
frame_inputs = tk.Frame(root)
frame_inputs.pack(fill=tk.X)

# Button to load an image
btn_load = tk.Button(frame_inputs, text="Load Image", command=load_image)
btn_load.pack(side=tk.LEFT, padx=10, pady=10)

# Button to plot graph
btn_plot = tk.Button(frame_inputs, text="Plot Graph", command=plot_graph)
btn_plot.pack(side=tk.LEFT, padx=10, pady=10)

# Checkbox
var_checkbox = tk.IntVar()
checkbox = tk.Checkbutton(frame_inputs, text="Enable Option", variable=var_checkbox, command=on_checkbox_change)
checkbox.pack(side=tk.LEFT, padx=10)

# Radio buttons
var_radio = tk.StringVar(value="1")
radio1 = tk.Radiobutton(frame_inputs, text="Option 1", variable=var_radio, value="1", command=on_radio_change)
radio1.pack(side=tk.LEFT, padx=10)
radio2 = tk.Radiobutton(frame_inputs, text="Option 2", variable=var_radio, value="2", command=on_radio_change)
radio2.pack(side=tk.LEFT, padx=10)

# Horizontal slider
slider = tk.Scale(frame_inputs, from_=0, to=100, orient=tk.HORIZONTAL)
slider.pack(side=tk.LEFT, padx=10)

# Text box
text_box = tk.Entry(frame_inputs)
text_box.pack(side=tk.LEFT, padx=10)

# Label for displaying images
image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()
