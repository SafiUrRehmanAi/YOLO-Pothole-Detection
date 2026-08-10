# 🕳️ Pothole Detection and Road Analytics using YOLO26

A computer vision system for detecting and tracking potholes in road videos using **YOLO26s, ByteTrack, OpenCV, and Streamlit**. The project combines custom-trained pothole detection with object tracking and a Streamlit based analytics dashboard for reviewing road footage and detection data.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![YOLO](https://img.shields.io/badge/YOLO-26s-purple)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?logo=opencv)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![ByteTrack](https://img.shields.io/badge/Tracking-ByteTrack-orange)

---

# 📌 Project Highlights

* ✅ Custom-trained **YOLO26s pothole detection model**
* ✅ Pothole detection in road videos
* ✅ **ByteTrack** object tracking
* ✅ Persistent pothole and track IDs
* ✅ Frame-by-frame detection telemetry
* ✅ Unique pothole tracking summaries
* ✅ Annotated road video generation
* ✅ Interactive Streamlit road analytics dashboard
* ✅ Detection confidence analysis
* ✅ Pothole tracking timeline
* ✅ Individual track inspection
* ✅ CSV-based detection and tracking reports

---

# 📂 Dataset

**Dataset:** [Aegis Pothole Detection — Roboflow Universe](https://universe.roboflow.com/aegis/pothole-detection-i00zy/dataset/10)

The YOLO26s model was trained using the **Aegis Pothole Detection** dataset, containing annotated road images for pothole detection.

### Dataset Version

`v10`

### Dataset Distribution

| Split      |    Images |
| ---------- | --------: |
| Training   |     3,043 |
| Validation |       273 |
| Test       |       174 |
| **Total**  | **3,490** |

### Classes

`Pothole`

**Number of classes:** `1`

---

# 🧠 Pothole Detection and Tracking Pipeline

```text
Road Video
     ↓
YOLO26s Pothole Detection
     ↓
ByteTrack Object Tracking
     ↓
Permanent Pothole ID Assignment
     ↓
Telemetry & Tracking Data
     ↓
Annotated Video + CSV Reports
     ↓
Streamlit Analytics Dashboard
```

For video inference, YOLO tracking is performed with persistent tracking enabled and the **ByteTrack** tracker at an image size of 640.

---

# 🏗️ Model Information

| Component        | Value              |
| ---------------- | ------------------ |
| Model            | YOLO26s            |
| Framework        | Ultralytics        |
| Task             | Pothole Detection  |
| Input Size       | 640 × 640          |
| Tracking         | ByteTrack          |
| Video Processing | OpenCV             |
| Deployment       | OpenCV + Streamlit |

---

# ⚙️ Training Configuration

| Parameter  | Value                      |
| ---------- | ----------------           |
| Framework  | Ultralytics YOLO           |
| Model      | YOLO26s                    |
| Image Size | 640                        |
| Hardware   | Kaggle NVIDIA Tesla T4 GPU |
| Epochs     | 100                        |
| Batch Size | 32                          |

---

# 📊 Model Performance

The trained YOLO26s model achieved the following validation results:

| Metric    |     Score |
| --------- | --------: |
| Precision | **0.817** |
| Recall    | **0.804** |
| mAP@50    | **0.854** |
| mAP@50-95 | **0.503** |

### Validation Set

* **Images:** 273
* **Instances:** 970

The model achieved an **85.4% mAP@50**, with precision and recall of **81.7%** and **80.4%**, respectively.

---

# 🎥 Video Detection and Tracking

The system processes road footage frame by frame and uses YOLO26s together with ByteTrack to maintain object identities across frames.

For every detected pothole, the system records:

* Pothole ID
* ByteTrack Track ID
* Detection confidence
* Frame number
* Timestamp
* First appearance
* Last appearance
* Number of detections
* Maximum confidence

A permanent pothole ID is assigned to each tracked object and mapped to its corresponding ByteTrack ID.

Example detection label:

```text
Pothole #3 (Track 7) 87%
```

The processed video also displays the current number of tracked potholes.

---

# 📊 Streamlit Road Analytics Dashboard

The project includes an interactive Streamlit dashboard for analyzing the processed road footage and tracking data.

### Road Condition Overview

Displays:

* Tracked Potholes
* Total Detections
* Average Confidence
* Maximum Confidence
* Video Duration

### Annotated Road Footage

Displays the processed road video with pothole bounding boxes, IDs, tracking IDs, and confidence scores.

### Pothole Summary

Provides a summary of individual tracked potholes, including:

* Pothole ID
* Track ID
* First Timestamp
* Last Timestamp
* Maximum Confidence
* Number of Detections

### Detection Confidence Analysis

Includes:

* Confidence over time
* Confidence distribution

### Pothole Tracking Timeline

Visualizes individual pothole tracks throughout the video.

### Track Inspector

Allows individual pothole tracks to be selected and inspected.

### Raw Telemetry

Provides access to the complete frame-level detection data.

---

# 📋 Generated Analytics

The system generates two CSV files for each processed road video.

### Frame-Level Telemetry

```text
frame
timestamp_sec
track_id
type
confidence
```

### Unique Pothole Summary

```text
pothole_id
track_id
type
first_frame
last_frame
first_timestamp
last_timestamp
max_confidence
detections
```

The unique summary stores one record for each tracked pothole trajectory.

---

# 🖥️ Applications

## 1. Video Inference Application

The main inference script processes road videos using YOLO26s and ByteTrack.

### Features

* Pothole detection
* Object tracking
* Permanent pothole IDs
* Bounding box visualization
* Confidence display
* Annotated video generation
* Telemetry generation
* Unique pothole reports

Run the inference pipeline:

```bash
python main.py
```

Or specify custom paths:

```bash
python main.py --model best.pt --input potholes_2.mp4
```

---

## 2. Streamlit Analytics Dashboard

The Streamlit application provides a browser-based interface for exploring the results generated by the inference pipeline.

### Features

* Road video selection
* Annotated video playback
* Pothole summaries
* Confidence analysis
* Tracking timeline
* Track inspector
* Raw telemetry viewer

Run the dashboard:

```bash
streamlit run app.py
```

---

# 🛠️ Technologies Used

* Python
* Ultralytics
* YOLO26s
* ByteTrack
* OpenCV
* Streamlit
* Pandas
* Plotly
---

# 📁 Repository Structure

```text
YOLO-Pothole-Detection/
│
├── app.py                         # Streamlit analytics dashboard
├── main.py                        # YOLO + ByteTrack inference
├── README.md
├── requirements.txt
├── LICENSE
│
├── best.pt                        # Trained YOLO model
│
│
├── potholes_1_unique.csv          # Unique pothole summary
└── potholes_2_unique.csv
```

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/SafiUrRehmanAi/YOLO-Pothole-Detection.git
```

Navigate to the project directory:

```bash
cd YOLO-Pothole-Detection
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

### Run Video Inference

```bash
python main.py
```

The inference pipeline generates:

* Annotated road video
* Frame-level telemetry CSV
* Unique pothole CSV

### Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard can then be used to explore the processed videos and their corresponding detection and tracking analytics.

---

# 🚀 Future Improvements

* Improve pothole localization performance
* Experiment with larger YOLO model variants
* Add pothole severity classification
* Add GPS-based pothole localization
* Support real-time camera input
* Optimize inference for edge devices
* Generate automated road-condition reports
* Add more road-defect categories such as cracks and patches
* Explore deployment on roadside/vehicle-mounted cameras

---

# 📜 License

This project is licensed under the MIT License.

## About

Pothole detection and road analytics using YOLO26s, ByteTrack, OpenCV, and Streamlit.
