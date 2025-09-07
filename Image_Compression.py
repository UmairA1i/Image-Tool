import os
from tkinter import Tk, Button, filedialog, simpledialog, messagebox
from PIL import Image
from PIL import ImageFilter

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


def save_image(new_img, default_name="output.jpg", quality=None, optimize=False):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        initialfile=default_name,
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
    )
    if save_path:
        fmt = os.path.splitext(save_path)[1].upper().lstrip('.')
        if fmt in ('JPG', 'JPEG') and (quality or optimize):
            new_img = new_img.convert("RGB") if new_img.mode != "RGB" else new_img
            new_img.save(save_path, "JPEG", quality=quality, optimize=optimize)
        else:
            new_img.save(save_path)
        messagebox.showinfo("Saved", f"Image saved at:\n{save_path}")


def compress_image():
    if img:
        quality = simpledialog.askinteger("Input", "Enter quality (1–100):", minvalue=1, maxvalue=100)
        if quality:
            save_image(img, "compressed.jpg", quality=quality, optimize=True)


def resize_image():
    if not img:
        messagebox.showerror("Error", "Please open an image first.")
        return
    preserve = messagebox.askyesno("Resize", "Preserve aspect ratio?")
    w, h = img.size
    if preserve:
        new_w = simpledialog.askinteger("Input", "Enter new width (height auto-adjusts):")
        if new_w:
            new_h = int(h * (new_w / w))
    else:
        new_w = simpledialog.askinteger("Input", "Enter new width:")
        new_h = simpledialog.askinteger("Input", "Enter new height:")
    if new_w and new_h and new_w > 0 and new_h > 0:
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        save_image(resized, "resized.jpg")
    else:
        messagebox.showerror("Error", "Invalid dimensions.")


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
            if left >= right or top >= bottom:
                messagebox.showerror("Error", "Invalid dimensions: left < right and top < bottom required.")
                return
            cropped = img.crop((left, top, right, bottom))
            save_image(cropped, "cropped.jpg")


def upscale_image():
    if img:
        factor = simpledialog.askinteger("Upscale", "Enter upscale factor (2, 3, 4 or 8):", minvalue=2, maxvalue=8)
        if factor:
            w, h = img.size
            max_factor_w = 7680 / w
            max_factor_h = 4320 / h
            capped_factor = min(factor, max_factor_w, max_factor_h)
            new_w = int(w * capped_factor)
            new_h = int(h * capped_factor)
            upscaled = img.resize((new_w, new_h), Image.LANCZOS)
            upscaled = upscaled.filter(ImageFilter.SHARPEN)
            save_image(upscaled, "upscaled_8k.jpg")


def upscale_bicubic():
    if img:
        factor = simpledialog.askinteger("Upscale", "Enter upscale factor (2-8):", minvalue=2, maxvalue=8)
        if factor:
            w, h = img.size
            upscaled = img.resize((w * factor, h * factor), Image.BICUBIC)
            upscaled = upscaled.filter(ImageFilter.SHARPEN)
            save_image(upscaled, f"bicubic_upscaled_{factor}x.jpg")
           

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
Button(root, text="Bicubic Upscale (fastest)", command=upscale_bicubic).pack(pady=5)

root.mainloop()
