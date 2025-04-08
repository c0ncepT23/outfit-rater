# test_bulk_process.py

import os
from pathlib import Path
from vision.yolo_detector import (
    detect_outfit_yolo as detect_outfit_from_image,
    save_detection_image
)
from rating_engine import rate_outfit

INPUT_FOLDER = "vision/sample_images"
OUTPUT_FOLDER = "vision/output"

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

# Loop through all images in input folder
for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"{Path(filename).stem}_pred.jpg")

    print(f"\n🖼️ Processing {filename}...")

    result = detect_outfit_from_image(image_path)
    detected = result["detected"]
    score, feedback = rate_outfit(detected)

    print("🎯 Detected Outfit:")
    print(f" - top: {detected['top']}")
    print(f" - bottom: {detected['bottom']}")
    print(f" - shoes: {detected['shoes']}")
    print(f" - accessories: {detected['accessories']}")
    print(f" - color_palette: {detected['color_palette']}")
    print(f" - fit: {detected['fit']}")
    print()
    print(f"⭐ Score: {score}/100")
    print(f"💬 Feedback: {feedback}")

    save_detection_image(image_path, result=result["raw_result"], output_path=output_path)
    print(f"📸 Saved: {output_path}")
