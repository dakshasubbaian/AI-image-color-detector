---
# AI Image Color Detector - README

## Project Overview

This is a simple Python GUI application that allows you to open any image and click on a pixel to get its exact color in HEX format. The app displays the HEX color code and copies it automatically to your clipboard for easy use.

---

## Features

* Open common image formats (`.jpg`, `.png`, `.bmp`, `.gif`, etc.) using a file dialog.
* Display the image resized to fit the window while preserving aspect ratio.
* Click on any pixel in the image to:

  * Retrieve the pixel’s color value.
  * Convert the color from BGR (OpenCV format) to HEX format.
  * Show the HEX color code on the app with the label background set to that color.
  * Automatically copy the HEX code to the clipboard.

---

## How It Works

1. **Image Loading and Display**
   When you click the "Open Image" button, a file dialog opens for you to select an image. The image is read using OpenCV (`cv2.imread`) in BGR format.
   If the image is larger than 800 pixels in any dimension, it is resized proportionally to fit the display window.
   The resized image is converted to RGB and then to a format usable by Tkinter (`PhotoImage`) for display on a canvas widget.

2. **Color Picking**
   When you click anywhere on the displayed image, the app calculates the corresponding pixel position in the original (full-resolution) image by accounting for any resizing scale.
   It fetches the BGR color value of that pixel, converts it to a HEX color string, updates the status label with this HEX color, changes the label’s background to that color for visual feedback, and copies the HEX code to your clipboard.

---

## Dependencies

* Python 3.x
* OpenCV (`opencv-python`) — for image loading and processing
* Tkinter (built-in with Python) — for GUI elements
* Pillow (`PIL`) — to interface OpenCV images with Tkinter
* Pyperclip — to copy HEX color to clipboard automatically

Install dependencies with:

```bash
pip install opencv-python pillow pyperclip
```

---

## How to Run

1. Save the script as `color_picker_app.py`.
2. Run the script:

```bash
python color_picker_app.py
```

3. Click **Open Image** and select an image file.
4. Click anywhere on the image to get the HEX color of that pixel.
5. The HEX code will appear on the label and be copied to your clipboard.

---

## Notes

* The app ensures that color picking corresponds accurately to the original image pixels regardless of resizing.
* The label’s background changes to the selected color with white text for readability.
* Clipboard support allows quick use of colors in design or development.

---
