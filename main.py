# import cv2
# from ultralytics import YOLO
# import csv
# import time
# import argparse
# import sys
# from pathlib import Path

# WORKSPACE_DIR = Path(__file__).resolve().parent
# DEFAULT_MODEL_PATH = str(WORKSPACE_DIR / "best.pt")
# DEFAULT_INPUT_VIDEO = str(WORKSPACE_DIR / "potholes_2.mp4")
# DEFAULT_OUTPUT_VIDEO = str(WORKSPACE_DIR / "pothole_2_output.mp4")
# DEFAULT_CSV_OUTPUT = str(WORKSPACE_DIR / "pothole_telemetry.csv")

# # Standardized asphalt defect palette
# DEFAULT_COLOR = (0, 0, 255) # Red fallback
# DEFECT_COLORS = {
#     'Pothole': (0, 0, 255),      # Red
#     'Severe_Pothole': (0, 0, 139), # Dark Red
#     'Crack': (0, 255, 255),      # Yellow
#     'Patch': (0, 255, 0)         # Green
# }

# class PotholeAnalytics:
#     def __init__(self, csv_file_handle):
#         self.discovered_potholes = set()  # Track unique IDs to prevent double counting
        
#         # Structure CSV columns for civil engineering / mapping metrics
#         self.csv_writer = csv.DictWriter(csv_file_handle, fieldnames=['frame', 'timestamp_sec', 'pothole_id', 'type', 'confidence'])
#         self.csv_writer.writeheader()

#     def register_defect(self, track_id, defect_type, conf, frame_num, fps):
#         timestamp = round(frame_num / fps, 2)
        
#         # Log entry for raw frame tracking
#         self.csv_writer.writerow({
#             'frame': frame_num,
#             'timestamp_sec': timestamp,
#             'pothole_id': track_id,
#             'type': defect_type,
#             'confidence': round(conf, 4)
#         })

#         # Add to unique set
#         self.discovered_potholes.add(track_id)

#     def get_total_count(self):
#         return len(self.discovered_potholes)

# def process_road_video(args):
#     print(f"🔄 Loading Pothole Detection Model: {args.model}...")
#     try:
#         model = YOLO(args.model)
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         sys.exit(1)

#     cap = cv2.VideoCapture(args.input)
#     if not cap.isOpened():
#         print(f"❌ Error: Could not open input road video {args.input}")
#         sys.exit(1)

#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

#     frame_num = 0

#     print(f"🎥 Processing road footage ({total_frames} frames total)...")

#     with open(args.csv, 'w', newline='') as f:
#         analytics = PotholeAnalytics(f)

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             frame_num += 1

#             # tracking with a larger image size (640) for better small-pothole accuracy down the road
#             results = model.track(frame, persist=True, tracker="bytetrack.yaml", imgsz=640, verbose=False)[0]

#             if results.boxes.id is not None:
#                 # Convert tensor data to CPU iterables safely
#                 boxes = results.boxes.xyxy.int().cpu().tolist()
#                 ids = results.boxes.id.int().cpu().tolist()
#                 confs = results.boxes.conf.cpu().tolist()
#                 classes = results.boxes.cls.int().cpu().tolist()

#                 for box, track_id, conf, cls in zip(boxes, ids, confs, classes):
#                     x1, y1, x2, y2 = box
#                     defect_name = results.names[cls]

#                     # Map incoming class name to your expected pothole label fallback
#                     if "pothole" in defect_name.lower():
#                         defect_name = "Pothole"

#                     analytics.register_defect(track_id, defect_name, conf, frame_num, fps)

#                     # Dynamic styling
#                     color = DEFECT_COLORS.get(defect_name, DEFAULT_COLOR)
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

#                     # Safe label generation near video boundaries
#                     label = f"Defect #{track_id}: {defect_name} ({conf:.0%})"
#                     (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
#                     text_offset_y = y1 - th - 10 if y1 - th - 10 > 0 else y1 + th + 10
                    
#                     cv2.rectangle(frame, (x1, text_offset_y - th), (x1 + tw, text_offset_y + 5), color, -1)
#                     cv2.putText(frame, label, (x1, text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

#             # Frame status overlay
#             cv2.putText(frame, f"Unique Potholes Logged: {analytics.get_total_count()}", (20, 40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

#             out.write(frame)

#             if frame_num % 15 == 0:
#                 pct = (frame_num / total_frames) * 100
#                 print(f"Progress: {pct:.1f}% | Frame {frame_num}/{total_frames}", end="\r")

#     cap.release()
#     out.release()
    
#     print(f"\n\n🚀 Analysis Pipeline Finished Successfully!")
#     print(f"📊 Report Summary saved to: {args.csv}")
#     print(f"🕳️ Total Distinct Potholes Identified: {analytics.get_total_count()}")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Industrial Road Quality Tracker using YOLO")
#     parser.add_argument("--model", type=str, default=DEFAULT_MODEL_PATH, help="Path to your trained pothole best.pt model")
#     parser.add_argument("--input", type=str, default=DEFAULT_INPUT_VIDEO, help="Path to road video file")
#     parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_VIDEO, help="Output path for annotated video")
#     parser.add_argument("--csv", type=str, default=DEFAULT_CSV_OUTPUT, help="Output CSV path for analytics logs")
    
#     args = parser.parse_args()
#     process_road_video(args)


import cv2
from ultralytics import YOLO
import csv
import argparse
import sys
from pathlib import Path


WORKSPACE_DIR = Path(__file__).resolve().parent

DEFAULT_MODEL_PATH = str(WORKSPACE_DIR / "best.pt")
DEFAULT_INPUT_VIDEO = str(WORKSPACE_DIR / "potholes_2.mp4")
DEFAULT_OUTPUT_VIDEO = str(WORKSPACE_DIR / "pothole_2_output.mp4")
DEFAULT_CSV_OUTPUT = str(WORKSPACE_DIR / "pothole_2_telemetry.csv")
DEFAULT_UNIQUE_CSV = str(WORKSPACE_DIR / "unique_2_potholes.csv")


DEFAULT_COLOR = (0, 0, 255)

DEFECT_COLORS = {
    "Pothole": (0, 0, 255),
    "Severe_Pothole": (0, 0, 139),
    "Crack": (0, 255, 255),
    "Patch": (0, 255, 0)
}


class PotholeAnalytics:

    def __init__(self, csv_file_handle):
        # Frame-by-frame CSV
        self.csv_writer = csv.DictWriter(
            csv_file_handle,
            fieldnames=[
                "frame",
                "timestamp_sec",
                "track_id",
                "type",
                "confidence"
            ]
        )

        self.csv_writer.writeheader()

        # Store information about every track
        self.tracks = {}

        # Our own permanent ID counter
        self.next_pothole_id = 1

        # Mapping:
        # ByteTrack ID -> permanent pothole ID
        self.track_to_pothole = {}

    def register_defect(
        self,
        track_id,
        defect_type,
        conf,
        frame_num,
        fps
    ):

        timestamp = round(frame_num / fps, 2)

        # ---------------------------------------------------------
        # 1. Write frame-by-frame telemetry
        # ---------------------------------------------------------

        self.csv_writer.writerow({
            "frame": frame_num,
            "timestamp_sec": timestamp,
            "track_id": track_id,
            "type": defect_type,
            "confidence": round(conf, 4)
        })

        # ---------------------------------------------------------
        # 2. Assign our own pothole ID to this track
        # ---------------------------------------------------------

        if track_id not in self.track_to_pothole:

            self.track_to_pothole[track_id] = self.next_pothole_id

            self.next_pothole_id += 1

        pothole_id = self.track_to_pothole[track_id]

        # ---------------------------------------------------------
        # 3. Create record for this track if necessary
        # ---------------------------------------------------------

        if track_id not in self.tracks:

            self.tracks[track_id] = {
                "pothole_id": pothole_id,
                "track_id": track_id,
                "type": defect_type,

                "first_frame": frame_num,
                "last_frame": frame_num,

                "first_timestamp": timestamp,
                "last_timestamp": timestamp,

                "max_confidence": conf,
                "detections": 1
            }

        else:

            track = self.tracks[track_id]

            track["last_frame"] = frame_num
            track["last_timestamp"] = timestamp

            track["max_confidence"] = max(
                track["max_confidence"],
                conf
            )

            track["detections"] += 1

    def get_total_count(self):

        return len(self.tracks)

    def write_unique_csv(self, filename):

        fieldnames = [
            "pothole_id",
            "track_id",
            "type",
            "first_frame",
            "last_frame",
            "first_timestamp",
            "last_timestamp",
            "max_confidence",
            "detections"
        ]

        with open(filename, "w", newline="") as f:

            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames
            )

            writer.writeheader()

            # Sort by permanent pothole ID
            sorted_tracks = sorted(
                self.tracks.values(),
                key=lambda x: x["pothole_id"]
            )

            for track in sorted_tracks:

                writer.writerow({
                    "pothole_id": track["pothole_id"],
                    "track_id": track["track_id"],
                    "type": track["type"],
                    "first_frame": track["first_frame"],
                    "last_frame": track["last_frame"],
                    "first_timestamp": track["first_timestamp"],
                    "last_timestamp": track["last_timestamp"],
                    "max_confidence": round(
                        track["max_confidence"],
                        4
                    ),
                    "detections": track["detections"]
                })


def process_road_video(args):

    print(
        f"🔄 Loading Pothole Detection Model: {args.model}..."
    )

    try:
        model = YOLO(args.model)

    except Exception as e:

        print(f"❌ Error loading model: {e}")
        sys.exit(1)

    cap = cv2.VideoCapture(args.input)

    if not cap.isOpened():

        print(
            f"❌ Error: Could not open input road video "
            f"{args.input}"
        )

        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        args.output,
        fourcc,
        fps,
        (width, height)
    )

    frame_num = 0

    print(
        f"🎥 Processing road footage "
        f"({total_frames} frames total)..."
    )

    with open(args.csv, "w", newline="") as f:

        analytics = PotholeAnalytics(f)

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            frame_num += 1

            # -----------------------------------------------------
            # YOLO + ByteTrack
            # -----------------------------------------------------

            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                imgsz=640,
                verbose=False
            )[0]

            if results.boxes.id is not None:

                boxes = (
                    results.boxes.xyxy
                    .int()
                    .cpu()
                    .tolist()
                )

                ids = (
                    results.boxes.id
                    .int()
                    .cpu()
                    .tolist()
                )

                confs = (
                    results.boxes.conf
                    .cpu()
                    .tolist()
                )

                classes = (
                    results.boxes.cls
                    .int()
                    .cpu()
                    .tolist()
                )

                for box, track_id, conf, cls in zip(
                    boxes,
                    ids,
                    confs,
                    classes
                ):

                    x1, y1, x2, y2 = box

                    defect_name = results.names[cls]

                    if "pothole" in defect_name.lower():

                        defect_name = "Pothole"

                    # -------------------------------------------------
                    # Register observation
                    # -------------------------------------------------

                    analytics.register_defect(
                        track_id,
                        defect_name,
                        conf,
                        frame_num,
                        fps
                    )

                    # Get our permanent ID
                    pothole_id = (
                        analytics.track_to_pothole[track_id]
                    )

                    # -------------------------------------------------
                    # Draw bounding box
                    # -------------------------------------------------

                    color = DEFECT_COLORS.get(
                        defect_name,
                        DEFAULT_COLOR
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        color,
                        3
                    )

                    # -------------------------------------------------
                    # Display BOTH IDs
                    # -------------------------------------------------

                    label = (
                        f"Pothole #{pothole_id} "
                        f"(Track {track_id}) "
                        f"{conf:.0%}"
                    )

                    (
                        tw,
                        th
                    ), _ = cv2.getTextSize(
                        label,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        2
                    )

                    text_offset_y = (
                        y1 - th - 10
                        if y1 - th - 10 > 0
                        else y1 + th + 10
                    )

                    cv2.rectangle(
                        frame,
                        (
                            x1,
                            text_offset_y - th
                        ),
                        (
                            x1 + tw,
                            text_offset_y + 5
                        ),
                        color,
                        -1
                    )

                    cv2.putText(
                        frame,
                        label,
                        (
                            x1,
                            text_offset_y
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA
                    )

            # ---------------------------------------------------------
            # Status
            # ---------------------------------------------------------

            cv2.putText(
                frame,
                f"Tracked Potholes: "
                f"{analytics.get_total_count()}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
                cv2.LINE_AA
            )

            out.write(frame)

            if frame_num % 15 == 0:

                pct = (
                    frame_num /
                    total_frames *
                    100
                )

                print(
                    f"Progress: {pct:.1f}% | "
                    f"Frame {frame_num}/{total_frames}",
                    end="\r"
                )

    cap.release()
    out.release()

    # -------------------------------------------------------------
    # Write one-row-per-track CSV
    # -------------------------------------------------------------

    analytics.write_unique_csv(
        args.unique_csv
    )

    print("\n")
    print("🚀 Analysis Pipeline Finished Successfully!")
    print(f"📊 Frame telemetry: {args.csv}")
    print(f"📊 Unique tracks: {args.unique_csv}")

    print(
        f"🕳️ Total ByteTrack trajectories: "
        f"{analytics.get_total_count()}"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Industrial Road Quality Tracker using YOLO"
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_PATH
    )

    parser.add_argument(
        "--input",
        type=str,
        default=DEFAULT_INPUT_VIDEO
    )

    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_VIDEO
    )

    parser.add_argument(
        "--csv",
        type=str,
        default=DEFAULT_CSV_OUTPUT
    )

    parser.add_argument(
        "--unique-csv",
        type=str,
        default=DEFAULT_UNIQUE_CSV,
        help="One row per tracked pothole trajectory"
    )

    args = parser.parse_args()

    process_road_video(args)