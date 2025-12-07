# pose_utils.py

from typing import List, Optional
import numpy as np

def extract_pose_landmarks(frames: List) -> List[Optional[np.ndarray]]:
    """
    Placeholder: return list of (33 x 3) landmarks in normalized coordinates.
    Use MediaPipe or your model here. None for frames with no detection.
    """
    landmarks = []
    for _ in frames:
        landmarks.append(None)  # replace with actual pose inference result
    return landmarks

def extract_pose_features(landmarks_seq: List[np.ndarray]) -> List[dict]:
    """
    Compute kinematic, planar, volumetric features per frame.
    """
    features = []
    for lm in landmarks_seq:
        if lm is None:
            features.append({"kinematic": {}, "planar": {}, "volumetric": {}})
            continue
        velocities = [0.0] * 5
        bbox = {"xmin": 0.0, "xmax": 1.0, "ymin": 0.0, "ymax": 1.0}
        torso_volume = float(0.0)
        features.append({
            "kinematic": {"velocities": velocities},
            "planar": {"bbox": bbox, "shoulders": (0.0, 0.0)},
            "volumetric": {"torso_volume": torso_volume},
        })
    return features