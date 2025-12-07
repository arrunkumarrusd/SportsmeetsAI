# main.py

import argparse
from assess import assess_taekwando

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--instructor_url", required=True)
    p.add_argument("--instructor_start", type=int, default=None)
    p.add_argument("--instructor_end", type=int, default=None)
    p.add_argument("--student_url", required=True)
    p.add_argument("--student_start", type=int, default=None)
    p.add_argument("--student_end", type=int, default=None)
    p.add_argument("--output_dir", required=True)
    p.add_argument("--max_frames", type=int, default=None)
    p.add_argument("--debug_viz", action="store_true")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    assess_taekwando(
        instructor_url=args.instructor_url,
        instructor_start_sec=args.instructor_start,
        instructor_end_sec=args.instructor_end,
        student_url=args.student_url,
        student_start_sec=args.student_start,
        student_end_sec=args.student_end,
        output_dir_path=args.output_dir,
        max_frames=args.max_frames,
        debug_viz=args.debug_viz,
    )