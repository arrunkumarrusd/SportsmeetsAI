# config.py

from dataclasses import dataclass

@dataclass
class ActionDetectConfig:
    fps_instructor: float = 30.0
    fps_student: float = 30.0
    punch_velocity_thresh: float = 0.07
    punch_angle_thresh: float = 145.0
    block_velocity_thresh: float = 0.04
    min_punch_gap_sec: float = 0.4
    wrist_dx_threshold: float = 0.008

@dataclass
class OverlayConfig:
    font_scale: float = 0.6
    thickness: int = 2
    color_ok: tuple = (0, 255, 0)
    color_student: tuple = (0, 0, 255)
    color_summary: tuple = (255, 255, 0)