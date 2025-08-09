import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyperclip
import os

def bgr_to_hex(bgr):
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def open_image():
    global img, orig_img, tk_img, orig_w, orig_h, SCALE, disp_img

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )

    if not file_path:
        return

    orig_img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if orig_img is None:
        status_label.config(text="Error loading image")
        return

    orig_h, orig_w = orig_img.shape[:2]

    MAX_DIM = 800
    SCALE = 1.0
    if max(orig_w, orig_h) > MAX_DIM:
        SCALE = MAX_DIM / max(orig_w, orig_h)
    disp_w, disp_h = int(orig_w * SCALE), int(orig_h * SCALE)
    disp_img = cv2.resize(orig_img, (disp_w, disp_h), interpolation=cv2.INTER_AREA) if SCALE != 1.0 else orig_img.copy()

    img_rgb = cv2.cvtColor(disp_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    tk_img = ImageTk.PhotoImage(img_pil)

    canvas.config(width=disp_w, height=disp_h)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    status_label.config(text="Click anywhere on the image to get HEX color")


def on_click(event):
    if orig_img is None:
        return
    ox = min(int(event.x / SCALE), orig_w - 1)
    oy = min(int(event.y / SCALE), orig_h - 1)
    bgr = orig_img[oy, ox]
    hex_color = bgr_to_hex(bgr)

    # Copy to clipboard
    pyperclip.copy(hex_color)

    # Change label text & background to the clicked color
    status_label.config(text=f"HEX: {hex_color}", bg=hex_color, fg="white")

# Main Tkinter window
root = tk.Tk()
root.title("AI Image Color Detector")

# Buttons & status
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
open_btn = tk.Button(btn_frame, text="Open Image", command=open_image)
open_btn.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="Choose an image to start", font=("Arial", 12))
status_label.pack(pady=5)

# Canvas for image display
canvas = tk.Canvas(root)
canvas.pack()
canvas.bind("<Button-1>", on_click)

# Globals
orig_img = None
SCALE = 1.0
orig_w = orig_h = 0
tk_img = None
disp_img = None

root.mainloop()
