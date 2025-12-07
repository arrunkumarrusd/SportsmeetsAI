# overlay.py

import cv2
from typing import Optional, Tuple

def draw_skeleton(frame, landmarks):
    # Placeholder: draw lines between keypoints
    return frame

def blur_face_region(frame, landmarks):
    # Placeholder: blur around nose/eyes region
    return frame

def overlay_stats(display_frame,
                  score: float,
                  punches_made: int,
                  punches_missed: int,
                  blocks_made: int,
                  blocks_missed: int,
                  kinematic: str,
                  planar: str,
                  volumetric: str,
                  overall: str,
                  last_punch_result: str,
                  current_color: Tuple[int, int, int],
                  subtitle: Optional[str] = None):
    frame = display_frame.copy()
    x, y = 20, 30
    lines = [
        f"Score: {score:.2f}",
        f"Punches Made: {punches_made}",
        f"Punches Missed: {punches_missed}",
        f"Blocks Made: {blocks_made}",
        f"Blocks Missed: {blocks_missed}",
        f"Kinematic: {kinematic}",
        f"Planar: {planar}",
        f"Volumetric: {volumetric}",
        f"Overall: {overall}",
        f"{subtitle or ''}",
    ]
    for i, text in enumerate(lines):
        cv2.putText(frame, text, (x, y + i*24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, current_color, 2, cv2.LINE_AA)
    return frame

def save_debug_video(frames, out_path, fps: float):
    if not frames:
        return
    h, w = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (w, h))
    for f in frames:
        writer.write(f)
    writer.release()