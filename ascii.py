import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

ASCII_CHARS = "@%#*+=-:. "

class ASCIIConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Image Converter")

        self.input_image_path = tk.StringVar()
        self.output_image_path = tk.StringVar()

        self.range_width = tk.DoubleVar(value=20)
        self.font_size = tk.DoubleVar(value=10)

        self.input_placeholder_image = Image.new("RGB", (400, 400), "white")
        self.output_placeholder_image = Image.new("RGB", (400, 400), "white")

        self.image_frame = tk.Frame(self.root)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        self.side_bar = tk.Frame(self.root)
        self.side_bar.grid(row=0, column=1, padx=10, pady=10)

        self.create_widgets()
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def create_widgets(self):
        self.show_input_image(self.input_placeholder_image, parent_frame=self.image_frame)
        self.show_output_image(self.output_placeholder_image, parent_frame=self.image_frame)

        browse_input_frame = tk.Frame(self.side_bar)
        browse_input_frame.pack(pady=5)

        tk.Label(browse_input_frame, text="Browse Input Image:", anchor="w").pack(side="top", fill="x")

        path_button_frame = tk.Frame(browse_input_frame)
        path_button_frame.pack(side="top", fill="x")

        self.input_image_path_entry = tk.Entry(path_button_frame, width=40, state="readonly")
        self.input_image_path_entry.pack(side="left", padx=5, fill="x")

        tk.Button(path_button_frame, text="Select Image", command=self.browse_input_image).pack(side="left", padx=5)

        browse_output_frame = tk.Frame(self.side_bar)
        browse_output_frame.pack(side="top", fill="x")

        tk.Label(browse_output_frame, text="Select Output Folder:", anchor="w").pack(side="top", fill="x")

        self.output_folder_path_entry = tk.Entry(browse_output_frame, width=40, state="readonly")
        self.output_folder_path_entry.pack(side="left", padx=5, fill="x")

        tk.Button(browse_output_frame, text="Select Folder", command=self.browse_output_folder).pack(side="left", padx=5)

        range_width_frame = tk.Frame(self.side_bar)
        range_width_frame.pack(pady=5)

        tk.Label(range_width_frame, text="Range Width:", anchor="w").pack(side="top", fill="x")

        scale = tk.Scale(range_width_frame, variable=self.range_width, from_=1.0, to=50.0, orient="horizontal", resolution=1.0, showvalue=False, label=None)
        scale.pack(side="top", padx=5, fill="x")
        tk.Label(range_width_frame, width=2, textvariable=self.range_width).pack(side="top", padx=2)

        font_size_frame = tk.Frame(self.side_bar)
        font_size_frame.pack(pady=5)

        tk.Label(font_size_frame, text="Font Size:", anchor="w").pack(side="top", fill="x")

        font_size_scale = tk.Scale(font_size_frame, variable=self.font_size, from_=5, to=15, orient="horizontal", resolution=1, showvalue=False, label=None)
        font_size_scale.pack(side="top", padx=5, fill="x")
        tk.Label(font_size_frame, width=2, textvariable=self.font_size).pack(side="top", padx=2)

        tk.Button(self.side_bar, text="Convert", command=self.convert_image).pack(pady=10, fill="x")


    def update_input_image_path_entry(self, path):
        self.input_image_path_entry.config(state="normal")
        _, last_portion = os.path.split(path)
        self.input_image_path_entry.delete(0, "end")
        self.input_image_path_entry.insert(0, last_portion)
        self.input_image_path_entry.config(state="readonly")

    def update_output_folder_path_entry(self, path):
        self.output_folder_path_entry.config(state="normal")
        self.output_folder_path_entry.delete(0, "end")
        self.output_folder_path_entry.insert(0, path)
        self.output_folder_path_entry.config(state="readonly")

    def browse_input_image(self):
        file_path = filedialog.askopenfilename(title="Select Input Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.input_image_path.set(file_path)
            self.show_input_image(parent_frame=self.image_frame)
            self.update_input_image_path_entry(file_path)

    def browse_output_folder(self):
        output_folder_path = filedialog.askdirectory(title="Select Output Folder")
        if output_folder_path:
            self.output_image_path.set(output_folder_path)
            self.update_output_folder_path_entry(output_folder_path)

    def show_input_image(self, image=None, parent_frame=None):
        if image is None:
            image_path = self.input_image_path.get()
            if image_path:
                image = Image.open(image_path)

        max_width = 400
        max_height = 400
        width, height = image.size
        aspect_ratio = width / height

        if aspect_ratio > 1:
            new_width = min(width, max_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, max_height)
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        input_image_label = tk.Label(parent_frame, image=photo)
        input_image_label.image = photo
        input_image_label.grid(row=0, column=0, padx=10, pady=10)

    def convert_image(self):
        input_path = self.input_image_path.get()
        output_folder_path = self.output_image_path.get()

        if not input_path or not output_folder_path:
            return

        input_dir, input_filename = os.path.split(input_path)
        output_filename = f"{os.path.splitext(input_filename)[0]}-ascii.png"
        output_path = os.path.join(output_folder_path, output_filename)

        font_size = int(self.font_size.get())

        create_ascii_image(input_path, output_path, new_width=100, range_width=self.range_width.get(), font_size=font_size)

        self.show_output_image(Image.open(output_path), parent_frame=self.image_frame)

    def show_output_image(self, image=None, parent_frame=None):
        if image is None:
            image_path = self.output_image_path.get()
            if image_path:
                image = Image.open(image_path)

        max_width = 400
        max_height = 400
        width, height = image.size
        aspect_ratio = width / height

        if aspect_ratio > 1:
            new_width = min(width, max_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, max_height)
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        output_image_label = tk.Label(parent_frame, image=photo)
        output_image_label.image = photo
        output_image_label.grid(row=0, column=1, padx=10, pady=10)

def resize_image(image, new_width=100):
    height, width, _ = image.shape
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def pixels_to_ascii(image, range_width=20):
    pixels = image.flatten()
    ascii_str = ""
    for pixel_value in pixels:
        inverted_pixel_value = 255 - pixel_value
        normalized_pixel = int(inverted_pixel_value / range_width)
        index = min(normalized_pixel, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def create_ascii_image(input_path, output_path, new_width=100, range_width=21.0, font_size=10):
    try:
        image = cv2.imread(input_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width=new_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image, range_width=range_width)
    img_width = image.shape[1]
    img_height = image.shape[0]

    font_size_scale = font_size

    output_image = np.zeros((img_height * font_size_scale, img_width * font_size_scale, 3), np.uint8)

    for i in range(len(ascii_str)):
        row = i // img_width
        col = i % img_width
        position = (col * font_size_scale, row * font_size_scale)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = font_size_scale / 40
        font_thickness = 1
        font_color = (255, 255, 255)
        cv2.putText(output_image, ascii_str[i], position, font, font_scale, font_color, font_thickness)

    cv2.imwrite(output_path, output_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIConverterApp(root)
    root.mainloop()
