import cv2
import os
import shutil
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

def pixels_to_ascii(image, range_width=21):
    pixels = image.flatten()
    ascii_str = ""
    for pixel_value in pixels:
        # Invert the mapping for darker pixels
        inverted_pixel_value = 255 - pixel_value
        normalized_pixel = int(inverted_pixel_value / range_width)
        index = min(normalized_pixel, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def create_ascii_frame(frame, new_width=100):
    frame = resize_image(frame, new_width=new_width)
    frame = grayify(frame)

    ascii_str = pixels_to_ascii(frame)
    img_width = frame.shape[1]
    img_height = frame.shape[0]

    font_size = 10  # You can adjust the font size

    # Create a black background
    output_frame = np.zeros((img_height * font_size, img_width * font_size, 3), np.uint8)

    # Draw white ASCII characters on the black background
    for i in range(len(ascii_str)):
        row = i // img_width
        col = i % img_width
        position = (col * font_size, row * font_size)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4  # You can adjust the font scale
        font_thickness = 1  # You can adjust the font thickness
        font_color = (255, 255, 255)  # White color
        cv2.putText(output_frame, ascii_str[i], position, font, font_scale, font_color, font_thickness)

    return output_frame

def create_video(frames_folder, output_video_path, fps=30):
    frame_files = [f for f in os.listdir(frames_folder) if f.endswith(".png")]
    frame_files.sort()

    if not frame_files:
        print("No frame images found in the specified folder.")
        return

    frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
    frame_height, frame_width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec based on your system
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    print("Creating video from ASCII frames...")
    for i, frame_file in enumerate(frame_files, start=1):
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)
        print(f"Processed frame {i}/{len(frame_files)}")

    out.release()
    print("Video creation complete!")

def process_video(input_video_path, output_video_path, new_width=100, fps=30):
    frames_folder = "frames"

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    os.makedirs(frames_folder, exist_ok=True)

    frame_count = 0

    print("Generating ASCII frames from video...")
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        ascii_frame = create_ascii_frame(frame, new_width=new_width)

        # Save the ASCII frame as an image in the frames folder
        frame_filename = os.path.join(frames_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, ascii_frame)

        frame_count += 1
        print(f"Processed frame {frame_count}")

    cap.release()

    # Create video from ASCII frames
    create_video(frames_folder, output_video_path, fps=fps)

    # Delete the frames folder
    shutil.rmtree(frames_folder)

if __name__ == "__main__":
    input_video_path = "aa.mp4"
    output_video_path = "output_ascii_video.mp4"
    process_video(input_video_path, output_video_path)
