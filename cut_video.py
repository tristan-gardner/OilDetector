import cv2
import os

def video_to_images(input_folder, output_folder, frame_interval=10):
    """
    Extracts frames from a video and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the folder to save the extracted images.
        frame_interval (int): Extract one frame every `frame_interval` frames.

    Returns:
        None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    saved_count = 0
    print(os.listdir(input_folder))

    for filename in os.listdir(input_folder):
        print(f'slicing file: {filename}')
        video_path = os.path.join(input_folder, filename)

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Cannot open video file.")
            continue

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:  # End of video
                break   

            # Save every `frame_interval`-th frame
            if frame_count % frame_interval == 0:
                output_path = os.path.join(output_folder, f"{saved_count:04d}.jpg")
                cv2.imwrite(output_path, frame)
                print(f"Saved {output_path}")
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"Extraction completed. Total frames saved: {saved_count}")

# Usage
video_path = "./raw_videos/oil"  # Replace with your video file path
output_folder = "./pics/oil_pics"  # Replace with your output folder path
video_to_images(video_path, output_folder, frame_interval=30)  # Save one frame every 30 frames
