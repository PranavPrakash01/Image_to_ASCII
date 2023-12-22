import cv2
import os

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

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()

if __name__ == "__main__":
    frames_folder = "frames"
    output_video_path = "output_video.mp4"
    create_video(frames_folder, output_video_path)
