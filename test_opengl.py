import glfw
from OpenGL.GL import *
import numpy as np

# Global viewport and zoom settings
window_width, window_height = 800, 600
viewport_x, viewport_y = 0, 0
zoom_level = 1.0
zoom_factor = 1.1
NUMBER_OF_POINTS = 1000000
point_size = 0.1

def key_callback(window, key, scancode, action, mods):
    global zoom_level

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_UP:
            zoom_level *= zoom_factor  # Zoom in
        elif key == glfw.KEY_DOWN:
            zoom_level /= zoom_factor  # Zoom out
        #zoom_level = max(0.1, min(100.0, zoom_level))  # Ensure a valid zoom level
        print("Zoom level: {:.2f}".format(zoom_level))

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(window_width, window_height, "Colored Points", None, None)
    if not window:
        glfw.terminate()
        return

    # Setup input callbacks
    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to dark gray
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glPointSize(point_size)  # Set point size for visibility

    # Generate points and colors
    x_coords = np.random.rand(NUMBER_OF_POINTS) * 2 - 1
    y_coords = np.random.rand(NUMBER_OF_POINTS) * 2 - 1
    points = np.column_stack((x_coords, y_coords)).astype(np.float32)
    colors = np.random.rand(NUMBER_OF_POINTS, 3).astype(np.float32)  # RGB colors for each point

    # Buffer the points
    VBO1 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO1)
    glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # Buffer the colors
    VBO2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO2)
    glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # Unbind buffers
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Main loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # Implement Zoom using translation
        glLoadIdentity()  # Reset transformations
        glScalef(zoom_level, zoom_level, 1)  # Scale uniformly in X and Y dimensions

        glPointSize(point_size * zoom_level)

        # Draw points with their corresponding colors
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glBindBuffer(GL_ARRAY_BUFFER, VBO1)
        glVertexPointer(2, GL_FLOAT, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, VBO2)
        glColorPointer(3, GL_FLOAT, 0, None)

        glDrawArrays(GL_POINTS, 0, NUMBER_OF_POINTS)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        # Swap the buffers
        glfw.swap_buffers(window)

        # Poll for events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
