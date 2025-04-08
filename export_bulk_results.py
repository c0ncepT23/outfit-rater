# export_bulk_results.py

import os
import csv
from pathlib import Path
from vision.yolo_detector import (
    detect_outfit_yolo as detect_outfit_from_image,
    save_detection_image
)
from rating_engine import rate_outfit

INPUT_FOLDER = "vision/sample_images"
OUTPUT_FOLDER = "vision/output"
CSV_PATH = "vision/output/outfit_results.csv"

Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

rows = []

for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"{Path(filename).stem}_pred.jpg")

    print(f"\n🖼️ Processing {filename}...")

    result = detect_outfit_from_image(image_path)
    detected = result["detected"]
    score, feedback = rate_outfit(detected)

    save_detection_image(image_path, result=result["raw_result"], output_path=output_path)

    row = {
        "image": filename,
        "top": detected["top"],
        "bottom": detected["bottom"],
        "shoes": detected["shoes"],
        "accessories": ", ".join(detected["accessories"]),
        "color_palette": detected["color_palette"],
        "fit": detected["fit"],
        "score": score,
        "feedback": feedback
    }

    rows.append(row)

# Write to CSV
with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"\n✅ Results saved to: {CSV_PATH}")
