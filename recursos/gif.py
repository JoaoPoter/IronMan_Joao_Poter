from PIL import Image, ImageSequence
import os

def extract_frames(gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(gif_path) as img:
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            frame.save(os.path.join(output_folder, f"frame_{i:03d}.png"))
    print(f"Frames salvos em: {output_folder}")
