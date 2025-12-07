# video_utils.py

import cv2
import pathlib
from typing import List, Optional

def download_clip(url: str, output_dir: pathlib.Path, start_sec: Optional[int], end_sec: Optional[int], basename: str) -> str:
    """
    Placeholder: implement actual download + trim.
    For now assume `url` points to a local mp4 file path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(url)  # replace with actual downloader

def get_video_frame_count(video_path: str) -> int:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {video_path}")
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frames

def get_video_fps(video_path: str) -> float:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video file: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return float(fps) if fps and fps > 0 else 30.0

def load_video_frames(video_path: str, max_frames: Optional[int] = None) -> List:
    cap = cv2.VideoCapture(str(video_path))
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        count += 1
        if max_frames is not None and count >= max_frames:
            break
    cap.release()
    return frames