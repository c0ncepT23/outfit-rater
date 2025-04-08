# test_detect_from_image.py

from vision.yolo_detector import (
    detect_outfit_yolo as detect_outfit_from_image,
    save_detection_image
)
from rating_engine import rate_outfit

# Path to test image
image_path = "vision/sample_images/outfit1.jpg"

# Run detection
result = detect_outfit_from_image(image_path)

# Print detections
detected = result["detected"]
print("🎯 Detected Outfit:")
print(f" - top: {detected['top']}")
print(f" - bottom: {detected['bottom']}")
print(f" - shoes: {detected['shoes']}")
print(f" - accessories: {detected['accessories']}")
print(f" - color_palette: {detected['color_palette']}")
print(f" - fit: {detected['fit']}")
print()

# Score the outfit
score, feedback = rate_outfit(detected)
print(f"⭐ Score: {score}/100")
print(f"💬 Feedback: {feedback}")

# Save image with YOLO boxes
save_detection_image(
    image_path,
    result=result["raw_result"],
    output_path="vision/output/outfit1_pred.jpg"
)

print("📸 Bounding box image saved to: vision/output/outfit1_pred.jpg")
