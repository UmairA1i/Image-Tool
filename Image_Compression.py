import os
import sys
import numpy as np
from tkinter import Tk, Button, filedialog, simpledialog, messagebox
from PIL import Image


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS  # When running as exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


img = None
file_path = None

def open_image():
    global img, file_path
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff")]
    )
    if file_path:
        img = Image.open(file_path)
        messagebox.showinfo("Success", f"Loaded image: {os.path.basename(file_path)}")

def save_image(new_img, default_name="output.jpg"):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        initialfile=default_name,
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
    )
    if save_path:
        new_img.save(save_path)
        messagebox.showinfo("Saved", f"Image saved at:\n{save_path}")




def compress_image():
    if img:
        quality = simpledialog.askinteger("Input", "Enter quality (1–100):", minvalue=1, maxvalue=100)
        if quality:
            compressed = img.copy()
            save_image(compressed, "compressed.jpg")
            compressed.save("compressed.jpg", "JPEG", optimize=True, quality=quality)

def resize_image():
    if img:
        w = simpledialog.askinteger("Input", "Enter new width:")
        h = simpledialog.askinteger("Input", "Enter new height:")
        if w and h:
            resized = img.resize((w, h), Image.LANCZOS)
            save_image(resized, "resized.jpg")

def grayscale_image():
    if img:
        gray = img.convert("L")
        save_image(gray, "grayscale.jpg")

def rotate_image():
    if img:
        angle = simpledialog.askinteger("Input", "Enter rotation angle:")
        if angle is not None:
            rotated = img.rotate(angle, expand=True)
            save_image(rotated, "rotated.jpg")

def crop_image():
    if img:
        left = simpledialog.askinteger("Crop", "Left (x):")
        top = simpledialog.askinteger("Crop", "Top (y):")
        right = simpledialog.askinteger("Crop", "Right (x):")
        bottom = simpledialog.askinteger("Crop", "Bottom (y):")
        if None not in (left, top, right, bottom):
            cropped = img.crop((left, top, right, bottom))
            save_image(cropped, "cropped.jpg")

def upscale_image():
    """Normal upscale (up to 8K)"""
    if img:
        factor = simpledialog.askinteger("Upscale", "Enter upscale factor (2, 3, 4 or 8):", minvalue=2, maxvalue=8)
        if factor:
            w, h = img.size
            new_w, new_h = w * factor, h * factor

            # Cap at 8K (7680×4320)
            new_w = min(new_w, 7680)
            new_h = min(new_h, 4320)

            upscaled = img.resize((new_w, new_h), Image.LANCZOS)
            save_image(upscaled, "upscaled_8k.jpg")

def upscale_bicubic():
    """Fast Bicubic upscale"""
    if img:
        factor = 4  # fixed 4x upscale
        w, h = img.size
        upscaled = img.resize((w * factor, h * factor), Image.BICUBIC)
        save_image(upscaled, "bicubic_upscaled.jpg")


# GUI Setup
root = Tk()
root.title("All-in-One Image Tool")
root.geometry("320x600")

Button(root, text="Open Image", command=open_image).pack(pady=10)
Button(root, text="Compress Image", command=compress_image).pack(pady=5)
Button(root, text="Resize Image", command=resize_image).pack(pady=5)
Button(root, text="Grayscale", command=grayscale_image).pack(pady=5)
Button(root, text="Rotate", command=rotate_image).pack(pady=5)
Button(root, text="Crop", command=crop_image).pack(pady=5)
Button(root, text="Upscale (up to 8K)", command=upscale_image).pack(pady=5)
Button(root, text="AI Upscale - Bicubic (fastest)", command=upscale_bicubic).pack(pady=5)

root.mainloop()
