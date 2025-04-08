# train_yolo.py

import shutil
import os
from ultralytics import YOLO

# === CONFIG ===========================
MODEL_SIZE = "yolov8n.pt"  # use yolov8s.pt or yolov8m.pt for more accuracy
EPOCHS = 30
IMG_SIZE = 640

DATA_YAML = "Clothing-Detection-1/data.yaml"
BEST_PT_TARGET = "vision/best.pt"  # where to save best model
# ======================================

def train_model():
    print("🚀 Starting YOLOv8 training...")
    
    model = YOLO(MODEL_SIZE)

    results = model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        verbose=True
    )

    print("✅ Training complete.")
    from pathlib import Path
    best_model_path = Path(results.save_dir) / "weights" / "best.pt"


    if os.path.exists(best_model_path):
        print(f"📦 Found best.pt at {best_model_path}")
        print(f"📁 Copying to {BEST_PT_TARGET}...")
        shutil.copy(best_model_path, BEST_PT_TARGET)
        print("✅ Model saved to vision/best.pt")
    else:
        print("❌ best.pt not found — check training output.")

if __name__ == "__main__":
    train_model()
