import cv2
import numpy as np

ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    height, width, _ = image.shape
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def grayify(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def pixels_to_ascii(image, range_width=27):
    pixels = image.flatten()
    ascii_str = ""
    for pixel_value in pixels:
        # Invert the mapping for darker pixels
        inverted_pixel_value = 255 - pixel_value
        normalized_pixel = int(inverted_pixel_value / range_width)
        index = min(normalized_pixel, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def create_ascii_image(image_path, output_path, new_width=100):
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width=new_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)
    img_width = image.shape[1]
    img_height = image.shape[0]

    font_size = 10  # You can adjust the font size

    # Create a black background
    output_image = np.zeros((img_height * font_size, img_width * font_size, 3), np.uint8)

    # Draw white ASCII characters on the black background
    for i in range(len(ascii_str)):
        row = i // img_width
        col = i % img_width
        position = (col * font_size, row * font_size)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4  # You can adjust the font scale
        font_thickness = 1  # You can adjust the font thickness
        font_color = (255, 255, 255)  # White color
        cv2.putText(output_image, ascii_str[i], position, font, font_scale, font_color, font_thickness)

    # Save the resulting image
    cv2.imwrite(output_path, output_image)

if __name__ == "__main__":
    input_image_path = "ann.png"
    output_image_path = "ascii_image.png"
    create_ascii_image(input_image_path, output_image_path)
