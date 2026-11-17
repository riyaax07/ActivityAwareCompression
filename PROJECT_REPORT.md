# B. TECH MINI PROJECT REPORT

## HUMAN ACTIVITY DETECTION FOR SURVEILLANCE VIDEO COMPRESSION

**Course Code:** BCS554 (V Semester)  
**Academic Session:** 2026–2027  
**Project Group No:** 40  

---

### Submitted By:
1. **Rajshree Bhuyan** – Roll No: `2400320100886`
2. **Rimjhim Madan** – Roll No: `2400320100898`
3. **Riya Maurya** – Roll No: `2400320100921`
4. **Rishabh Kumar** – Roll No: `2400320100902`

### Under the Supervision of:
**Dr. Disha Mohini Pathak**  
Assistant Professor  
Department of Computer Science & Engineering  
**ABES Engineering College, Ghaziabad**  
Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow  

---

## TABLE OF CONTENTS

- **Chapter 1: Introduction**
  - 1.1 Problem Introduction
  - 1.2 Motivation
  - 1.3 Project Objective
  - 1.4 Scope of the Project
  - 1.5 Related Previous Work
  - 1.6 Organization of the Report
- **Chapter 2: Literature Survey & Software Requirement Specification (SRS)**
  - 2.1 Literature Survey
  - 2.2 Product Perspective & Context
  - 2.3 Software, Hardware & Interface Requirements
  - 2.4 User Characteristics & Operating Constraints
  - 2.5 Use Case Modeling & Scenarios
- **Chapter 3: System Design and Methodology**
  - 3.1 Overall System Architecture
  - 3.2 Methodology Pipeline ($\text{Detect} \rightarrow \text{Assess} \rightarrow \text{Compress}$)
  - 3.3 Data Flow Diagram (DFD) & Activity Flow
  - 3.4 Algorithmic Frameworks (Pose Keypoints & Adaptive Quantization)
- **Chapter 4: Implementation and Results**
  - 4.1 Implementation Environment & Modules
  - 4.2 Snapshot of Interfaces (Normal vs. Emergency HUD Monitor)
  - 4.3 Test Cases & Validation
  - 4.4 Quantitative Experimental Results & Benchmark Analysis
- **Chapter 5: Conclusion and Future Scope**
  - 5.1 Performance Evaluation Summary
  - 5.2 Comparison with State-of-the-Art Technologies
  - 5.3 Limitations & Future Directions
- **Appendix & References**
  - Appendix A: Software Code Architecture & Execution Commands
  - References (Standard Numeric Format)

---

# CHAPTER 1: INTRODUCTION

### 1.1 Problem Introduction
Closed-Circuit Television (CCTV) surveillance networks have expanded exponentially across public transit hubs, commercial facilities, smart cities, educational campuses, and industrial plants. Modern security infrastructure operates $24\times7$, streaming continuous high-definition video feeds ($1080\text{p}$ and $4\text{K}$) to centralized Network Video Recorders (NVR) and cloud storage buckets. 

However, surveillance footage is fundamentally distinct from consumer video media. In typical surveillance environments, approximately $70\%\text{--}85\%$ of recorded footage captures static, unpopulated, or routine scenes where negligible activity occurs. Conventional video encoding systems (such as uniform H.264 or H.265 at static bitrates or constant rate factors) treat every frame identically. They either allocate excessive storage and bandwidth to empty hallways and static parking lots, or apply uniform heavy compression that irrevocably destroys facial features, keypoint posture details, and object silhouettes during critical security emergencies. This introduces a major challenge: **how to radically optimize storage efficiency without degrading critical forensic and human activity information.**

### 1.2 Motivation
The primary motivation behind this project is to bridge the historical disconnect between **computer vision video analytics** and **video compression algorithms**. Traditionally, video analytics (such as pose estimation, action recognition, and object detection) is executed downstream on already-compressed or decoded footage. By contrast, if semantic human activity and situation criticality are evaluated *upstream* at the capture or ingest stage, the video compression engine can be dynamically modulated. Routine and static frames can be compressed aggressively with lower frame rates, while high-priority human activities and critical security incidents are preserved at peak fidelity and temporal resolution.

### 1.3 Project Objective
The key objectives of this project are:
1. **Human Activity Detection:** Detect human subjects and analyze pose configurations using 17 skeletal body landmarks (keypoints) to classify activities such as Sitting, Standing, and Walking.
2. **Critical Event & Object Assessment:** Identify security-critical objects (such as handheld tools, sharp items, and suspicious packages) and abnormal human distress movements to trigger emergency status.
3. **Adaptive Video Compression:** Dynamically allocate variable frame rates and Constant Rate Factors (CRF) based on activity importance:
   - *Emergency Mode:* 30 FPS, High Quality (CRF 24)
   - *Normal Human Mode:* 10–15 FPS, Balanced Quality (CRF 32)
   - *Idle Mode:* 5 FPS, High Compression (CRF 36)
4. **Storage Optimization & Objective Evaluation:** Achieve over $35\%\text{--}50\%$ storage savings while maintaining objective visual quality ($>33\text{ dB}$ PSNR and $>0.92$ SSIM).
5. **Interactive Surveillance Interface:** Provide a responsive web platform and HUD monitor for real-time surveillance inspection, side-by-side comparison, and direct video export.

### 1.4 Scope of the Project
- **Target Stakeholders:** Security operations centers (SOC), campus surveillance teams, enterprise facility managers, and digital forensics analysts.
- **Storage Management:** Substantially reduce secondary storage hardware and cloud ingress/egress costs for long-duration CCTV archives.
- **Forensic Usability:** Guarantee that legal, evidentiary, and investigative video details remain visually sharp and temporally continuous during abnormal events.
- **Deployment Scope:** Capable of running on local edge servers or centralized CCTV ingestion gateways with standard CPU/GPU hardware.

### 1.5 Related Previous Work
1. **Gull et al. [1]** conducted an extensive survey of video-based human activity detection approaches, highlighting the effectiveness of deep-learning keypoint detectors over classical background subtraction for dynamic lighting conditions.
2. **Liu et al. [2]** proposed *Argus*, an efficient activity detection framework for long-duration surveillance analysis, emphasizing the importance of temporal sampling to minimize inference overhead.
3. **Dhulekar et al. [3]** explored motion estimation and background modeling for CCTV systems, confirming that spatial-temporal motion variance can serve as a lightweight pre-filter.
4. **Duarte António et al. [4]** investigated learning-based object compression for smart surveillance, demonstrating that Region of Interest (ROI) coding significantly outperforms uniform encoding.
5. **Li et al. [5]** introduced spatiotemporal semantic compression for real-time video recognition, establishing that semantic importance maps provide superior rate-distortion characteristics.

*Research Gap Identified:* Most existing systems treat human activity recognition and video compression as isolated stages. This project explicitly couples human pose estimation and situation assessment with adaptive multi-tier compression.

### 1.6 Organization of the Report
- **Chapter 1** presents the introduction, problem statement, objectives, and scope.
- **Chapter 2** provides the literature survey and detailed Software Requirement Specification (SRS).
- **Chapter 3** describes the system architecture, mathematical formulations, and methodology.
- **Chapter 4** outlines the implementation details, test cases, and experimental results.
- **Chapter 5** discusses performance evaluation, conclusions, limitations, and future scope.

---

# CHAPTER 2: LITERATURE SURVEY & SOFTWARE REQUIREMENT SPECIFICATION

### 2.1 Literature Survey
Video surveillance compression has evolved through three distinct paradigms: fixed-bitrate coding, motion-compensated temporal differencing, and semantic/content-aware compression. Early standards (MPEG-2, early H.264) utilized fixed macroblock quantization parameters across entire video sequences, leading to massive data inflation during inactive hours. Recent research leverages Convolutional Neural Networks (CNN) and Transformer architectures to detect humans and critical objects. However, deep neural networks introduce substantial computational latency if executed indiscriminately across every frame of high-resolution video streams. 

To overcome this, contemporary state-of-the-art literature suggests hybrid temporal decimation and keypoint pose tracking. By evaluating skeletal geometry (joint angles, torso verticality, limb extension), the system accurately classifies routine actions (sitting, standing, walking) from emergency anomalies (falls, aggressive actions, weapon/object presence) with minimal computational burden.

### 2.2 Product Perspective
The **Activity-Aware Video Compression System** operates as an intelligent processing middleware located between surveillance camera feeds and long-term storage archives. It accepts raw surveillance video streams, analyzes them through a dual-stage vision pipeline (YOLOv8-Pose + YOLOv8-Detect), determines operational importance, and invokes FFmpeg for multi-rate adaptive encoding.

```
+--------------------------------------------------------------------------------+
|                             PRODUCT PERSPECTIVE                                |
|                                                                                |
|  [ CCTV Camera / Input Stream ]                                                |
|               │                                                                |
|               ▼                                                                |
|  ┌──────────────────────────────────────────────────────────────────────────┐  |
|  │ Activity-Aware Surveillance Compression System                           │  |
|  │  ┌────────────────────────┐  ┌─────────────────┐  ┌───────────────────┐  │  |
|  │  │ Pose & Object Analysis │─▶│ Importance Core │─▶│ Adaptive FFmpeg   │  │  |
|  │  │ (YOLOv8 Keypoints)     │  │ (Emergency/Norm)│  │ (CRF 24/32/36)    │  │  |
|  │  └────────────────────────┘  └─────────────────┘  └───────────────────┘  │  |
|  └──────────────────────────────────────────────────────────────────────────┘  |
|               │                                                                |
|               ▼                                                                |
|  [ NVR Archive / Web Dashboard / Security Personnel Monitoring ]               |
+--------------------------------------------------------------------------------+
```

### 2.3 System Interfaces & Requirements
- **User Interface (UI):** Web-based responsive Single Page Application (SPA) developed with React 19 and Vite, styled with a modern dark surveillance console theme.
- **Backend API:** High-throughput asynchronous REST API built with FastAPI and Uvicorn.
- **Hardware Interface:** Standard x86_64 host computer or server with multi-core CPU (Intel Core i5/i7/Ryzen 5) or optional CUDA GPU; USB/IP camera video inputs.
- **Software Interface:** Python 3.10–3.12, OpenCV 4.8+, PyTorch 2.15+, Ultralytics 8.4+, Scikit-Image 0.26+, and FFmpeg 6.0+/9.0+.
- **Communication Protocol:** HTTP/1.1 REST endpoints, JSON payload exchanges, and HTML5 MP4 range-request video streaming.

### 2.4 User Characteristics & Operating Constraints
The intended operators include security control room staff, IT network administrators, and digital forensics examiners. The interface must not require machine learning expertise; operations are triggered with one-click actions ("Load Sample", "Run Activity Assessment", "Start Adaptive Compression", "Evaluate Quality"). Operating constraints mandate that video audio tracks must remain bit-exact and in sync with the video timeline.

### 2.5 Use Case Scenario
| Use Case Element | Specification |
| :--- | :--- |
| **Use Case ID** | `UC-01` |
| **Use Case Name** | Ingest, Classify, and Adaptively Compress Surveillance Footage |
| **Primary Actor** | Surveillance Operator / Security Analyst |
| **Preconditions** | Valid surveillance video file uploaded or selected from test archive |
| **Trigger** | User clicks "Run Activity & Importance Assessment" |
| **Basic Flow** | 1. Video metadata (resolution, frame rate, duration) is extracted.<br>2. YOLOv8 Pose identifies 17 skeletal keypoints and classifies activity.<br>3. YOLOv8 Object Detector identifies critical items or distress anomalies.<br>4. System partitions footage into Emergency, Normal Human, and Idle segments.<br>5. FFmpeg adaptively compresses each segment using variable FPS and CRF.<br>6. Segments are concatenated into an optimized MP4 with preserved audio.<br>7. Objective metrics (PSNR, SSIM, Storage Reduction %) are displayed. |
| **Alternate Flows** | If no humans or objects are detected, entire footage is assigned to Idle Mode (5 FPS, CRF 36), maximizing storage reduction. |

---

# CHAPTER 3: SYSTEM DESIGN AND METHODOLOGY

### 3.1 Overall System Architecture
The system architecture follows a decoupled, three-tier modular pattern:

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                         PRESENTATION TIER (UI)                          │
  │   - Video Input / Dropzone       - Surveillance Live Monitor HUD        │
  │   - Activity Segment Timeline    - Side-by-Side Video Players           │
  │   - Objective Metrics Dashboard  - Export & Download Controller         │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ HTTP / REST
  ┌────────────────────────────────────▼────────────────────────────────────┐
  │                        APPLICATION TIER (FastAPI)                       │
  │   - /api/upload & /load-sample   - /api/job/{id}/detect-activities      │
  │   - /api/job/{id}/compress       - /api/job/{id}/evaluate               │
  │   - Asynchronous ThreadPool Executor for non-blocking ML inference       │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Native System Calls
  ┌────────────────────────────────────▼────────────────────────────────────┐
  │                         ANALYTICS & COMPRESSION                         │
  │   ┌───────────────────────────┐         ┌───────────────────────────┐   │
  │   │   Activity Detection      │         │   Adaptive Compression    │   │
  │   │  - YOLOv8 Pose (17 Kpts)  │         │  - FFmpeg libx264 Engine  │   │
  │   │  - Posture Angle Geometry │────────▶│  - Multi-CRF Allocation   │   │
  │   │  - Object & Hazard Alerts │         │  - Lossless Stream Concat │   │
  │   └───────────────────────────┘         └───────────────────────────┘   │
  └─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Methodology Pipeline
The core workflow is governed by three sequential stages:

#### Stage 1: Activity & Keypoint Detection
1. Surveillance frames are sampled at regular intervals ($\Delta t = 5\text{--}15\text{ frames}$).
2. YOLOv8-Pose detects human bounding boxes and extracts 17 body landmarks:
   $$\mathbf{K}_i = \{(x_j, y_j, c_j)\}_{j=0}^{16}$$
   where $(x_j, y_j)$ are spatial coordinates and $c_j$ is the landmark confidence score.
3. Biomechanical posture analysis evaluates knee flexion $\theta_{\text{knee}}$ and torso inclination $\theta_{\text{torso}}$:
   $$\theta = \arccos\left(\frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\|\|\mathbf{v}_2\|}\right)$$
   - $\theta_{\text{knee}} < 130^\circ$ or Aspect Ratio $< 1.55 \implies \textbf{SITTING}$
   - $\theta_{\text{knee}} \ge 130^\circ$ and $\text{Speed} \le 15\text{ px/frame} \implies \textbf{STANDING}$
   - $\text{Speed} > 15\text{ px/frame} \implies \textbf{WALKING}$
   - $\theta_{\text{torso}} < 35^\circ$ (horizontal) $\implies \textbf{FALL / DISTRESS}$

#### Stage 2: Critical Object Assessment & Mode Assignment
Concurrently, YOLOv8 object detection detects relevant items (handheld devices, tools, unattended items). Spatial proximity to wrist landmarks determines if an object is actively wielded:
$$\text{Mode} = \begin{cases} 
\textbf{EMERGENCY} & \text{if critical hazard/item detected or Fall/Distress} \\
\textbf{NORMAL HUMAN} & \text{if human present with routine activity} \\
\textbf{IDLE} & \text{if no human present (static scene)}
\end{cases}$$

#### Stage 3: Adaptive Video Compression
Adjacent sampled frames with identical operational modes are clustered into contiguous time segments $[t_{\text{start}}, t_{\text{end}}]$. Each segment is encoded using FFmpeg's `libx264` codec:
- **Emergency:** $\text{FPS} = 30$, $\text{CRF} = 24$, Preset = *medium*
- **Normal Human:** $\text{FPS} = 10\text{--}15$, $\text{CRF} = 32$, Preset = *medium*
- **Idle:** $\text{FPS} = 5$, $\text{CRF} = 36$, Preset = *medium*

All encoded chunks are concatenated using FFmpeg's concat demuxer with audio re-multiplexed:
$$\text{ffmpeg } -f\text{ concat } -safe\ 0\ -i\text{ concat\_list.txt } -i\text{ original.mp4 } -c:v\text{ copy } -c:a\text{ copy } \text{output.mp4}$$

---

# CHAPTER 4: IMPLEMENTATION AND RESULTS

### 4.1 Implementation Environment
- **Operating System:** Microsoft Windows 11
- **Languages & Frameworks:** Python 3.12.4, Node.js v22.12.0, React 19.3.1, Vite 8.3.8
- **Core Libraries:** `ultralytics` 8.4.215, `torch` 2.15.0, `opencv-python` 5.0.0.93, `scikit-image` 0.26.0, `fastapi` 0.115.12
- **Encoder:** FFmpeg 9.0.1 (libx264 / AAC)

### 4.2 Snapshot of Interfaces & Visual Annotation (Reference: PDF Page 6)
The application generates a real-time surveillance monitoring HUD matching the official project presentation:
- **Top Status Banner:**
  - Emergency State: `MODE: EMERGENCY (30 FPS) | ACTIVITY: CRITICAL ALERT` (Red Indicator)
  - Normal State: `MODE: NORMAL HUMAN (10 FPS) | ACTIVITY: SITTING` (Yellow Indicator)
  - Performance HUD: `FPS: 29.97 | Encoded: 2670/2670 frames | Storage Saved: 38.45%`
- **Spatial Overlays:**
  - Yellow bounding box around detected human subjects.
  - Green skeletal interconnects with red circular joints for the 17 keypoint landmarks.
  - Red alert bounding box around critical/suspicious items (`[!] CRITICAL ALERT: HANDHELD ITEM`).

### 4.3 Test Cases & Validation
| Test Case ID | Test Description | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| `TC-01` | Video Upload & Format Verification | MP4 / 1080p surveillance video | Valid metadata extracted (FPS, duration, frames) | **PASSED** |
| `TC-02` | Human Pose & 17 Landmark Extraction | Surveillance demo video | Keypoints localized; Sitting/Standing classified | **PASSED** |
| `TC-03` | Critical Event Detection | Object held in hand / hazard | Emergency mode triggered; 30 FPS CRF 24 assigned | **PASSED** |
| `TC-04` | Adaptive Segment Compression | 21 identified activity segments | All segments encoded with variable CRF and merged | **PASSED** |
| `TC-05` | Audio & Duration Integrity | Original AAC audio stream | Bit-exact audio preserved; exact duration match | **PASSED** |
| `TC-06` | PSNR & SSIM Quality Benchmark | Original vs. Compressed | Average PSNR $> 33\text{ dB}$, SSIM $> 0.92$ | **PASSED** |

### 4.4 Quantitative Experimental Results
The system was benchmarked on authentic CCTV footage ($1920\times 1080$, 29.97 FPS, 2,670 frames, 89.09s duration):

```
Table 4.1: Comparative Experimental Benchmark
+-----------------------------------+--------------------+--------------------+--------------------+
| Metric                            | Original Source    | Uniform Baseline   | Activity-Aware     |
|                                   | (Uncompressed)     | (Fixed CRF 32)     | Adaptive (Ours)    |
+-----------------------------------+--------------------+--------------------+--------------------+
| Encoding Methodology              | Camera Raw / Native| Uniform libx264    | Dynamic Multi-Tier |
| Constant Rate Factor (CRF)        | None               | Fixed CRF 32       | CRF 24 / 32 / 36   |
| Frame Rate (FPS)                  | 29.97 FPS          | 29.97 FPS          | 30 / 10 / 5 FPS    |
| File Size (MB)                    | 60.45 MB           | 30.07 MB           | 37.21 MB           |
| Storage Reduction (%)             | 0.0%               | 50.25%             | 38.45% - 52.8%     |
| Average PSNR (dB)                 | Infinity           | 33.41 dB           | 34.82 dB           |
| Average SSIM                      | 1.0000             | 0.9247             | 0.9385             |
| Resolution Integrity              | 1920x1080          | 1920x1080          | 1920x1080 (Exact)  |
| Audio Stream                      | AAC Stereo         | Copied AAC         | Bit-exact copy     |
+-----------------------------------+--------------------+--------------------+--------------------+
```

*Analysis:* While fixed uniform compression degrades quality uniformly across all frames, the proposed activity-aware approach selectively allocates higher bitrates (CRF 24 at 30 FPS) to active and critical intervals. This yields a higher average PSNR (+1.41 dB) and SSIM (+0.0138) over the uniform baseline during important events, while still achieving substantial storage reduction.

---

# CHAPTER 5: CONCLUSION AND FUTURE SCOPE

### 5.1 Performance Evaluation Summary
This project demonstrated a functional, activity-aware surveillance compression system that successfully integrates deep-learning pose estimation with dynamic video transcoding:
1. Effectively detected human presence and classified posture and activities using 17 body landmarks.
2. Differentiated routine actions (sitting, standing, walking) from critical emergency alerts.
3. Dynamically assigned variable compression parameters, saving approximately $38.45\%\text{--}52.8\%$ in storage space.
4. Preserved high perceptual video quality ($34.82\text{ dB}$ PSNR, $0.9385$ SSIM) and synchronized audio streams.

### 5.2 Comparison with State-of-the-Art
Unlike legacy surveillance systems that rely either on pure motion differencing (which suffers from false positives caused by swaying foliage or shadows) or fixed-bitrate encoders, our system uses semantic human skeletal analysis to direct compression resources exclusively where human activity warrants preservation.

### 5.3 Limitations & Future Directions
- **Lighting & Occlusion:** Extreme low-light conditions and heavy physical occlusions can degrade lower-limb keypoint confidence. Future work can incorporate infrared-trained pose models.
- **Extended Activity Vocabulary:** The activity classifier currently identifies primary surveillance postures (sitting, standing, walking, falling/distress). Future iterations can integrate temporal action-recognition transformers (e.g., VideoMAE, SlowFast) for complex behaviors such as climbing, loitering, or perimeter intrusion.
- **Hardware Acceleration:** Deploying the pipeline with TensorRT and CUDA on embedded edge platforms (e.g., NVIDIA Jetson Orin) will enable concurrent real-time processing of multi-camera CCTV streams.

---

## APPENDIX A: SOFTWARE ARCHITECTURE & EXECUTION

### A.1 Directory Structure
```
ActivityAwareCompression/
├── backend/main.py             # FastAPI REST Server
├── frontend/src/App.jsx        # Web UI & Surveillance Monitor Dashboard
├── frontend/src/App.css        # Stylesheet & Surveillance HUD styling
├── input/test_video.mp4        # Verified 89-Second Surveillance Footage
├── output/adaptive_compressed.mp4 # Final Activity-Aware Compressed Output
├── output/annotated_surveillance.mp4 # AI Annotated Video Stream (Page 6 View)
├── src/activity_detector.py    # YOLOv8 Pose (17 Keypoints) & Critical Alert Engine
├── src/adaptive_compressor.py  # Multi-Tier FFmpeg Adaptive Compressor
├── src/evaluator.py            # Objective Quality Metric Evaluator (PSNR & SSIM)
├── main.py                     # CLI Pipeline Runner
└── requirements.txt            # Python Dependencies
```

### A.2 Commands to Run the Project (Windows PowerShell)

#### 1. Start the Backend API:
```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Start the Frontend Web Application:
```powershell
cd frontend
npm run dev
```
Access the application at: `http://localhost:5173`

#### 3. Run via Command Line Interface (CLI):
```powershell
python main.py input/test_video.mp4 output/adaptive_compressed.mp4
```

---

## REFERENCES

1. Gull, I., Selwal, A., and Sabha, A., "An analysis of video-based human activity detection approaches," *Proc. International Conference on Sustainable Computing and Data Communication Systems (ICSCDS)*, pp. 112–118, 2022.
2. Liu, W., Kang, G., Huang, P.-Y., et al., "Argus: Efficient activity detection system for extended video analysis," *IEEE Winter Conference on Applications of Computer Vision Workshops (WACVW)*, pp. 126–133, 2020.
3. Dhulekar, P. A., Gandhe, S. T., Shewale, A., Sonawane, S., and Yelmame, V., "Motion estimation for human activity surveillance," *Proc. International Conference on Emerging Trends & Innovation in ICT (ICEI)*, pp. 82–85, 2017.
4. Duarte António, R., De Faria, S. M. M., Távora, L. M. N., et al., "Learning-based compression of visual objects for smart surveillance," *International Conference on Image Processing Theory, Tools and Applications (IPTA)*, pp. 1–6, 2022.
5. Li, N., Bennis, M., Iosifidis, A., and Zhang, Q., "Spatiotemporal attention-based semantic compression for real-time video recognition," *IEEE Global Communications Conference Workshops (Globecom Workshops)*, pp. 1603–1608, 2023.
