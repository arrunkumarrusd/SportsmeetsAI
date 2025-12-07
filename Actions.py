# actions.py

from typing import List, Tuple
import numpy as np

def detect_actions(landmarks_seq: List[np.ndarray],
                   fps: float = 30.0,
                   punch_velocity_thresh: float = 0.07,
                   punch_angle_thresh: float = 145.0,
                   block_velocity_thresh: float = 0.04,
                   min_punch_gap_sec: float = 0.4,
                   wrist_dx_threshold: float = 0.008
                   ) -> Tuple[int, int, List[int], List[int]]:
    """
    Detect punches and lower blocks from pose landmarks.
    Returns:
        punches_total, blocks_total, punches_cumulative, blocks_cumulative
    """
    punches = 0
    blocks = 0
    punches_cumulative = []
    blocks_cumulative = []

    punch_in_progress = False
    last_punch_frame = -int(min_punch_gap_sec * fps)
    min_frame_gap = int(min_punch_gap_sec * fps)

    def angle_between(a, b, c):
        ba = a - b
        bc = c - b
        cosang = np.dot(ba, bc) / (np.linalg.norm(ba)*np.linalg.norm(bc) + 1e-6)
        return np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))

    for i in range(1, len(landmarks_seq)):
        prev, curr = landmarks_seq[i-1], landmarks_seq[i]
        if prev is None or curr is None:
            punches_cumulative.append(punches)
            blocks_cumulative.append(blocks)
            continue

        # Right arm joints (MediaPipe indices assumed)
        shoulder = curr[12][:2]
        elbow    = curr[14][:2]
        wrist    = curr[16][:2]
        nose     = curr[0][:2]

        elbow_angle = angle_between(shoulder, elbow, wrist)
        wrist_forward = wrist[0] > nose[0]
        wrist_dx = curr[16][0] - prev[16][0]
        wrist_v = np.linalg.norm(curr[16][:3] - prev[16][:3])

        if (elbow_angle > punch_angle_thresh
            and wrist_forward
            and wrist_dx > wrist_dx_threshold
            and wrist_v > punch_velocity_thresh):
            if not punch_in_progress and (i - last_punch_frame) > min_frame_gap:
                punches += 1
                punch_in_progress = True
                last_punch_frame = i
        else:
            punch_in_progress = False

        # Lower block detection (right fist)
        right_thigh   = curr[24][:2]
        wrist_r       = curr[16][:2]
        wrist_v_r     = np.linalg.norm(curr[16][:3] - prev[16][:3])
        torso_rotation = abs(curr[11][0] - curr[12][0]) - abs(prev[11][0] - prev[12][0])

        if (wrist_r[1] > right_thigh[1] and wrist_v_r > block_velocity_thresh and torso_rotation > 0.02):
            blocks += 1

        # Lower block detection (left fist)
        left_thigh     = curr[23][:2]
        wrist_l        = curr[15][:2]
        wrist_v_l      = np.linalg.norm(curr[15][:3] - prev[15][:3])

        if (wrist_l[1] > left_thigh[1] and wrist_v_l > block_velocity_thresh and torso_rotation > 0.02):
            blocks += 1

        punches_cumulative.append(punches)
        blocks_cumulative.append(blocks)

    # Pad cumulative lists to match frame count
    while len(punches_cumulative) < len(landmarks_seq):
        punches_cumulative.append(punches)
    while len(blocks_cumulative) < len(landmarks_seq):
        blocks_cumulative.append(blocks)

    return punches, blocks, punches_cumulative, blocks_cumulative