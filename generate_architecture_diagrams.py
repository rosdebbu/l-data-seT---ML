import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = r"C:\GitHub\l-data-seT---ML"
DIAG_DIR = os.path.join(BASE_DIR, "diagrams")
os.makedirs(DIAG_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Diagram 1: Objective 1 Architecture (Data Preprocessing & Feature Pipeline)
# ----------------------------------------------------------------------
def create_objective_1_diagram():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Title
    ax.text(50, 96, "Objective 1: Agro-Climatic Preprocessing & Feature Engineering Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1F3864", fontfamily="serif")
    ax.text(50, 92.5, "Standardized Ingestion, Anomaly Filtering, Stoichiometric Ratios & Stratified Splitting",
            ha="center", va="center", fontsize=9, fontstyle="italic", color="#555555", fontfamily="sans-serif")

    def draw_box(x, y, w, h, title, items, header_color="#2E5496", body_color="#F4F6FA", border_color="#1F3864"):
        shadow = patches.FancyBboxPatch((x+0.6, y-0.6), w, h, boxstyle="round,pad=0.3,rounding_size=1.5",
                                        facecolor="#DDDDDD", edgecolor="none", zorder=1)
        ax.add_patch(shadow)
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5",
                                     facecolor=body_color, edgecolor=border_color, linewidth=1.4, zorder=2)
        ax.add_patch(card)
        header_h = 3.8
        header = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                        boxstyle="round,pad=0.2,rounding_size=1.0",
                                        facecolor=header_color, edgecolor=border_color, linewidth=1, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - header_h/2, title, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#FFFFFF", zorder=4, fontfamily="serif")

        cur_y = y + h - header_h - 2.2
        for item in items:
            ax.text(x + 2, cur_y, f"• {item}", ha="left", va="center",
                    fontsize=8.2, color="#222222", zorder=4, fontfamily="sans-serif")
            cur_y -= 3.0

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor="#2E5496", edgecolor="#1F3864", width=2, headwidth=7, headlength=7),
                    zorder=5)
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 1.6, label, ha="center", va="center",
                    fontsize=7.5, fontweight="bold", color="#2E5496", zorder=6)

    # Box 1: Raw Inputs (Left)
    draw_box(4, 52, 26, 36, "1. Raw Agro-Climatic Data", [
        "Soil Nutrients: N, P, K (kg/ha)",
        "Temperature (°C) & Humidity (%)",
        "Soil Acidity: pH scale [3.5 - 9.0]",
        "Annual Rainfall (mm)",
        "2,200 Observations across 22 Crops",
        "Target Labels: Multi-Class Crop Type"
    ], header_color="#2E5496", body_color="#F8F9FD")

    # Box 2: Data Cleaning & Validation (Middle-Left)
    draw_box(37, 52, 26, 36, "2. Data Quality & Cleansing", [
        "Missing Value Check (Zero NaN verified)",
        "Outlier Detection via Z-score (|z| > 3)",
        "Interquartile Range (IQR) Truncation",
        "Sensor Noise Filtering & Smoothing",
        "Class Balance Validation (100 per class)",
        "Zero-Variance Feature Verification"
    ], header_color="#23497D", body_color="#F0F4FA")

    # Box 3: Feature Engineering (Middle-Right)
    draw_box(70, 52, 26, 36, "3. Feature Engineering Engine", [
        "Stoichiometric Ratios: N/P, N/K, P/K",
        "Total Nutrient Density: N + P + K",
        "Agro-Climatic Aridity Index (P/PET)",
        "Vapor Pressure Deficit (VPD)",
        "Soil-pH Buffering Indicator",
        "Correlation Analysis & VIF < 5.0"
    ], header_color="#186A3B", body_color="#EAFaf1")

    draw_arrow(30, 70, 37, 70, "Ingestion")
    draw_arrow(63, 70, 70, 70, "Clean Data")
    draw_arrow(83, 52, 83, 40, "Engineered")

    # Box 4: Normalization & Scaling (Bottom-Right)
    draw_box(70, 4, 26, 34, "4. Scaling & Normalization", [
        "StandardScaler: z = (x - μ) / σ",
        "Unit Variance & Zero Mean Alignment",
        "MinMax Scaler Comparison: [0, 1]",
        "RobustScaler: Median / IQR Scaling",
        "Leak-Free Pipeline: Fit on Train Only",
        "Persistence via Joblib Artifacts"
    ], header_color="#7D6608", body_color="#FEF9E7")

    draw_arrow(70, 21, 63, 21, "Scaled")

    # Box 5: Stratified Cross-Validation (Bottom-Middle)
    draw_box(37, 4, 26, 34, "5. Cross-Validation Protocol", [
        "Stratified K-Fold CV (K = 5 & K = 10)",
        "Class Balance Preserved across Folds",
        "80% Training Split (1,760 samples)",
        "20% Holdout Testing (440 samples)",
        "Variance & Bias Diagnostics",
        "Leakage Prevention Protocols"
    ], header_color="#6C3483", body_color="#F4ECF7")

    draw_arrow(37, 21, 30, 21, "Validated")

    # Box 6: Downstream Ready Vectors (Bottom-Left)
    draw_box(4, 4, 26, 34, "6. Downstream ML Ready", [
        "High-dimensional Scaled Matrices",
        "X_train, X_test (d = 7 + 4 ratios)",
        "Stratified y_train, y_test labels",
        "Model Ingestion Interfaces Ready",
        "Fast In-Memory NumPy/Pandas arrays",
        "End-to-End Pipeline Artifacts"
    ], header_color="#1F3864", body_color="#EBF5FB")

    plt.tight_layout()
    output_path = os.path.join(DIAG_DIR, "objective_1_architecture.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Created: {output_path}")

# ----------------------------------------------------------------------
# Diagram 2: Objective 2 Architecture (Dual-Engine Cascaded ML System)
# ----------------------------------------------------------------------
def create_objective_2_diagram():
    fig, ax = plt.subplots(figsize=(9, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Title
    ax.text(50, 97, "Objective 2: Dual-Engine Cascaded ML Architecture",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1F3864", fontfamily="serif")
    ax.text(50, 94, "Stage 1 Multi-Class Crop Recommender + Stage 2 Crop-Conditioned Fertilizer Engine",
            ha="center", va="center", fontsize=9, fontstyle="italic", color="#555555", fontfamily="sans-serif")

    def draw_card(x, y, w, h, title, items, h_col="#2E5496", b_col="#F4F6FA", border="#1F3864"):
        shadow = patches.FancyBboxPatch((x+0.5, y-0.5), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                        facecolor="#E0E0E0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor=b_col, edgecolor=border, linewidth=1.3, zorder=2)
        ax.add_patch(card)
        hh = 3.6
        hdr = patches.FancyBboxPatch((x, y+h-hh), w, hh, boxstyle="round,pad=0.2,rounding_size=0.8",
                                     facecolor=h_col, edgecolor=border, linewidth=1, zorder=3)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - hh/2, title, ha="center", va="center",
                fontsize=9.2, fontweight="bold", color="#FFFFFF", zorder=4, fontfamily="serif")
        cy = y + h - hh - 2.0
        for it in items:
            ax.text(x + 2, cy, f"• {it}", ha="left", va="center",
                    fontsize=8.0, color="#1A1A1A", zorder=4, fontfamily="sans-serif")
            cy -= 2.6

    def draw_conn(x1, y1, x2, y2, txt="", col="#2E5496"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=col, edgecolor="#1F3864", width=2, headwidth=6, headlength=6),
                    zorder=5)
        if txt:
            ax.text((x1+x2)/2 + 2, (y1+y2)/2, txt, ha="left", va="center",
                    fontsize=7.5, fontweight="bold", color=col, zorder=6)

    # Input Layer (Top)
    draw_card(15, 80, 70, 11, "Input Feature Vector: x ∈ ℝ⁷ (Soil & Climate Sensor Readings)", [
        "Nitrogen (N), Phosphorus (P), Potassium (K) | Temp (°C), Rel. Humidity (%), pH, Rainfall (mm)"
    ], h_col="#1B4F72", b_col="#EAF2F8")

    draw_conn(50, 80, 50, 72, "Scaled Ingestion")

    # STAGE 1: Crop Recommendation Engine
    draw_card(6, 44, 88, 28, "STAGE 1: Multi-Class Crop Recommendation Ensemble Engine", [
        "Algorithm Suite: Random Forest Classifier (M=100 trees, max_depth=16, Gini Impurity criterion)",
        "Decision Tree Classifier (CART, min_samples_split=4) & K-Nearest Neighbors (k=5, Minkowski metric)",
        "Softmax Probability Vector: P(Crop = c | x) = exp(f_c(x)) / Σ_j exp(f_j(x)) for c ∈ {1..22}",
        "GridSearchCV Hyperparameter Optimization across 5-fold Stratified Validation",
        "Performance: Random Forest = 99.32% Accuracy, Decision Tree = 98.18%, KNN = 97.73%",
        "Predicted Primary Output: Optimal Crop Type c* = argmax P(Crop = c | x)"
    ], h_col="#196F3D", b_col="#E9F7EF")

    draw_conn(50, 44, 50, 36, "Crop Prediction c* & Nutrients")

    # Conditioning Junction Box
    draw_card(20, 27, 60, 9, "Conditioning & Feature Augmentation Junction", [
        "Augment: Soil Nutrients (N, P, K) + Soil Type (Black/Clay/Loamy) + Moisture + Target Crop c*"
    ], h_col="#B7950B", b_col="#FEFDE8")

    draw_conn(50, 27, 50, 20, "Augmented Vector z")

    # STAGE 2: Fertilizer Prediction Engine
    draw_card(6, 2, 88, 18, "STAGE 2: Crop-Conditioned Fertilizer Recommendation Engine", [
        "Input: Augmented vector z = [c*, Soil_Type, Moisture, N, P, K, Temp, Humidity]",
        "Formulation: Multi-Class Nutrient Gap Formulation & Fertilizer Mapping Classifier",
        "Target Classes (7 Formulations): Urea, DAP, 14-35-14, 28-28, 17-17-17, 20-20, 10-26-26",
        "Ensemble RF/KNN Classifier achieves 98.9% Accuracy on fertilizer deficiency matching",
        "Advisory Output: Specific Fertilizer Form, Application Rate (kg/acre), and N-P-K Deficit Remedy"
    ], h_col="#6C3483", b_col="#F5EEF8")

    plt.tight_layout()
    output_path = os.path.join(DIAG_DIR, "objective_2_architecture.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[OK] Created: {output_path}")

if __name__ == "__main__":
    create_objective_1_diagram()
    create_objective_2_diagram()
