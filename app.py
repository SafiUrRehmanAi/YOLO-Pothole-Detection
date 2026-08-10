# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from pathlib import Path


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Pothole Detection Analytics",
#     page_icon="🕳️",
#     layout="wide"
# )


# # ============================================================
# # PATHS
# # ============================================================

# WORKSPACE_DIR = Path(__file__).resolve().parent


# VIDEOS = {
#     "Road Video 1": {
#         "video": WORKSPACE_DIR / "potholes_1_output.mp4",
#         "telemetry": WORKSPACE_DIR / "potholes_1_telemetry.csv",
#         "summary": WORKSPACE_DIR / "potholes_1_unique.csv",
#     },
#     "Road Video 2": {
#         "video": WORKSPACE_DIR / "potholes_2_output.mp4",
#         "telemetry": WORKSPACE_DIR / "potholes_2_telemetry.csv",
#         "summary": WORKSPACE_DIR / "potholes_2_unique.csv",
#     },
# }


# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .main {
#         background-color: #f7f9fc;
#     }

#     .dashboard-title {
#         font-size: 38px;
#         font-weight: 700;
#         color: #17202a;
#         margin-bottom: 0px;
#     }

#     .dashboard-subtitle {
#         font-size: 17px;
#         color: #667085;
#         margin-top: 0px;
#         margin-bottom: 25px;
#     }

#     .metric-card {
#         background-color: white;
#         padding: 20px;
#         border-radius: 12px;
#         border: 1px solid #e5e7eb;
#         box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     '<div class="dashboard-title">🕳️ Pothole Detection & Road Analytics</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="dashboard-subtitle">'
#     'YOLO-based pothole detection with ByteTrack object tracking'
#     '</div>',
#     unsafe_allow_html=True
# )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.title("⚙️ Dashboard Controls")

# selected_video = st.sidebar.selectbox(
#     "Select Road Video",
#     list(VIDEOS.keys())
# )

# paths = VIDEOS[selected_video]


# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_csv(path):

#     if not path.exists():
#         return None

#     return pd.read_csv(path)


# telemetry = load_csv(paths["telemetry"])
# summary = load_csv(paths["summary"])


# # ============================================================
# # FILE VALIDATION
# # ============================================================

# if telemetry is None:

#     st.error(
#         f"Telemetry CSV not found:\n\n{paths['telemetry']}"
#     )

#     st.stop()


# if summary is None:

#     st.error(
#         f"Summary CSV not found:\n\n{paths['summary']}"
#     )

#     st.stop()


# # ============================================================
# # NORMALIZE COLUMN NAMES
# # ============================================================

# telemetry.columns = [
#     col.strip().lower()
#     for col in telemetry.columns
# ]

# summary.columns = [
#     col.strip().lower()
#     for col in summary.columns
# ]


# # ============================================================
# # HANDLE TRACK ID COLUMN
# # ============================================================

# if "track_id" not in telemetry.columns:

#     if "pothole_id" in telemetry.columns:
#         telemetry["track_id"] = telemetry["pothole_id"]


# # ============================================================
# # METRICS
# # ============================================================

# if "track_id" in telemetry.columns:

#     total_tracks = telemetry["track_id"].nunique()

# else:

#     total_tracks = len(summary)


# total_detections = len(telemetry)

# average_confidence = telemetry["confidence"].mean()

# max_confidence = telemetry["confidence"].max()

# min_confidence = telemetry["confidence"].min()


# if "timestamp_sec" in telemetry.columns:

#     duration = telemetry["timestamp_sec"].max()

# else:

#     duration = 0


# # ============================================================
# # KPI CARDS
# # ============================================================

# st.subheader("📊 Road Condition Overview")

# col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
#     st.metric(
#         "Tracked Potholes",
#         f"{total_tracks}"
#     )

# with col2:
#     st.metric(
#         "Total Detections",
#         f"{total_detections:,}"
#     )

# with col3:
#     st.metric(
#         "Average Confidence",
#         f"{average_confidence:.1%}"
#     )

# with col4:
#     st.metric(
#         "Maximum Confidence",
#         f"{max_confidence:.1%}"
#     )

# with col5:
#     st.metric(
#         "Video Duration",
#         f"{duration:.2f}s"
#     )


# st.divider()


# # ============================================================
# # VIDEO + SUMMARY
# # ============================================================

# left, right = st.columns([1.5, 1])


# # ============================================================
# # VIDEO
# # ============================================================

# with left:

#     st.subheader("🎥 Annotated Road Footage")

#     video_path = paths["video"]

#     if video_path.exists():

#         st.video(
#             str(video_path)
#         )

#     else:

#         st.warning(
#             f"Output video not found:\n{video_path}"
#         )


# # ============================================================
# # SUMMARY
# # ============================================================

# with right:

#     st.subheader("🕳️ Pothole Summary")

#     if len(summary) > 0:

#         display_columns = [
#             col
#             for col in [
#                 "pothole_id",
#                 "track_id",
#                 "first_timestamp",
#                 "last_timestamp",
#                 "max_confidence",
#                 "detections"
#             ]
#             if col in summary.columns
#         ]

#         st.dataframe(
#             summary[display_columns],
#             use_container_width=True,
#             height=400
#         )

#     else:

#         st.info("No potholes found.")


# # ============================================================
# # CONFIDENCE ANALYSIS
# # ============================================================

# st.divider()

# st.subheader("📈 Detection Confidence Analysis")


# col1, col2 = st.columns(2)


# # ------------------------------------------------------------
# # Confidence over time
# # ------------------------------------------------------------

# with col1:

#     if (
#         "timestamp_sec" in telemetry.columns
#         and "confidence" in telemetry.columns
#     ):

#         confidence_fig = px.scatter(
#             telemetry,
#             x="timestamp_sec",
#             y="confidence",
#             color="track_id",
#             title="Confidence Over Time",
#             labels={
#                 "timestamp_sec": "Time (seconds)",
#                 "confidence": "Confidence",
#                 "track_id": "Track ID"
#             }
#         )

#         confidence_fig.update_layout(
#             height=450,
#             legend_title="Track"
#         )

#         st.plotly_chart(
#             confidence_fig,
#             use_container_width=True
#         )


# # ------------------------------------------------------------
# # Confidence distribution
# # ------------------------------------------------------------

# with col2:

#     confidence_fig2 = px.histogram(
#         telemetry,
#         x="confidence",
#         nbins=20,
#         title="Confidence Distribution",
#         labels={
#             "confidence": "Detection Confidence"
#         },
#         color_discrete_sequence=["#e74c3c"]
#     )

#     confidence_fig2.update_layout(
#         height=450
#     )

#     st.plotly_chart(
#         confidence_fig2,
#         use_container_width=True
#     )


# # ============================================================
# # TRACKING TIMELINE
# # ============================================================

# st.divider()

# st.subheader("🆔 Pothole Tracking Timeline")


# if (
#     "timestamp_sec" in telemetry.columns
#     and "track_id" in telemetry.columns
# ):

#     timeline = (
#         telemetry
#         .groupby("track_id")
#         .agg(
#             first_seen=("timestamp_sec", "min"),
#             last_seen=("timestamp_sec", "max"),
#             detections=("timestamp_sec", "count"),
#             confidence=("confidence", "mean")
#         )
#         .reset_index()
#     )

#     timeline["duration"] = (
#         timeline["last_seen"]
#         - timeline["first_seen"]
#     )

#     timeline_fig = px.scatter(
#         timeline,
#         x="first_seen",
#         y="track_id",
#         size="detections",
#         color="confidence",
#         hover_data=[
#             "last_seen",
#             "duration",
#             "detections"
#         ],
#         color_continuous_scale="RdYlGn",
#         title="Tracked Potholes Through Video",
#         labels={
#             "first_seen": "First Detection (seconds)",
#             "track_id": "Track ID",
#             "confidence": "Average Confidence"
#         }
#     )

#     timeline_fig.update_layout(
#         height=500
#     )

#     st.plotly_chart(
#         timeline_fig,
#         use_container_width=True
#     )


# # ============================================================
# # DETECTIONS PER TRACK
# # ============================================================

# st.subheader("📊 Detection Frequency by Track")


# track_counts = (
#     telemetry["track_id"]
#     .value_counts()
#     .reset_index()
# )

# track_counts.columns = [
#     "track_id",
#     "detections"
# ]


# bar_fig = px.bar(
#     track_counts,
#     x="track_id",
#     y="detections",
#     color="detections",
#     color_continuous_scale="Reds",
#     title="Number of Frames Each Track Was Detected",
#     labels={
#         "track_id": "Track ID",
#         "detections": "Number of Detections"
#     }
# )

# st.plotly_chart(
#     bar_fig,
#     use_container_width=True
# )


# # ============================================================
# # DETAILED TRACK INSPECTOR
# # ============================================================

# st.divider()

# st.subheader("🔍 Track Inspector")


# available_tracks = sorted(
#     telemetry["track_id"].unique()
# )

# selected_track = st.selectbox(
#     "Select a Track ID",
#     available_tracks
# )


# track_data = telemetry[
#     telemetry["track_id"] == selected_track
# ].copy()


# col1, col2, col3, col4 = st.columns(4)


# with col1:

#     st.metric(
#         "Track ID",
#         selected_track
#     )


# with col2:

#     st.metric(
#         "Detections",
#         len(track_data)
#     )


# with col3:

#     st.metric(
#         "Average Confidence",
#         f"{track_data['confidence'].mean():.1%}"
#     )


# with col4:

#     st.metric(
#         "Best Confidence",
#         f"{track_data['confidence'].max():.1%}"
#     )


# st.dataframe(
#     track_data,
#     use_container_width=True,
#     height=300
# )


# # ============================================================
# # RAW DATA
# # ============================================================

# with st.expander("📋 View Complete Telemetry Data"):

#     st.dataframe(
#         telemetry,
#         use_container_width=True,
#         height=500
#     )


# # ============================================================
# # FOOTER
# # ============================================================

# st.divider()

# st.caption(
#     "Pothole Detection & Road Analytics | "
#     "YOLO + ByteTrack + Streamlit"
# )







import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Pothole Detection Analytics",
    page_icon="🕳️",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

WORKSPACE_DIR = Path(__file__).resolve().parent

VIDEOS = {
    "Road Video 1": {
        # Browser-compatible H.264 video
        "video": WORKSPACE_DIR / "potholes_1_web.mp4",

        "telemetry": WORKSPACE_DIR / "potholes_1_telemetry.csv",

        "summary": WORKSPACE_DIR / "potholes_1_unique.csv",
    },

    "Road Video 2": {
        # Browser-compatible H.264 video
        "video": WORKSPACE_DIR / "potholes_2_web.mp4",

        "telemetry": WORKSPACE_DIR / "potholes_2_telemetry.csv",

        "summary": WORKSPACE_DIR / "potholes_2_unique.csv",
    },
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        color: #17202a;
        margin-bottom: 0px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #667085;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🕳️ Pothole Detection & Road Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'YOLO-based pothole detection with ByteTrack object tracking'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Dashboard Controls")

selected_video = st.sidebar.selectbox(
    "Select Road Video",
    list(VIDEOS.keys())
)

paths = VIDEOS[selected_video]


# ============================================================
# LOAD CSV DATA
# ============================================================

@st.cache_data
def load_csv(path):

    if not path.exists():
        return None

    return pd.read_csv(path)


telemetry = load_csv(paths["telemetry"])
summary = load_csv(paths["summary"])


# ============================================================
# FILE VALIDATION
# ============================================================

if telemetry is None:

    st.error(
        f"Telemetry CSV not found:\n\n{paths['telemetry']}"
    )

    st.stop()


if summary is None:

    st.error(
        f"Summary CSV not found:\n\n{paths['summary']}"
    )

    st.stop()


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

telemetry.columns = [
    col.strip().lower()
    for col in telemetry.columns
]

summary.columns = [
    col.strip().lower()
    for col in summary.columns
]


# ============================================================
# HANDLE TRACK ID COLUMN
# ============================================================

if "track_id" not in telemetry.columns:

    if "pothole_id" in telemetry.columns:

        telemetry["track_id"] = telemetry["pothole_id"]


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "confidence"
]

missing_columns = [
    col
    for col in required_columns
    if col not in telemetry.columns
]

if missing_columns:

    st.error(
        "The telemetry CSV is missing these columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# METRICS
# ============================================================

if "track_id" in telemetry.columns:

    total_tracks = telemetry["track_id"].nunique()

else:

    total_tracks = len(summary)


total_detections = len(telemetry)

average_confidence = telemetry["confidence"].mean()

max_confidence = telemetry["confidence"].max()

min_confidence = telemetry["confidence"].min()


if "timestamp_sec" in telemetry.columns:

    duration = telemetry["timestamp_sec"].max()

else:

    duration = 0


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Road Condition Overview")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Tracked Potholes",
        f"{total_tracks}"
    )


with col2:

    st.metric(
        "Total Detections",
        f"{total_detections:,}"
    )


with col3:

    st.metric(
        "Average Confidence",
        f"{average_confidence:.1%}"
    )


with col4:

    st.metric(
        "Maximum Confidence",
        f"{max_confidence:.1%}"
    )


with col5:

    st.metric(
        "Video Duration",
        f"{duration:.2f}s"
    )


st.divider()


# ============================================================
# VIDEO + SUMMARY
# ============================================================

left, right = st.columns([1.5, 1])


# ============================================================
# VIDEO
# ============================================================

with left:

    st.subheader("🎥 Annotated Road Footage")

    video_path = paths["video"]

    if video_path.exists():

        st.video(
            str(video_path)
        )

    else:

        st.error(
            "Web-compatible video not found:\n\n"
            f"{video_path}\n\n"
            "Make sure you converted the output video "
            "using FFmpeg."
        )


# ============================================================
# SUMMARY
# ============================================================

with right:

    st.subheader("🕳️ Pothole Summary")

    if len(summary) > 0:

        display_columns = [
            col
            for col in [
                "pothole_id",
                "track_id",
                "first_timestamp",
                "last_timestamp",
                "max_confidence",
                "detections"
            ]
            if col in summary.columns
        ]

        st.dataframe(
            summary[display_columns],
            use_container_width=True,
            height=400
        )

    else:

        st.info("No potholes found.")


# ============================================================
# CONFIDENCE ANALYSIS
# ============================================================

st.divider()

st.subheader("📈 Detection Confidence Analysis")

col1, col2 = st.columns(2)


# ============================================================
# CONFIDENCE OVER TIME
# ============================================================

with col1:

    if (
        "timestamp_sec" in telemetry.columns
        and "confidence" in telemetry.columns
        and "track_id" in telemetry.columns
    ):

        confidence_fig = px.scatter(
            telemetry,
            x="timestamp_sec",
            y="confidence",
            color="track_id",
            title="Confidence Over Time",
            labels={
                "timestamp_sec": "Time (seconds)",
                "confidence": "Confidence",
                "track_id": "Track ID"
            }
        )

        confidence_fig.update_layout(
            height=450,
            legend_title="Track"
        )

        st.plotly_chart(
            confidence_fig,
            use_container_width=True
        )


# ============================================================
# CONFIDENCE DISTRIBUTION
# ============================================================

with col2:

    confidence_fig2 = px.histogram(
        telemetry,
        x="confidence",
        nbins=20,
        title="Confidence Distribution",
        labels={
            "confidence": "Detection Confidence"
        },
        color_discrete_sequence=["#e74c3c"]
    )

    confidence_fig2.update_layout(
        height=450
    )

    st.plotly_chart(
        confidence_fig2,
        use_container_width=True
    )


# ============================================================
# TRACKING TIMELINE
# ============================================================

st.divider()

st.subheader("🆔 Pothole Tracking Timeline")


if (
    "timestamp_sec" in telemetry.columns
    and "track_id" in telemetry.columns
):

    timeline = (
        telemetry
        .groupby("track_id")
        .agg(
            first_seen=("timestamp_sec", "min"),
            last_seen=("timestamp_sec", "max"),
            detections=("timestamp_sec", "count"),
            confidence=("confidence", "mean")
        )
        .reset_index()
    )

    timeline["duration"] = (
        timeline["last_seen"]
        - timeline["first_seen"]
    )

    timeline_fig = px.scatter(
        timeline,
        x="first_seen",
        y="track_id",
        size="detections",
        color="confidence",
        hover_data=[
            "last_seen",
            "duration",
            "detections"
        ],
        color_continuous_scale="RdYlGn",
        title="Tracked Potholes Through Video",
        labels={
            "first_seen": "First Detection (seconds)",
            "track_id": "Track ID",
            "confidence": "Average Confidence"
        }
    )

    timeline_fig.update_layout(
        height=500
    )

    st.plotly_chart(
        timeline_fig,
        use_container_width=True
    )


# ============================================================
# DETECTIONS PER TRACK
# ============================================================

st.subheader("📊 Detection Frequency by Track")


if "track_id" in telemetry.columns:

    track_counts = (
        telemetry["track_id"]
        .value_counts()
        .reset_index()
    )

    track_counts.columns = [
        "track_id",
        "detections"
    ]

    bar_fig = px.bar(
        track_counts,
        x="track_id",
        y="detections",
        color="detections",
        color_continuous_scale="Reds",
        title="Number of Frames Each Track Was Detected",
        labels={
            "track_id": "Track ID",
            "detections": "Number of Detections"
        }
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )


# ============================================================
# DETAILED TRACK INSPECTOR
# ============================================================

st.divider()

st.subheader("🔍 Track Inspector")


if "track_id" in telemetry.columns:

    available_tracks = sorted(
        telemetry["track_id"].unique()
    )

    selected_track = st.selectbox(
        "Select a Track ID",
        available_tracks
    )

    track_data = telemetry[
        telemetry["track_id"] == selected_track
    ].copy()

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Track ID",
            selected_track
        )


    with col2:

        st.metric(
            "Detections",
            len(track_data)
        )


    with col3:

        st.metric(
            "Average Confidence",
            f"{track_data['confidence'].mean():.1%}"
        )


    with col4:

        st.metric(
            "Best Confidence",
            f"{track_data['confidence'].max():.1%}"
        )


    st.dataframe(
        track_data,
        use_container_width=True,
        height=300
    )


# ============================================================
# RAW DATA
# ============================================================

with st.expander("📋 View Complete Telemetry Data"):

    st.dataframe(
        telemetry,
        use_container_width=True,
        height=500
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Pothole Detection & Road Analytics | "
    "YOLO + ByteTrack + Streamlit"
)