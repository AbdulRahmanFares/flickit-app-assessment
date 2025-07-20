# Computer Vision Engineer Assignment

## Overview

This project implements a comprehensive computer vision system for analyzing sports videos, specifically focusing on player interactions with a ball. The system provides real-time analysis of:

- **Touch Counting**: Right and left leg touch detection and counting
- **Ball Rotation**: Estimation of ball spin direction (forward/backward) using hybrid optical flow method
- **Player Velocity**: Movement velocity calculation at each touch point
- **Dynamic Visualization**: Real-time overlays and annotations with output video saving

## Project Structure

```
flickit-app-assessment/
├── src/                          # Source code (modular architecture)
│   ├── __init__.py
│   ├── main.py                   # Entry point
│   ├── video_io.py              # Video reading/writing utilities
│   ├── detection.py             # Player/ball detection (YOLOv11)
│   ├── pose.py                  # Pose estimation (MediaPipe)
│   ├── touch_counter.py         # Touch detection and counting
│   ├── ball_spin.py             # Ball spin estimation (hybrid method)
│   ├── velocity.py              # Player velocity calculation
│   └── overlay.py               # Drawing/annotation utilities
├── models/                       # Model weights
│   └── yolo11n.pt              # YOLOv11 model file
├── assessment_video.mp4          # Input video
├── output_annotated.mp4         # Output video with annotations
├── requirements.txt              # Python dependencies
├── requirements.in               # Source dependencies for uv
├── REPORT.md                     # Detailed technical report
└── README.md                     # This file
```

## Features

### 1. Touch Counting & Leg Identification
- **Detection**: YOLOv11 for player and ball detection
- **Pose Estimation**: MediaPipe for body keypoint extraction
- **Touch Logic**: Distance-based touch detection with rising edge counting
- **Visualization**: Real-time touch counts and leg keypoints

### 2. Ball Rotation Estimation
- **Hybrid Method**: Optical flow + rule-based classifier
- **Features**: Mean and standard deviation of flow vectors
- **Classification**: Forward Spin, Backspin, or No Spin
- **Accuracy**: Optimized for visible ball features

### 3. Player Movement Velocity
- **Tracking**: Mid-hip position using pose keypoints
- **Calculation**: Distance/time-based velocity at touch events
- **Units**: Pixels per second (can be calibrated for real-world units)

### 4. Dynamic Visualization
- **Real-time Overlays**: Touch counts, ball direction, velocity
- **Keypoint Visualization**: Leg tracking for debugging
- **Output Video**: Saves annotated video with all features

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast dependency management and Python 3.10 for compatibility with all required packages.

### Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) installed
- [uv](https://github.com/astral-sh/uv) installed

### Setup

1. **Install Python 3.10**:
   ```bash
   pyenv install 3.10.14
   ```

2. **Create a uv Virtual Environment with Python 3.10**:
   ```bash
   uv venv flickit-app-assessment-venv --python $(pyenv root)/versions/3.10.14/bin/python
   ```

3. **Activate the environment**:
   ```bash
   source flickit-app-assessment-venv/bin/activate
   ```

4. **Compile Dependencies**:
   ```bash
   uv pip compile requirements.in -o requirements.txt
   ```

5. **Install Dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Basic Usage

1. **Place your input video** as `assessment_video.mp4` in the project root.

2. **Run the analysis**:
   ```bash
   python -m src.main
   ```

3. **View results**:
   - Real-time display with annotations
   - Press `q` to quit
   - Output saved as `output_annotated.mp4`

### Advanced Usage

You can modify individual components:

```python
# Custom detection threshold
touch_counter = TouchCounter(threshold=60)

# Custom model path
detector = Detector(model_path='models/custom_model.pt')

# Custom velocity calculation
velocity_calc = VelocityCalculator(fps=60.0)
```

## Architecture & SOLID Principles

### Single Responsibility Principle
- Each class has one specific responsibility
- `Detector`: Object detection only
- `PoseEstimator`: Pose estimation only
- `TouchCounter`: Touch detection and counting only

### Open/Closed Principle
- Classes are open for extension but closed for modification
- New spin classifiers can be added without changing existing code
- Different detection models can be swapped easily

### Liskov Substitution Principle
- Interfaces allow for easy swapping of implementations
- Detection, pose estimation, and spin estimation are modular

### Interface Segregation Principle
- Only relevant methods are exposed per module
- Clean, focused APIs for each component

### Dependency Inversion Principle
- High-level modules depend on abstractions
- Easy to test and maintain

## Dependencies

- **OpenCV**: Video processing and optical flow
- **Ultralytics YOLOv11**: Object detection
- **MediaPipe**: Pose estimation
- **NumPy**: Numerical operations
- **PyTorch**: Deep learning framework

## Performance

- **Real-time Processing**: Optimized for live video analysis
- **Memory Efficient**: Modular design reduces memory footprint
- **Scalable**: Easy to add new features or models

## Limitations & Future Improvements

### Current Limitations
- Ball spin accuracy depends on ball size and visible features
- Velocity in pixels/second (requires calibration for real-world units)
- Touch detection threshold may need tuning for different video resolutions

### Future Improvements
- Deep learning-based spin estimation (RAFT-lite, PWC-Net)
- Camera calibration for real-world velocity units
- Multi-player support
- Advanced ball tracking algorithms
- Machine learning-based touch detection

---

## Quick Start

```bash
# Install and run
uv pip install -r requirements.txt
python -m src.main
```

The system will process `assessment_video.mp4` and save the annotated output as `output_annotated.mp4`.
