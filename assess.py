# assess.py

import pathlib
import numpy as np
from config import ActionDetectConfig, OverlayConfig
from video_utils import download_clip, get_video_frame_count, get_video_fps, load_video_frames
from pose_utils import extract_pose_landmarks, extract_pose_features
from actions import detect_actions
from scoring import similarity_score, grade_student, suggest_improvement
from overlay import overlay_stats, draw_skeleton, blur_face_region, save_debug_video

def assess_taekwando(instructor_url: str,
                     instructor_start_sec: int,
                     instructor_end_sec: int,
                     student_url: str,
                     student_start_sec: int,
                     student_end_sec: int,
                     output_dir_path: str,
                     max_frames: int | None = None,
                     debug_viz: bool = True) -> None:

    outdir = pathlib.Path(output_dir_path)
    outdir.mkdir(parents=True, exist_ok=True)

    instructor_mp4 = download_clip(instructor_url, outdir, instructor_start_sec, instructor_end_sec, "instructor")
    student_mp4    = download_clip(student_url, outdir, student_start_sec, student_end_sec, "student")

    if max_frames is None:
        instr_total = get_video_frame_count(instructor_mp4)
        stud_total  = get_video_frame_count(student_mp4)
        max_frames = min(instr_total, stud_total)

    instr_frames = load_video_frames(instructor_mp4, max_frames)
    stud_frames  = load_video_frames(student_mp4, max_frames)

    instr_fps = get_video_fps(instructor_mp4)
    stud_fps  = get_video_fps(student_mp4)

    instr_landmarks = extract_pose_landmarks(instr_frames)
    stud_landmarks  = extract_pose_landmarks(stud_frames)

    min_len = min(len(instr_landmarks), len(stud_landmarks))
    instr_landmarks = instr_landmarks[:min_len]
    stud_landmarks  = stud_landmarks[:min_len]
    instr_frames    = instr_frames[:min_len]
    stud_frames     = stud_frames[:min_len]

    instr_features = extract_pose_features(instr_landmarks)
    stud_features  = extract_pose_features(stud_landmarks)

    cfg = ActionDetectConfig(fps_instructor=instr_fps, fps_student=stud_fps)
    instr_punches, instr_blocks, instr_punches_cum, instr_blocks_cum = detect_actions(
        instr_landmarks,
        fps=cfg.fps_instructor,
        punch_velocity_thresh=cfg.punch_velocity_thresh,
        punch_angle_thresh=cfg.punch_angle_thresh,
        block_velocity_thresh=cfg.block_velocity_thresh,
        min_punch_gap_sec=cfg.min_punch_gap_sec,
        wrist_dx_threshold=cfg.wrist_dx_threshold,
    )
    stud_punches, stud_blocks, stud_punches_cum, stud_blocks_cum = detect_actions(
        stud_landmarks,
        fps=cfg.fps_student,
        punch_velocity_thresh=cfg.punch_velocity_thresh,
        punch_angle_thresh=cfg.punch_angle_thresh,
        block_velocity_thresh=cfg.block_velocity_thresh,
        min_punch_gap_sec=cfg.min_punch_gap_sec,
        wrist_dx_threshold=cfg.wrist_dx_threshold,
    )

    stud_scores, frame_suggestions = [], []
    for A, B in zip(instr_landmarks, stud_landmarks):
        res = similarity_score(A, B)
        stud_scores.append(res.score)
        frame_suggestions.append(suggest_improvement(A, B, res.per_joint_dist))

    stud_avg_score = float(np.mean(stud_scores)) if stud_scores else 0.0
    stud_grade = grade_student(stud_avg_score)
    overall_suggestion = frame_suggestions[0] if frame_suggestions else "No suggestions available."

    if debug_viz:
        instr_viz, stud_viz = [], []
        ovcfg = OverlayConfig()

        for i, (f, l, feat) in enumerate(zip(instr_frames, instr_landmarks, instr_features)):
            timestamp = i / max(instr_fps, 1e-6)
            frame = draw_skeleton(f, l)
            frame = blur_face_region(frame, l)
            frame = overlay_stats(
                frame,
                score=100.0,
                punches_made=instr_punches_cum[i],
                punches_missed=0,
                blocks_made=instr_blocks_cum[i],
                blocks_missed=0,
                kinematic=str(feat["kinematic"]),
                planar=str(feat["planar"]),
                volumetric=str(feat["volumetric"]),
                overall="Reference",
                last_punch_result="made",
                current_color=ovcfg.color_ok,
                subtitle=f"Time: {timestamp:.2f}s"
            )
            instr_viz.append(frame)

        for i, (f, l, feat) in enumerate(zip(stud_frames, stud_landmarks, stud_features)):
            timestamp = i / max(stud_fps, 1e-6)
            frame = draw_skeleton(f, l)
            frame = blur_face_region(frame, l)
            frame = overlay_stats(
                frame,
                score=stud_scores[i],
                punches_made=stud_punches_cum[i],
                punches_missed=0,
                blocks_made=stud_blocks_cum[i],
                blocks_missed=0,
                kinematic=str(feat["kinematic"]),
                planar=str(feat["planar"]),
                volumetric=str(feat["volumetric"]),
                overall=stud_grade,
                last_punch_result="eval",
                current_color=ovcfg.color_student,
                subtitle=frame_suggestions[i]
            )
            stud_viz.append(frame)

        # Summary frame
        if stud_frames:
            final = overlay_stats(
                stud_frames[-1],
                score=stud_avg_score,
                punches_made=stud_punches,
                punches_missed=0,
                blocks_made=stud_blocks,
                blocks_missed=0,
                kinematic="Summary",
                planar="Summary",
                volumetric="Summary",
                overall=stud_grade,
                last_punch_result="summary",
                current_color=ovcfg.color_summary,
                subtitle=overall_suggestion
            )
            stud_viz.append(final)

        save_debug_video(instr_viz, outdir / "instructor_skeleton_blurred.mp4", fps=instr_fps)
        save_debug_video(stud_viz,  outdir / "student_skeleton_blurred.mp4",   fps=stud_fps)

    print("\n--- Taekwando Assessment ---")
    print(f"Frames compared: {min_len}")
    print(f"Average similarity score: {stud_avg_score:.2f} / 100")
    print(f"Grade: {stud_grade}")
    print(f"Suggested improvement: {overall_suggestion}")
    print(f"Punches (student): {stud_punches} | Blocks (student): {stud_blocks}")
    print(f"Saved outputs to: {outdir}")