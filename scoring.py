# scoring.py

from typing import List, NamedTuple
import numpy as np

class ScoreResult(NamedTuple):
    score: float
    per_joint_dist: List[float]

def similarity_score(instr_lm: np.ndarray, stud_lm: np.ndarray) -> ScoreResult:
    """
    Placeholder: compute similarity between instructor and student landmarks.
    """
    if instr_lm is None or stud_lm is None:
        return ScoreResult(score=0.0, per_joint_dist=[float("inf")])
    dist = float(np.linalg.norm(instr_lm - stud_lm))
    score = max(0.0, 100.0 - dist * 100.0)
    return ScoreResult(score=score, per_joint_dist=[dist])

def grade_student(avg_score: float) -> str:
    if avg_score >= 85: return "Excellent"
    if avg_score >= 70: return "Good"
    if avg_score >= 55: return "Fair"
    return "Needs Improvement"

def suggest_improvement(instr_lm, stud_lm, per_joint_dist: List[float]) -> str:
    if instr_lm is None or stud_lm is None:
        return "Ensure consistent pose detection by improving lighting and camera angle."
    return "Focus on aligning your right wrist. Reduce deviation through targeted drills and mirror practice."