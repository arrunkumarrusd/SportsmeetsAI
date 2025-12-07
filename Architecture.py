# docs/architecture.py

"""
Architecture diagram for the Taekwondo assessment pipeline.
This file stores the Mermaid diagram as a string constant
and provides a helper function to export it into a Markdown file.
"""

ARCHITECTURE_MERMAID = """
flowchart TD
    %% Ingestion
    A[YouTube URLs + Time Windows] --> B[download_clip]
    B --> C[Video files: instructor.mp4, student.mp4]

    %% Decoding
    C --> D[get_video_fps & get_video_frame_count]
    C --> E[load_video_frames]

    %% Pose & Features
    E --> F[extract_pose_landmarks]
    F --> G[extract_pose_features]

    %% Actions
    F --> H[detect_actions]
    H --> H1[(punches_total)]
    H --> H2[(blocks_total)]
    H --> H3[(punches_cumulative per frame)]
    H --> H4[(blocks_cumulative per frame)]

    %% Scoring
    F --> I[similarity_score]
    I --> J[grade_student]
    I --> K[suggest_improvement per frame]

    %% Visualization
    E --> L[draw_skeleton]
    F --> M[blur_face_region]
    H & I & G --> N[overlay_stats]
    N --> O[save_debug_video (instructor & student)]

    %% Outputs
    O --> P[Assessment Summary + Videos + Logs]
"""

def export_mermaid_to_md(output_path: str = "architecture.md") -> None:
    """
    Export the Mermaid diagram into a Markdown file.
    """
    content = f"```mermaid\n{ARCHITECTURE_MERMAID}\n```"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Mermaid diagram exported to {output_path}")