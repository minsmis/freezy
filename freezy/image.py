from pathlib import Path
import cv2


def read_vid(vpath):
    vid = cv2.VideoCapture(vpath)
    return vid


def adjust_contrast_and_brightness(vpath, contrast=8.0, brightness=50):
    # Make output path
    vpath = Path(vpath)
    f = vpath.name.split('.')
    output_path = vpath.parent / (f[0] + "_adjusted." + f[-1])

    vid = cv2.VideoCapture(vpath)

    if not vid.isOpened():
        print("Failed to load video file:", vpath)
        return

    # Read video info
    fps = vid.get(cv2.CAP_PROP_FPS)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while (vid.isOpened()):
        ret, frame = vid.read()

        if not ret:
            break

        brighter = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

        out.write(brighter)

    vid.release()
    out.release()
    return output_path
