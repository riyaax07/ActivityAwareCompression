"""
create_all_diagrams.py
Generates professional academic engineering diagrams for the Mini Project Report:
1. Figure 2.1: Use Case Diagram
2. Figure 2.2: Sequence Diagram (Surveillance Ingest & Processing)
3. Figure 3.1: 3-Tier System Architecture Diagram
4. Figure 3.2: Level-1 Data Flow Diagram (DFD)
5. Figure 3.3: UML Class Diagram
6. Figure 3.4: Activity Decision & Compression Flowchart
7. Figure 4.1: Implementation Reference HUD (Normal vs Emergency Mode - Page 6)
8. Figure 4.2: Quantitative Benchmark Charts (Storage & PSNR/SSIM)
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

OUT_DIR = "output/diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

# Set global styles
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

# =============================================================================
# 1. USE CASE DIAGRAM (Figure 2.1)
# =============================================================================
def draw_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Boundary box
    system_box = FancyBboxPatch((28, 5), 44, 90, boxstyle="round,pad=1.5",
                                ec="#102C57", fc="#F8FAFC", lw=2)
    ax.add_patch(system_box)
    ax.text(50, 91, "Activity-Aware Surveillance System", ha="center", va="center",
            fontsize=13, fontweight='bold', color="#102C57")

    # Primary Actor: Security Operator (Left)
    ax.plot([10, 10], [55, 65], color="#1E293B", lw=3)       # Body
    circle = plt.Circle((10, 68), 3, color="#1E293B", fill=False, lw=3)
    ax.add_patch(circle)                                       # Head
    ax.plot([5, 15], [60, 60], color="#1E293B", lw=3)         # Arms
    ax.plot([10, 5], [55, 47], color="#1E293B", lw=3)         # Leg L
    ax.plot([10, 15], [55, 47], color="#1E293B", lw=3)        # Leg R
    ax.text(10, 42, "Security Operator\n(Primary Actor)", ha="center", va="top",
            fontsize=10, fontweight='bold', color="#1E293B")

    # Secondary Actor: NVR Storage Archive (Right)
    rect_nvr = FancyBboxPatch((85, 48), 12, 16, boxstyle="round,pad=0.5",
                              ec="#047857", fc="#ECFDF5", lw=2)
    ax.add_patch(rect_nvr)
    ax.text(91, 56, "NVR Storage\nArchive\n(System Actor)", ha="center", va="center",
            fontsize=9, fontweight='bold', color="#065F46")

    # Use cases
    use_cases = [
        ("UC1: Upload / Ingest Surveillance Video", 82),
        ("UC2: Extract 17 Skeletal Pose Keypoints", 70),
        ("UC3: Classify Posture (Sit/Stand/Walk)", 58),
        ("UC4: Detect Critical Objects & Hazards", 46),
        ("UC5: Dynamic Multi-Tier Video Encoding", 34),
        ("UC6: Real-Time HUD Monitoring & Export", 22),
        ("UC7: PSNR & SSIM Quality Evaluation", 10),
    ]

    for text, y in use_cases:
        ellipse = patches.Ellipse((50, y), 38, 7.5, ec="#2563EB", fc="#EFF6FF", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(50, y, text, ha="center", va="center", fontsize=9.5, fontweight='bold', color="#1E3A8A")

        # Connection to Actor 1
        ax.plot([15, 31], [58, y], color="#475569", lw=1.2, linestyle="--")

        # Connection to Storage Actor for UC5 & UC6
        if y in [34, 22, 10]:
            ax.plot([69, 85], [y, 56], color="#059669", lw=1.2, linestyle="--")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_use_case.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 2. SEQUENCE DIAGRAM (Figure 2.2)
# =============================================================================
def draw_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    lifelines = [
        ("Operator", 10, "#1E293B"),
        ("React UI", 28, "#2563EB"),
        ("FastAPI Backend", 48, "#7C3AED"),
        ("YOLOv8 Analytics", 70, "#D97706"),
        ("FFmpeg Engine", 90, "#059669")
    ]

    for name, x, col in lifelines:
        box = FancyBboxPatch((x-7, 90), 14, 6, boxstyle="round,pad=0.3", ec=col, fc="#F8FAFC", lw=2)
        ax.add_patch(box)
        ax.text(x, 93, name, ha="center", va="center", fontsize=9.5, fontweight='bold', color=col)
        ax.plot([x, x], [12, 90], color=col, linestyle=":", lw=1.5)

    messages = [
        (82, 10, 28, "1. Select / Upload Surveillance Video", True),
        (75, 28, 48, "2. POST /api/upload (Job Dispatch)", True),
        (68, 48, 70, "3. Extract Frames & Run YOLOv8 Pose", True),
        (61, 70, 70, "4. Posture Analysis (Sit/Stand/Alert)", False),
        (54, 70, 48, "5. Return Activity Segments & Critical Objects", False),
        (47, 48, 90, "6. Execute Multi-Tier Compression (CRF 24/32/36)", True),
        (40, 90, 90, "7. Transcode Chunks & Concat Audio Stream", False),
        (33, 90, 48, "8. Storage Saved (%) & Optimized Output", False),
        (26, 48, 28, "9. Return Job Status & Stream URL", False),
        (19, 28, 10, "10. Render Live HUD & Download Link", False)
    ]

    for y, x1, x2, txt, is_fwd in messages:
        if x1 == x2:  # Self-call
            ax.annotate("", xy=(x1, y-3), xytext=(x1, y+3),
                        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.5", color="#D97706", lw=1.5))
            ax.text(x1 + 8, y, txt, ha="left", va="center", fontsize=8.5, color="#92400E", fontweight='bold')
        else:
            col = "#1E293B" if is_fwd else "#059669"
            ls = "-" if is_fwd else "--"
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.5, linestyle=ls))
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 2, txt, ha="center", va="bottom", fontsize=8.5, color=col, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_sequence.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 3. 3-TIER ARCHITECTURE DIAGRAM (Figure 3.1)
# =============================================================================
def draw_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tier 1: Client Presentation Tier
    tier1 = FancyBboxPatch((5, 68), 90, 26, boxstyle="round,pad=0.8", ec="#2563EB", fc="#EFF6FF", lw=2)
    ax.add_patch(tier1)
    ax.text(8, 91, "TIER 1: PRESENTATION LAYER (React 19 + Vite SPA)", fontsize=11, fontweight='bold', color="#1E40AF")
    
    t1_boxes = [
        ("Video Upload / Dropzone\n& Format Validation", 18, 77),
        ("AI Surveillance HUD Monitor\n(Page 6 Live Playback)", 50, 77),
        ("Comparative Analytics\n(PSNR/SSIM & Export)", 82, 77)
    ]
    for txt, cx, cy in t1_boxes:
        b = FancyBboxPatch((cx-13, cy-6), 26, 13, boxstyle="round,pad=0.4", ec="#3B82F6", fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=9, color="#1E3A8A", fontweight='bold')

    # Tier 2: Application Middleware
    tier2 = FancyBboxPatch((5, 36), 90, 24, boxstyle="round,pad=0.8", ec="#7C3AED", fc="#F5F3FF", lw=2)
    ax.add_patch(tier2)
    ax.text(8, 57, "TIER 2: APPLICATION MIDDLEWARE (FastAPI Server + REST Engine)", fontsize=11, fontweight='bold', color="#5B21B6")

    t2_boxes = [
        ("REST API Routes\n(/upload, /compress)", 20, 45),
        ("Asynchronous Job Dispatcher\n(ThreadPoolExecutor)", 50, 45),
        ("Stream Controller\n(H.264 Range Requests)", 80, 45)
    ]
    for txt, cx, cy in t2_boxes:
        b = FancyBboxPatch((cx-13, cy-5.5), 26, 11, boxstyle="round,pad=0.4", ec="#8B5CF6", fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=9, color="#4C1D95", fontweight='bold')

    # Tier 3: Analytics & Compression
    tier3 = FancyBboxPatch((5, 4), 90, 24, boxstyle="round,pad=0.8", ec="#059669", fc="#ECFDF5", lw=2)
    ax.add_patch(tier3)
    ax.text(8, 25, "TIER 3: CORE ANALYTICS & ADAPTIVE COMPRESSION ENGINE", fontsize=11, fontweight='bold', color="#065F46")

    t3_boxes = [
        ("YOLOv8-Pose (17 Landmarks)\n& Biomechanical Angles", 20, 13),
        ("Critical Hazard Detector\n(Emergency Mode Trigger)", 50, 13),
        ("FFmpeg Multi-Tier Encoder\n(CRF 24/32/36 + Concat)", 80, 13)
    ]
    for txt, cx, cy in t3_boxes:
        b = FancyBboxPatch((cx-13, cy-5.5), 26, 11, boxstyle="round,pad=0.4", ec="#10B981", fc="#FFFFFF", lw=1.5)
        ax.add_patch(b)
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=9, color="#064E3B", fontweight='bold')

    # Inter-tier communication arrows
    ax.annotate("", xy=(30, 68), xytext=(30, 60), arrowprops=dict(arrowstyle="<->", color="#1E293B", lw=2))
    ax.text(32, 64, "HTTP / REST API & JSON Payloads", fontsize=8.5, color="#1E293B", fontweight='bold')

    ax.annotate("", xy=(70, 36), xytext=(70, 28), arrowprops=dict(arrowstyle="<->", color="#1E293B", lw=2))
    ax.text(72, 32, "Native OpenCV / PyTorch / FFmpeg Calls", fontsize=8.5, color="#1E293B", fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_architecture.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 4. LEVEL-1 DATA FLOW DIAGRAM (DFD) (Figure 3.2)
# =============================================================================
def draw_dfd_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Entities (Rectangles)
    ent_op = FancyBboxPatch((4, 70), 16, 12, boxstyle="square,pad=0.5", ec="#1E293B", fc="#F1F5F9", lw=2)
    ax.add_patch(ent_op)
    ax.text(12, 76, "Security\nOperator", ha="center", va="center", fontsize=10, fontweight='bold')

    ent_cam = FancyBboxPatch((4, 25), 16, 12, boxstyle="square,pad=0.5", ec="#1E293B", fc="#F1F5F9", lw=2)
    ax.add_patch(ent_cam)
    ax.text(12, 31, "CCTV Camera /\nVideo Feed", ha="center", va="center", fontsize=10, fontweight='bold')

    # Processes (Circles/Rounded)
    processes = [
        ("1.0\nIngest &\nDecode", 35, 76),
        ("2.0\nPose & Landmark\nExtraction", 60, 76),
        ("3.0\nImportance &\nMode Assess", 85, 76),
        ("4.0\nMulti-Tier\nCompression", 85, 31),
        ("5.0\nStream Concat &\nAudio Mux", 60, 31),
        ("6.0\nPSNR / SSIM\nEvaluation", 35, 31),
    ]
    for lbl, px, py in processes:
        p_box = FancyBboxPatch((px-9, py-7), 18, 14, boxstyle="circle,pad=0.3", ec="#2563EB", fc="#EFF6FF", lw=2)
        ax.add_patch(p_box)
        ax.text(px, py, lbl, ha="center", va="center", fontsize=8.5, fontweight='bold', color="#1E3A8A")

    # Data Store (Open ended rectangle)
    ax.plot([45, 75], [54, 54], color="#047857", lw=2)
    ax.plot([45, 75], [46, 46], color="#047857", lw=2)
    ax.plot([45, 45], [46, 54], color="#047857", lw=2)
    ax.text(60, 50, "D1: Activity Segments & Metadata", ha="center", va="center",
            fontsize=9, fontweight='bold', color="#065F46")

    # Data Flow Arrows
    flows = [
        (20, 76, 26, 76, "Raw Video"),
        (44, 76, 51, 76, "Decoded Frames"),
        (69, 76, 76, 76, "17 Keypoints"),
        (85, 69, 85, 38, "Modes: Emerg/Norm/Idle"),
        (76, 31, 69, 31, "Encoded Chunks"),
        (51, 31, 44, 31, "Final MP4 Video"),
        (26, 31, 20, 70, "Analytics & Playback"),
    ]
    for x1, y1, x2, y2, desc in flows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color="#334155", lw=1.5))
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1.5, desc, ha="center", va="bottom", fontsize=7.5, color="#0F172A", fontweight='bold')

    # Store connections
    ax.annotate("", xy=(60, 54), xytext=(80, 70), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, linestyle="--"))
    ax.annotate("", xy=(80, 38), xytext=(65, 46), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, linestyle="--"))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_dfd.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 5. UML CLASS DIAGRAM (Figure 3.3)
# =============================================================================
def draw_class_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    classes = [
        ("ActivityDetector", 20, 75, 32, 22, [
            "- pose_model: YOLO",
            "- det_model: YOLO",
            "+ classify_activity(kpts, bbox): str",
            "+ detect_critical_objects(frame): list",
            "+ process_frame(frame, idx, fps): tuple"
        ]),
        ("AdaptiveCompressor", 75, 75, 34, 22, [
            "- preset: str = 'faster'",
            "- crf_map: dict",
            "+ get_stream_info(path): dict",
            "+ compress_adaptive(input, output): dict",
            "+ assemble_stream(segments, audio): bool"
        ]),
        ("VideoEvaluator", 20, 25, 32, 20, [
            "- stride: int = 15",
            "- resolution: tuple",
            "+ evaluate_videos(orig, comp): dict",
            "+ compute_psnr(f1, f2): float",
            "+ compute_ssim(f1, f2): float"
        ]),
        ("SurveillanceJobManager", 75, 25, 34, 20, [
            "- jobs: Dict[str, dict]",
            "- executor: ThreadPoolExecutor",
            "+ create_job(path): str",
            "+ run_pipeline(job_id): void",
            "+ stream_video(job_id, kind): File"
        ])
    ]

    for name, cx, cy, w, h, members in classes:
        box = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="square,pad=0", ec="#1E293B", fc="#FFFFFF", lw=1.8)
        ax.add_patch(box)
        # Header banner
        header = FancyBboxPatch((cx-w/2, cy+h/2-4.5), w, 4.5, boxstyle="square,pad=0", ec="#1E293B", fc="#102C57", lw=1.8)
        ax.add_patch(header)
        ax.text(cx, cy+h/2-2.2, name, ha="center", va="center", fontsize=9.5, fontweight='bold', color="#FFFFFF")

        # Members text
        y_text = cy + h/2 - 7.5
        for m in members:
            ax.text(cx - w/2 + 1.5, y_text, m, ha="left", va="center", fontsize=7.5, family="monospace", color="#0F172A")
            y_text -= 3.2

    # Associations
    ax.annotate("", xy=(58, 75), xytext=(36, 75), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2))
    ax.text(47, 77, "generates segments", ha="center", fontsize=8, color="#1E40AF", fontweight='bold')

    ax.annotate("", xy=(75, 35), xytext=(75, 64), arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2))
    ax.text(77, 50, "orchestrates", ha="left", fontsize=8, color="#5B21B6", fontweight='bold')

    ax.annotate("", xy=(36, 25), xytext=(58, 25), arrowprops=dict(arrowstyle="->", color="#059669", lw=2))
    ax.text(47, 27, "benchmarks quality", ha="center", fontsize=8, color="#065F46", fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_class_diagram.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 6. ACTIVITY DECISION & COMPRESSION FLOWCHART (Figure 3.4)
# =============================================================================
def draw_activity_flowchart():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_box(cx, cy, w, h, text, fc="#EFF6FF", ec="#2563EB", is_diamond=False):
        if is_diamond:
            d = patches.Polygon([[cx, cy+h/2], [cx+w/2, cy], [cx, cy-h/2], [cx-w/2, cy]],
                                closed=True, ec=ec, fc=fc, lw=2)
            ax.add_patch(d)
        else:
            b = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.5", ec=ec, fc=fc, lw=2)
            ax.add_patch(b)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=8.5, fontweight='bold', color="#0F172A")

    # Start
    draw_box(50, 95, 24, 6, "Start Surveillance Ingest", fc="#E2E8F0", ec="#475569")
    draw_box(50, 84, 28, 6, "Extract Frame & Run YOLOv8")
    
    # Decision 1: Person Detected?
    draw_box(50, 71, 30, 8, "Human Subject\nDetected?", fc="#FEF3C7", ec="#D97706", is_diamond=True)

    # Idle Branch (No)
    draw_box(18, 71, 24, 7, "IDLE MODE\n(5 FPS | CRF 36)", fc="#E0F2FE", ec="#0284C7")

    # Posture Analysis (Yes)
    draw_box(50, 56, 32, 6, "Extract 17 Keypoints & Joint Angles")

    # Decision 2: Critical Event / Hazard?
    draw_box(50, 43, 30, 8, "Critical Alert / Hazard\nor Fall Detected?", fc="#FEE2E2", ec="#DC2626", is_diamond=True)

    # Emergency Mode (Yes)
    draw_box(82, 43, 26, 7, "EMERGENCY MODE\n(30 FPS | CRF 24)", fc="#FEE2E2", ec="#B91C1C")

    # Normal Human Mode (No)
    draw_box(50, 30, 26, 7, "NORMAL HUMAN MODE\n(10-15 FPS | CRF 32)", fc="#FEF3C7", ec="#B45309")

    # Multi-tier FFmpeg
    draw_box(50, 17, 36, 6, "Multi-Tier FFmpeg Segment Encoding")
    draw_box(50, 7, 32, 6, "Lossless Concatenation & Audio Mux", fc="#D1FAE5", ec="#059669")

    # Connectors
    arrows = [
        (50, 92, 50, 87),
        (50, 81, 50, 75),
        (35, 71, 30, 71),  # No to Idle
        (50, 67, 50, 59),  # Yes to Keypoints
        (50, 53, 50, 47),
        (65, 43, 69, 43),  # Yes to Emergency
        (50, 39, 50, 33.5),# No to Normal
        (50, 26.5, 50, 20),
        (50, 14, 50, 10),
        (18, 67.5, 18, 17), # Idle down
        (18, 17, 32, 17),
        (82, 39.5, 82, 17), # Emergency down
        (82, 17, 68, 17)
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.6))

    ax.text(32, 72.5, "No", fontsize=8, fontweight='bold', color="#DC2626")
    ax.text(51.5, 63, "Yes", fontsize=8, fontweight='bold', color="#059669")
    ax.text(66, 44.5, "Yes", fontsize=8, fontweight='bold', color="#DC2626")
    ax.text(51.5, 36, "No", fontsize=8, fontweight='bold', color="#059669")

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_activity_flow.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 7. IMPLEMENTATION REFERENCE HUD (Figure 4.1)
# =============================================================================
def draw_hud_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

    # Frame 1: Normal Human Mode (Left)
    f1 = np.full((360, 640, 3), (35, 38, 42), dtype=np.uint8)
    # Background room features
    cv2.rectangle(f1, (0, 260), (640, 360), (28, 30, 34), -1)
    cv2.rectangle(f1, (480, 50), (620, 200), (45, 48, 55), 2)
    # HUD Banner
    cv2.rectangle(f1, (0, 0), (640, 48), (20, 20, 24), -1)
    cv2.circle(f1, (20, 22), 6, (0, 215, 255), -1) # Yellow dot
    cv2.putText(f1, "MODE: NORMAL HUMAN (10 FPS) | ACTIVITY: SITTING", (35, 26),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)
    cv2.putText(f1, "FPS: 29.97 | Encoded: 1531/2670 frames | Storage Saved: 38.4%", (35, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

    # Human Person Box (Yellow)
    cv2.rectangle(f1, (160, 80), (460, 340), (0, 230, 255), 2)
    cv2.putText(f1, "PERSON: SITTING", (160, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 230, 255), 2)

    # Skeleton points (Green bones, Red joints)
    pts = [(310, 110), (310, 160), (250, 170), (370, 170), (220, 240), (400, 240),
           (280, 250), (340, 250), (260, 320), (360, 320)]
    bones = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 5), (1, 6), (1, 7), (6, 8), (7, 9)]
    for i1, i2 in bones:
        cv2.line(f1, pts[i1], pts[i2], (0, 255, 0), 2)
    for p in pts:
        cv2.circle(f1, p, 4, (0, 0, 255), -1)

    ax1.imshow(cv2.cvtColor(f1, cv2.COLOR_BGR2RGB))
    ax1.set_title("Mode: Normal Human (Sitting Posture - 10 FPS)", fontsize=11, fontweight='bold', pad=10)
    ax1.axis('off')

    # Frame 2: Emergency Mode (Right)
    f2 = f1.copy()
    # Update HUD Banner to Emergency
    cv2.rectangle(f2, (0, 0), (640, 48), (20, 20, 24), -1)
    cv2.circle(f2, (20, 22), 6, (0, 0, 255), -1) # Red dot
    cv2.putText(f2, "MODE: EMERGENCY (30 FPS) | ACTIVITY: CRITICAL ALERT", (35, 26),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)
    cv2.putText(f2, "FPS: 29.97 | Encoded: 1840/2670 frames | Storage Saved: 34.2%", (35, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

    # Red Critical Hazard Box
    cv2.rectangle(f2, (380, 210), (445, 280), (0, 0, 255), 2)
    cv2.putText(f2, "[!] CRITICAL ALERT", (360, 202), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    ax2.imshow(cv2.cvtColor(f2, cv2.COLOR_BGR2RGB))
    ax2.set_title("Mode: Emergency (Hazard Alert - 30 FPS Full Quality)", fontsize=11, fontweight='bold', pad=10)
    ax2.axis('off')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_hud_comparison.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

# =============================================================================
# 8. PERFORMANCE CHARTS (Figure 4.2)
# =============================================================================
def draw_performance_charts():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)

    # Subplot 1: File Size & Storage Savings
    categories = ['Original\nSurveillance', 'Uniform Baseline\n(Fixed CRF 32)', 'Activity-Aware\nAdaptive (Ours)']
    sizes_mb = [60.45, 30.07, 37.21]
    colors = ['#64748B', '#0284C7', '#059669']

    bars = ax1.bar(categories, sizes_mb, color=colors, width=0.55, edgecolor='#1E293B', lw=1.2)
    ax1.set_ylabel("Storage File Size (MB)", fontsize=10, fontweight='bold')
    ax1.set_title("Surveillance File Size Comparison", fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 75)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    for bar, val in zip(bars, sizes_mb):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 1.5, f"{val:.2f} MB",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    # Subplot 2: Quality Comparison (PSNR & SSIM)
    x = np.arange(2)
    width = 0.35
    psnr_vals = [33.41, 34.82]   # Baseline vs Ours
    ssim_vals = [0.9247, 0.9385] # Baseline vs Ours

    ax2_twin = ax2.twinx()
    b1 = ax2.bar(x - width/2, psnr_vals, width, label='Avg PSNR (dB)', color='#2563EB', edgecolor='#1E293B')
    b2 = ax2_twin.bar(x + width/2, ssim_vals, width, label='Avg SSIM', color='#F59E0B', edgecolor='#1E293B')

    ax2.set_xticks(x)
    ax2.set_xticklabels(['Uniform Baseline\n(CRF 32)', 'Activity-Aware\nAdaptive (Ours)'], fontweight='bold')
    ax2.set_ylabel("PSNR (dB)", color='#2563EB', fontsize=10, fontweight='bold')
    ax2_twin.set_ylabel("SSIM Score", color='#D97706', fontsize=10, fontweight='bold')
    ax2.set_title("Objective Video Quality in Active Zones", fontsize=11, fontweight='bold')
    ax2.set_ylim(28, 38)
    ax2_twin.set_ylim(0.85, 1.0)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    for bar, val in zip(b1, psnr_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.3, f"{val:.2f} dB", ha='center', fontsize=9, fontweight='bold', color='#1E40AF')
    for bar, val in zip(b2, ssim_vals):
        ax2_twin.text(bar.get_x() + bar.get_width()/2, val + 0.005, f"{val:.4f}", ha='center', fontsize=9, fontweight='bold', color='#B45309')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "figure_performance_charts.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    draw_use_case_diagram()
    draw_sequence_diagram()
    draw_architecture_diagram()
    draw_dfd_diagram()
    draw_class_diagram()
    draw_activity_flowchart()
    draw_hud_comparison()
    draw_performance_charts()
    print("All diagrams generated successfully in output/diagrams/!")
