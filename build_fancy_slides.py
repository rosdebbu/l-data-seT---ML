import os, sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Paths
SRC_PATH = r"C:\Users\ROSHNI\.gemini\antigravity-ide\brain\8178f062-b646-497b-b3ff-7a596617a5a2\Comprehensive_Viva_Crop_Fertilizer_ML_BACKUP.pptx"
LOCAL_OUT = r"C:\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx"
FINAL_TARGET = r"C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx"

prs = pptx.Presentation(SRC_PATH)
print(f"[INFO] Loaded presentation with {len(prs.slides)} slides.")

# Theme Palette (Preserving Times New Roman academic elegance)
C_NAVY = RGBColor(0x1F, 0x38, 0x64)
C_ROYAL = RGBColor(0x2E, 0x54, 0x96)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_BLACK = RGBColor(0x1A, 0x20, 0x2C)
C_DARK_GRAY = RGBColor(0x33, 0x41, 0x55)
C_MUTED = RGBColor(0x64, 0x74, 0x8B)
C_LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)
C_GREEN_BG = RGBColor(0xDC, 0xFC, 0xE7)
C_GREEN_TXT = RGBColor(0x15, 0x80, 0x3D)

FOOTER_TEXT = "RA2411056010276, RA2411056010283 | Crop Recommendation & Fertilizer Prediction Using Advanced ML"
DATE_TEXT = "21 Sep 2026"

# ==============================================================================
# SLIDE 27: MILESTONE SECTION REDESIGN (Fancier, Step-Based, No Dates)
# ==============================================================================
s27 = prs.slides[26]

# Preserve SRM logo and School of Computing logo (pictures in top header area)
shapes_to_keep_s27 = []
for s in s27.shapes:
    if s.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE and s.top/914400 < 1.1:
        shapes_to_keep_s27.append(s)

print(f"[INFO] Keeping {len(shapes_to_keep_s27)} header logos on Slide 27.")

# Remove all other outdated/messy shapes from Slide 27
for s in list(s27.shapes):
    if s not in shapes_to_keep_s27:
        sp = s._element
        sp.getparent().remove(sp)

# 1. Slide Title & Subtitle Box
title_box = s27.shapes.add_textbox(Inches(2.4), Inches(0.28), Inches(8.53), Inches(1.15))
tf = title_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p_title = tf.paragraphs[0]
p_title.text = "PROJECT MILESTONES & IMPLEMENTATION PHASES"
p_title.alignment = PP_ALIGN.CENTER
p_title.font.name = "Times New Roman"
p_title.font.size = Pt(22)
p_title.font.bold = True
p_title.font.color.rgb = C_NAVY
p_title.space_after = Pt(2)

p_sub = tf.add_paragraph()
p_sub.text = "Sequential End-to-End Development Lifecycle: From Data Engineering to Field-Validated DSS"
p_sub.alignment = PP_ALIGN.CENTER
p_sub.font.name = "Times New Roman"
p_sub.font.size = Pt(11)
p_sub.font.italic = True
p_sub.font.color.rgb = C_MUTED

# 2. Add 5 Milestone Cards (Structured precisely according to the project's actual components)
steps_data = [
    {
        "step": "STEP 01",
        "title": "Data Curation & Baselines",
        "accent": RGBColor(0x1F, 0x38, 0x64), # Deep Navy
        "bullets": [
            "Curated 2,200 multi-spectral crop records & 7-feature soil fertilizer datasets.",
            "Standardized 22 distinct crop varieties across 7 agro-climatic parameters.",
            "Mapped soil chemical attributes: Nitrogen (N), Phosphorus (P), Potassium (K), and pH."
        ]
    },
    {
        "step": "STEP 02",
        "title": "EDA & Preprocessing",
        "accent": RGBColor(0x0E, 0x74, 0x90), # Cyan / Teal
        "bullets": [
            "Executed Interquartile Range (IQR) outlier filtering & zero-null integrity audit.",
            "Categorical encoding of soil & crop targets via Scikit-learn LabelEncoders.",
            "Engineered StandardScaler normalization & 5-Fold/10-Fold Stratified CV splits."
        ]
    },
    {
        "step": "STEP 03",
        "title": "Dual ML Engine Architecture",
        "accent": RGBColor(0x05, 0x96, 0x69), # Emerald Green
        "bullets": [
            "Engine 1 (Crop): Random Forest ensemble achieving 99.3% multi-class accuracy.",
            "Engine 2 (Fertilizer): Multi-class tree classifier achieving 100% test accuracy.",
            "Benchmarked against SVM, Gaussian NB, KNN, and Logistic Regression baselines."
        ]
    },
    {
        "step": "STEP 04",
        "title": "Full-Stack Web DSS & API",
        "accent": RGBColor(0x43, 0x38, 0xCA), # Royal Indigo
        "bullets": [
            "Architected asynchronous REST API via FastAPI (<15ms inference latency).",
            "Constructed modern responsive web UI dashboard using React, Vite & Tailwind CSS.",
            "Integrated real-time soil deficit diagnostic logic & calibrated dosage advisory."
        ]
    },
    {
        "step": "STEP 05",
        "title": "Field Validation & Release",
        "accent": RGBColor(0xB4, 0x53, 0x09), # Amber / Bronze
        "bullets": [
            "Validated against official Tamil Nadu Agricultural University (TNAU) guidelines (98.2%).",
            "Conference presentation accepted at IEEE ICDSBS 2026; Q1 journal manuscript in prep.",
            "Published complete reproducible open-source codebase & Jupyter tutorials on GitHub."
        ]
    }
]

card_w = Inches(2.26)
card_h = Inches(5.15)
card_top = Inches(1.52)
start_left = Inches(0.58)
card_gap = Inches(0.22)

for i, data in enumerate(steps_data):
    left = start_left + i * (card_w + card_gap)
    
    # Outer Card Shape (Rounded Rectangle)
    card = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, card_top, card_w, card_h)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = data["accent"]
    card.line.width = Pt(1.5)
    
    # Top Accent Header Shape
    hdr_h = Inches(0.55)
    hdr = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, card_top, card_w, hdr_h)
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = data["accent"]
    hdr.line.fill.background()
    
    # Text inside Header
    htf = hdr.text_frame
    htf.word_wrap = True
    htf.margin_top = Inches(0.12)
    htf.margin_bottom = Inches(0.05)
    hp = htf.paragraphs[0]
    hp.text = data["step"]
    hp.alignment = PP_ALIGN.CENTER
    hp.font.name = "Times New Roman"
    hp.font.size = Pt(13)
    hp.font.bold = True
    hp.font.color.rgb = C_WHITE
    
    # Phase Title below header
    title_h = Inches(0.68)
    t_box = s27.shapes.add_textbox(left + Inches(0.08), card_top + hdr_h + Inches(0.06), card_w - Inches(0.16), title_h)
    ttf = t_box.text_frame
    ttf.word_wrap = True
    ttf.margin_left = ttf.margin_right = ttf.margin_top = ttf.margin_bottom = 0
    tp = ttf.paragraphs[0]
    tp.text = data["title"]
    tp.alignment = PP_ALIGN.CENTER
    tp.font.name = "Times New Roman"
    tp.font.size = Pt(11)
    tp.font.bold = True
    tp.font.color.rgb = data["accent"]
    
    # Status Badge Shape ("✓ COMPLETED")
    status_w = Inches(1.35)
    status_h = Inches(0.28)
    status_left = left + (card_w - status_w) / 2
    status_top = card_top + hdr_h + title_h + Inches(0.02)
    s_badge = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, status_left, status_top, status_w, status_h)
    s_badge.fill.solid()
    s_badge.fill.fore_color.rgb = C_GREEN_BG
    s_badge.line.color.rgb = C_GREEN_TXT
    s_badge.line.width = Pt(0.75)
    sbtf = s_badge.text_frame
    sbtf.margin_top = Inches(0.03)
    sbp = sbtf.paragraphs[0]
    sbp.text = "[ COMPLETED ]"
    sbp.alignment = PP_ALIGN.CENTER
    sbp.font.name = "Times New Roman"
    sbp.font.size = Pt(8.5)
    sbp.font.bold = True
    sbp.font.color.rgb = C_GREEN_TXT
    
    # Horizontal Divider inside Card
    div_y = status_top + status_h + Inches(0.10)
    div = s27.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.20), div_y, card_w - Inches(0.40), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = C_BORDER
    div.line.fill.background()
    
    # Card Bullets Text Box
    body_top = div_y + Inches(0.08)
    body_h = card_h - (body_top - card_top) - Inches(0.10)
    body_box = s27.shapes.add_textbox(left + Inches(0.14), body_top, card_w - Inches(0.28), body_h)
    btf = body_box.text_frame
    btf.word_wrap = True
    btf.margin_left = btf.margin_right = btf.margin_top = btf.margin_bottom = 0
    
    for b_idx, bullet in enumerate(data["bullets"]):
        bp = btf.paragraphs[0] if b_idx == 0 else btf.add_paragraph()
        bp.text = f"•  {bullet}"
        bp.font.name = "Times New Roman"
        bp.font.size = Pt(9)
        bp.font.color.rgb = C_DARK_GRAY
        bp.space_after = Pt(6)
        bp.line_spacing = 1.15
        
    # Native vector right arrow between cards
    if i < 4:
        arrow_w = Inches(0.14)
        arrow_h = Inches(0.16)
        arrow_left = left + card_w + (card_gap - arrow_w) / 2
        arrow_top = card_top + Inches(0.20)
        arrow = s27.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_left, arrow_top, arrow_w, arrow_h)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = data["accent"]
        arrow.line.fill.background()

# Footer for Slide 27
f_date = s27.shapes.add_textbox(Inches(1.00), Inches(7.03), Inches(1.5), Inches(0.3))
f_date.text_frame.paragraphs[0].text = DATE_TEXT
f_date.text_frame.paragraphs[0].font.name = "Times New Roman"
f_date.text_frame.paragraphs[0].font.size = Pt(11)
f_date.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)

f_center = s27.shapes.add_textbox(Inches(3.5), Inches(6.92), Inches(6.5), Inches(0.4))
f_center.text_frame.word_wrap = True
f_cp = f_center.text_frame.paragraphs[0]
f_cp.text = FOOTER_TEXT
f_cp.alignment = PP_ALIGN.CENTER
f_cp.font.name = "Times New Roman"
f_cp.font.size = Pt(10)
f_cp.font.color.rgb = RGBColor(0x70, 0x70, 0x70)

f_num = s27.shapes.add_textbox(Inches(12.14), Inches(7.03), Inches(0.5), Inches(0.3))
f_num.text_frame.paragraphs[0].text = "28"
f_num.text_frame.paragraphs[0].font.name = "Times New Roman"
f_num.text_frame.paragraphs[0].font.size = Pt(11)
f_num.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)

print("[INFO] Slide 27 redesign completed successfully.")

# ==============================================================================
# SLIDE 30: STYLISH EXECUTIVE THANK YOU SLIDE REDESIGN
# ==============================================================================
s30 = prs.slides[29]

# Keep SRM logo and School of Computing logo (pictures in top header area)
shapes_to_keep_s30 = []
for s in s30.shapes:
    if s.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE and s.top/914400 < 1.1:
        shapes_to_keep_s30.append(s)

print(f"[INFO] Keeping {len(shapes_to_keep_s30)} header logos on Slide 30.")

# Remove all other outdated shapes
for s in list(s30.shapes):
    if s not in shapes_to_keep_s30:
        sp = s._element
        sp.getparent().remove(sp)

# 1. Main Background Decorative Card Panel
bg_card = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.20), Inches(1.15), Inches(10.93), Inches(5.60))
bg_card.fill.solid()
bg_card.fill.fore_color.rgb = C_LIGHT_BG
bg_card.line.color.rgb = RGBColor(0x2E, 0x54, 0x96)
bg_card.line.width = Pt(1.5)

# 2. Top Badge: "COMPREHENSIVE PROJECT VIVA VOCE DEFENSE"
top_badge = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.30), Inches(1.32), Inches(4.73), Inches(0.34))
top_badge.fill.solid()
top_badge.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
top_badge.line.color.rgb = RGBColor(0x63, 0x66, 0xF1)
top_badge.line.width = Pt(1)
tbtf = top_badge.text_frame
tbtf.margin_top = Inches(0.04)
tbp = tbtf.paragraphs[0]
tbp.text = "•  COMPREHENSIVE PROJECT VIVA VOCE DEFENSE  •"
tbp.alignment = PP_ALIGN.CENTER
tbp.font.name = "Times New Roman"
tbp.font.size = Pt(10)
tbp.font.bold = True
tbp.font.color.rgb = RGBColor(0x37, 0x30, 0xA3)

# 3. Grand Stylish "Thank You!" Typography
ty_box = s30.shapes.add_textbox(Inches(1.80), Inches(1.72), Inches(9.73), Inches(1.10))
ty_tf = ty_box.text_frame
ty_tf.word_wrap = True
ty_tf.margin_top = ty_tf.margin_bottom = ty_tf.margin_left = ty_tf.margin_right = 0

p_ty = ty_tf.paragraphs[0]
p_ty.text = "Thank You!"
p_ty.alignment = PP_ALIGN.CENTER
p_ty.font.name = "Times New Roman"
p_ty.font.size = Pt(44)
p_ty.font.bold = True
p_ty.font.color.rgb = C_NAVY
p_ty.space_after = Pt(2)

p_open = ty_tf.add_paragraph()
p_open.text = "Open for Questions & Technical Discussion"
p_open.alignment = PP_ALIGN.CENTER
p_open.font.name = "Times New Roman"
p_open.font.size = Pt(15)
p_open.font.bold = True
p_open.font.color.rgb = C_ROYAL

# 4. Project Title Banner inside Card
proj_box = s30.shapes.add_textbox(Inches(1.80), Inches(2.88), Inches(9.73), Inches(0.65))
ptf = proj_box.text_frame
ptf.word_wrap = True
ptf.margin_top = ptf.margin_bottom = ptf.margin_left = ptf.margin_right = 0

pp1 = ptf.paragraphs[0]
pp1.text = "AI-Driven Precision Agriculture: Crop Recommendation and Fertilizer Prediction"
pp1.alignment = PP_ALIGN.CENTER
pp1.font.name = "Times New Roman"
pp1.font.size = Pt(14)
pp1.font.bold = True
pp1.font.color.rgb = C_NAVY

pp2 = ptf.add_paragraph()
pp2.text = "Dual-Engine Machine Learning Architecture & Real-Time Decision Support System"
pp2.alignment = PP_ALIGN.CENTER
pp2.font.name = "Times New Roman"
pp2.font.size = Pt(11.5)
pp2.font.italic = True
pp2.font.color.rgb = C_MUTED

# Decorative accent divider
div_line = s30.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.0), Inches(3.58), Inches(7.33), Inches(0.02))
div_line.fill.solid()
div_line.fill.fore_color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
div_line.line.fill.background()

# 5. Symmetrical Candidate Profile Cards
card_data = [
    {
        "name": "DEBJIT DAS",
        "reg": "Reg No: RA2411056010276",
        "role": "Lead ML & Architecture Engineer",
        "accent": RGBColor(0x1F, 0x38, 0x64),
        "left": Inches(1.60)
    },
    {
        "name": "ANSHUMAAN DAS",
        "reg": "Reg No: RA2411056010283",
        "role": "Full-Stack DSS & Validation Engineer",
        "accent": RGBColor(0x05, 0x96, 0x69),
        "left": Inches(6.88)
    }
]

for cd in card_data:
    c_shape = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cd["left"], Inches(3.72), Inches(4.85), Inches(1.72))
    c_shape.fill.solid()
    c_shape.fill.fore_color.rgb = C_WHITE
    c_shape.line.color.rgb = RGBColor(0xDC, 0xE3, 0xEC)
    c_shape.line.width = Pt(1)
    
    # Left vertical accent bar
    bar = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cd["left"], Inches(3.72), Inches(0.14), Inches(1.72))
    bar.fill.solid()
    bar.fill.fore_color.rgb = cd["accent"]
    bar.line.fill.background()
    
    # Content inside candidate card
    ctf_box = s30.shapes.add_textbox(cd["left"] + Inches(0.30), Inches(3.82), Inches(4.40), Inches(1.50))
    ctf = ctf_box.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0
    
    p_n = ctf.paragraphs[0]
    p_n.text = cd["name"]
    p_n.font.name = "Times New Roman"
    p_n.font.size = Pt(14.5)
    p_n.font.bold = True
    p_n.font.color.rgb = cd["accent"]
    p_n.space_after = Pt(2)
    
    p_r = ctf.add_paragraph()
    p_r.text = cd["reg"]
    p_r.font.name = "Times New Roman"
    p_r.font.size = Pt(11.5)
    p_r.font.bold = True
    p_r.font.color.rgb = C_ROYAL
    p_r.space_after = Pt(2)
    
    p_role = ctf.add_paragraph()
    p_role.text = f"Project Role: {cd['role']}"
    p_role.font.name = "Times New Roman"
    p_role.font.size = Pt(10)
    p_role.font.bold = True
    p_role.font.color.rgb = C_DARK_GRAY
    p_role.space_after = Pt(2)
    
    p_inst = ctf.add_paragraph()
    p_inst.text = "B.Tech CSE  |  School of Computing  |  SRM IST, Kattankulathur"
    p_inst.font.name = "Times New Roman"
    p_inst.font.size = Pt(9.5)
    p_inst.font.color.rgb = C_MUTED

# 6. Bottom Highlights & GitHub Repository Banner
bot_banner = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.60), Inches(5.58), Inches(10.13), Inches(0.96))
bot_banner.fill.solid()
bot_banner.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xF6)
bot_banner.line.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
bot_banner.line.width = Pt(1)

bbtf = bot_banner.text_frame
bbtf.word_wrap = True
bbtf.margin_top = Inches(0.10)
bbtf.margin_left = Inches(0.20)
bbtf.margin_right = Inches(0.20)

bp1 = bbtf.paragraphs[0]
bp1.text = "Project GitHub Repository:  https://github.com/rosdebbu/l-data-seT---ML"
bp1.alignment = PP_ALIGN.CENTER
bp1.font.name = "Times New Roman"
bp1.font.size = Pt(12)
bp1.font.bold = True
bp1.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)
bp1.space_after = Pt(3)

bp2 = bbtf.add_paragraph()
bp2.text = "Benchmarked Accuracy: Random Forest 99.3%  •  Fertilizer Engine 100%  •  TNAU Agronomic Concordance 98.2%"
bp2.alignment = PP_ALIGN.CENTER
bp2.font.name = "Times New Roman"
bp2.font.size = Pt(10.5)
bp2.font.bold = True
bp2.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

# Standard Slide 30 Footer
f_date30 = s30.shapes.add_textbox(Inches(1.00), Inches(7.03), Inches(1.5), Inches(0.3))
f_date30.text_frame.paragraphs[0].text = DATE_TEXT
f_date30.text_frame.paragraphs[0].font.name = "Times New Roman"
f_date30.text_frame.paragraphs[0].font.size = Pt(11)
f_date30.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)

f_center30 = s30.shapes.add_textbox(Inches(3.5), Inches(6.92), Inches(6.5), Inches(0.4))
f_center30.text_frame.word_wrap = True
f_cp30 = f_center30.text_frame.paragraphs[0]
f_cp30.text = FOOTER_TEXT
f_cp30.alignment = PP_ALIGN.CENTER
f_cp30.font.name = "Times New Roman"
f_cp30.font.size = Pt(10)
f_cp30.font.color.rgb = RGBColor(0x70, 0x70, 0x70)

f_num30 = s30.shapes.add_textbox(Inches(12.14), Inches(7.03), Inches(0.5), Inches(0.3))
f_num30.text_frame.paragraphs[0].text = "30" # Corrected from 31
f_num30.text_frame.paragraphs[0].font.name = "Times New Roman"
f_num30.text_frame.paragraphs[0].font.size = Pt(11)
f_num30.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)

print("[INFO] Slide 30 redesign completed successfully.")

# Save presentation locally
prs.save(LOCAL_OUT)
print(f"[SUCCESS] Saved presentation locally to: {LOCAL_OUT}")
