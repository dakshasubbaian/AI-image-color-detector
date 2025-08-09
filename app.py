# color_picker.py
import cv2
import argparse
import os

# optional clipboard copy
try:
    import pyperclip
    CLIPBOARD = True
except Exception:
    CLIPBOARD = False

def bgr_to_hex(bgr):
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def on_mouse(event, x, y, flags, param):
    # left click -> get original-image coords and show hex
    if event == cv2.EVENT_LBUTTONDOWN:
        global SCALE, orig_img, disp_img, orig_w, orig_h, window_name
        ox = min(int(x / SCALE), orig_w - 1)
        oy = min(int(y / SCALE), orig_h - 1)
        bgr = orig_img[oy, ox]
        hexc = bgr_to_hex(bgr)
        print(f"{hexc}  (x={ox}, y={oy})")
        if CLIPBOARD:
            pyperclip.copy(hexc)
            print("Copied to clipboard.")
        # quick visual feedback on window (optional)
        tmp = disp_img.copy()
        cv2.rectangle(tmp, (5,5), (160,40), (int(bgr[0]),int(bgr[1]),int(bgr[2])), -1)
        cv2.putText(tmp, hexc, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow(window_name, tmp)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("image", nargs="?", help="Path to image file")
    args = p.parse_args()

    path = args.image
    if path is None:
        # fallback to ask for path in console
        path = input("Image path: ").strip()

    if not os.path.isfile(path):
        print("File not found:", path)
        raise SystemExit(1)

    orig_img = cv2.imread(path, cv2.IMREAD_COLOR)
    if orig_img is None:
        print("Failed to read image. Supported formats: jpg, png, etc.")
        raise SystemExit(1)

    orig_h, orig_w = orig_img.shape[:2]

    # scale down for display if huge (maps clicks back to original)
    MAX_DIM = 1000
    SCALE = 1.0
    if max(orig_w, orig_h) > MAX_DIM:
        SCALE = MAX_DIM / max(orig_w, orig_h)
    disp_w, disp_h = int(orig_w * SCALE), int(orig_h * SCALE)
    disp_img = cv2.resize(orig_img, (disp_w, disp_h), interpolation=cv2.INTER_AREA) if SCALE != 1.0 else orig_img.copy()

    window_name = "Click a pixel - press Q or ESC to quit"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(window_name, disp_img)
    cv2.setMouseCallback(window_name, on_mouse)

    print("Click any pixel in the image window. Press Q or ESC to quit.")
    while True:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
        key = cv2.waitKey(20) & 0xFF
        if key == ord("q") or key == 27:
            break

    cv2.destroyAllWindows()
