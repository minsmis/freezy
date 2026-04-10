import os
from pathlib import Path

import numpy as np

import cv2
import deeplabcut as dlc

import freezy.image as ip

working_dir = Path(os.getcwd())
video_paths = [
    r"C:\Users\ompom777\Desktop\0410 (1).mp4"
]

rn = np.random.randint(1000, 10000, size=1)[0]

# Preprocessing - increase saturation
processed_video_paths = []
for vpath in video_paths:
    output_path = ip.adjust_contrast_and_brightness(vpath)
    processed_video_paths.append(str(output_path))

# Create new project
config_path = dlc.create_new_project("temp_{}".format(rn), "freezy", processed_video_paths)

# Extract frames to label
dlc.extract_frames(config_path)

# Label frames
dlc.label_frames(config_path)

# Check labels
dlc.check_labels(config_path)

# Create training dataset
dlc.create_training_dataset(config_path)

# Train network
dlc.train_network(config_path, epochs=1000)

# Evaluate network
dlc.evaluate_network(config_path)

# Analyze video
dlc.analyze_videos(config_path, processed_video_paths)
dlc.filterpredictions(config_path, processed_video_paths)

# Create labeled video
dlc.create_labeled_video(config_path, processed_video_paths, filtered=True)
