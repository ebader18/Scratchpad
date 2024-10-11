import cv2, numpy as np, pyautogui, time, math

palette = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Cyan
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Yellow
    (192, 192, 192),# Light Gray
    (128, 0, 0),    # Maroon
    (128, 128, 0),  # Olive
    (0, 128, 128)   # Teal
]
filepath = 'C:/_SW/eb_python/_images/DSC_0303.JPG'
#filepath = 'C:/_SW/eb_python/_images/beautiful_landscape_4k.jpg'
#filepath = 'C:/_SW/eb_python/_images/Mountain/pexels-photo-174523_1.png'
height, width = 1080, 1920
num_zones = 7
sequence = {
    "type": "geometric",
    "min": 0.1,
    "max": 1,
    "num_zones": 3
}

class foveated_rendering:
    def __init__(self, path_img, dim_img, sequence):
        self.indented_text = ' ' * 3
        self.path = path_img
        self.width, self.height = dim_img
        self.sequence = sequence
        self.images = {}
        self.images['diameter'] = self.GenerateZones()
        self.images['binned'] = self.GenerateBinnedImages()
        self.summary = self.ComputeRenderedPixel()
    
    def GenerateZones(self):
        if self.sequence["type"] == 'geometric':
            self.diam_zones = np.geomspace(self.sequence["min"], self.sequence["max"], self.sequence["num_zones"])
        elif self.sequence["type"] == 'linear':
            self.diam_zones = np.linspace(self.sequence["min"], self.sequence["max"], self.sequence["num_zones"])
        return self.diam_zones

    def GenerateBinnedImages(self):
        img = []
        orignal_img = cv2.imread(self.path)
        orignal_img = cv2.resize(orignal_img, (self.width, self.height), interpolation=cv2.INTER_AREA)
        img.append(orignal_img)
        for factor in range(2, self.sequence["num_zones"] + 2):
            new_width, new_height = int(self.width / factor), int(self.height / factor)
            tmp_img = cv2.resize(img[0], (new_width, new_height), interpolation=cv2.INTER_AREA)        # INTER_NEAREST, INTER_LINEAR, INTER_AREA, INTER_CUBIC, and INTER_LANCZOS4
            tmp_img = cv2.resize(tmp_img, (self.width, self.height), interpolation=cv2.INTER_LINEAR)        # INTER_NEAREST, INTER_LINEAR, INTER_AREA, INTER_CUBIC, and INTER_LANCZOS4
            img.append(tmp_img)
        return img

    def ComputeRenderedPixel(self):
        total_pixel = self.height * self.width
        summary = "1x1: <{:.1f}%".format(self.images['diameter'][0] * 100.0) + self.indented_text
        rendered_pixel = math.pi * (self.images['diameter'][0] * self.height / 2.0)**2
        for zone in range(self.sequence["num_zones"] - 1):
            summary += str(zone + 2) + "x" + str(zone + 2) + ": <{:.1f}%".format(self.images['diameter'][zone + 1] * 100.0) + self.indented_text
            inner_area = math.pi * (self.images['diameter'][zone] * self.height / 2.0)**2
            outer_area = math.pi * (self.images['diameter'][zone + 1] * self.height / 2.0)**2
            diff_area = (outer_area - inner_area) / (zone + 2)**2
            rendered_pixel += diff_area
        summary += str(self.sequence["num_zones"] + 1) + "x" + str(self.sequence["num_zones"] + 1) + ": remaining"
        inner_area = math.pi * (self.images['diameter'][-1] * self.height / 2.0)**2
        diff_area = (total_pixel - inner_area) / (self.sequence["num_zones"] + 1)**2
        rendered_pixel += diff_area
        pixel_reduction = 100.0 * rendered_pixel / total_pixel
        summary = "{:.1f}% pixels rendered".format(pixel_reduction) + self.indented_text + summary
        return summary

    def RenderFrame(self, center):
        combined_image = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        mask = 255*np.ones((self.height, self.width, 3), dtype=np.uint8)
        radius = int(self.images['diameter'][self.sequence["num_zones"] - 1] * self.height / 2.0)
        cv2.circle(mask, center, radius, (0, 0, 0), -1)
        circular_region = cv2.bitwise_and(self.images['binned'][self.sequence["num_zones"]], mask)
        combined_image = cv2.add(combined_image, circular_region)

        for i in range(1, self.sequence["num_zones"]):
            mask = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            outer_radius = int(self.images['diameter'][self.sequence["num_zones"] - i] * self.height / 2.0)
            inner_radius = int(self.images['diameter'][self.sequence["num_zones"] - i - 1] * self.height / 2.0)
            cv2.circle(mask, center, outer_radius, (255, 255, 255), -1)
            cv2.circle(mask, center, inner_radius, (0, 0, 0), -1)
            circular_region = cv2.bitwise_and(self.images['binned'][self.sequence["num_zones"] - i], mask)
            combined_image = cv2.add(combined_image, circular_region)
        
        mask = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        radius = int(self.images['diameter'][0] * self.height / 2.0)
        cv2.circle(mask, center, radius, (255, 255, 255), -1)
        circular_region = cv2.bitwise_and(self.images['binned'][0], mask)
        combined_image = cv2.add(combined_image, circular_region)

        return combined_image

    def AddInfoToFrame(self, frame, fps):
        cv2.rectangle(frame, (0, 0), (self.width, 110), (255, 255, 255), thickness=-1)
        cv2.putText(frame, "{:.1f} fps".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(frame, self.summary, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return frame

fov_ren = foveated_rendering(filepath, (width, height), sequence)
print(fov_ren.summary)

cv2.namedWindow('Resized Image', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Resized Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while True:
    start_time = time.time()
    frame = fov_ren.RenderFrame(pyautogui.position())
    fps = 1.0 / (time.time() - start_time)

    frame = fov_ren.AddInfoToFrame(frame, fps)
    cv2.imshow('Resized Image', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):     # Quit
        print('Exit')
        break
    elif key == ord('a'):   # Add a zone
        print("Add binning zones")
    elif key == ord('d'):   # Remove a zone
        print("Remove binning zones")
    elif key == ord('g'):   # Apply geometrical sequence to zones assignment
        print("Apply geometrical sequence to zones assignment")
    elif key == ord('l'):   # Apply linear sequence to zones assignment
        print("Apply linear sequence to zones assignment")
    elif key == ord('w'):   # Move to next image
        print("Move to next image")
    elif key == ord('s'):   # Move to previous image
        print("Move to previous image")

cv2.destroyAllWindows()