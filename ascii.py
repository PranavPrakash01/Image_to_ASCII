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

        # Create white placeholders for images with a fixed size
        self.input_placeholder_image = Image.new("RGB", (400, 400), "white")
        self.output_placeholder_image = Image.new("RGB", (400, 400), "white")

        self.create_widgets()
        self.root.update_idletasks()  # Update idle tasks to calculate widget sizes
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def create_widgets(self):
        # Arrange input and output image displays side by side
        tk.Label(self.root, text="Input Image").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Output Image").grid(row=0, column=1, padx=10, pady=10)

        # Set placeholders as initial images
        self.show_input_image(self.input_placeholder_image)
        self.show_output_image(self.output_placeholder_image)

        # Convert Button
        tk.Button(self.root, text="Convert", command=self.convert_image).grid(row=2, column=0, columnspan=2, pady=10)

        # Browse Buttons
        tk.Label(self.root, text="Browse Input Image").grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_input_image).grid(row=3, column=1, padx=10, pady=10)

    def browse_input_image(self):
        # Set placeholders as initial images
        self.show_input_image(self.input_placeholder_image)
        self.show_output_image(self.output_placeholder_image)
        
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.input_image_path.set(file_path)
            self.show_input_image()

    def show_input_image(self, image=None):
        if image is None:
            image_path = self.input_image_path.get()
            if image_path:
                image = Image.open(image_path)

        # Calculate the maximum size that fits within the placeholder while maintaining the aspect ratio
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
        self.input_image_label = tk.Label(self.root, image=photo)
        self.input_image_label.image = photo
        self.input_image_label.grid(row=1, column=0, padx=10, pady=10)

    def convert_image(self):
        input_path = self.input_image_path.get()
        if not input_path:
            return

        # Get the directory and filename of the input image
        input_dir, input_filename = os.path.split(input_path)
        output_filename = f"{os.path.splitext(input_filename)[0]}-ascii.png"
        output_path = os.path.join(input_dir, output_filename)

        create_ascii_image(input_path, output_path)

        self.output_image_path.set(output_path)
        self.show_output_image()

    def show_output_image(self, image=None):
        if image is None:
            image_path = self.output_image_path.get()
            if image_path:
                image = Image.open(image_path)

        # Calculate the maximum size that fits within the placeholder while maintaining the aspect ratio
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
        self.output_image_label = tk.Label(self.root, image=photo)
        self.output_image_label.image = photo
        self.output_image_label.grid(row=1, column=1, padx=10, pady=10)

def resize_image(image, new_width=100):
    height, width, _ = image.shape
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def pixels_to_ascii(image, range_width=21):
    pixels = image.flatten()
    ascii_str = ""
    for pixel_value in pixels:
        inverted_pixel_value = 255 - pixel_value
        normalized_pixel = int(inverted_pixel_value / range_width)
        index = min(normalized_pixel, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def create_ascii_image(input_path, output_path, new_width=100):
    try:
        image = cv2.imread(input_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width=new_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)
    img_width = image.shape[1]
    img_height = image.shape[0]

    font_size = 10

    output_image = np.zeros((img_height * font_size, img_width * font_size, 3), np.uint8)

    for i in range(len(ascii_str)):
        row = i // img_width
        col = i % img_width
        position = (col * font_size, row * font_size)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        font_thickness = 1
        font_color = (255, 255, 255)
        cv2.putText(output_image, ascii_str[i], position, font, font_scale, font_color, font_thickness)

    cv2.imwrite(output_path, output_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIConverterApp(root)
    root.mainloop()