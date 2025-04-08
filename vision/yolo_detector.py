from ultralytics import YOLO
import cv2
from sklearn.cluster import KMeans
from collections import Counter

MODEL_PATH = "vision/best.pt"

CATEGORY_MAP = {
    "clothing": "clothing",
    "shirt": "top",
    "t-shirt": "top",
    "top": "top",
    "jacket": "top",
    "dress": "top",
    "kurta": "top",
    "pants": "bottom",
    "trousers": "bottom",
    "jeans": "bottom",
    "shorts": "bottom",
    "skirt": "bottom",
    "shoe": "shoes",
    "shoes": "shoes",
    "sneakers": "shoes",
    "footwear": "shoes",
    "bag": "accessory",
    "backpack": "accessory",
    "hat": "accessory",
    "watch": "accessory",
}

model = YOLO(MODEL_PATH)

def extract_dominant_color(image_path, k=3):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    image = cv2.resize(image, (200, 200))
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(image)
    cluster_centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = Counter(labels)
    dominant_rgb = cluster_centers[counts.most_common(1)[0][0]]
    return label_color(dominant_rgb)

def label_color(rgb):
    r, g, b = rgb
    brightness = sum([r, g, b]) / 3
    if brightness < 75:
        return "dark"
    elif brightness > 200:
        return "bright"
    elif abs(r - g) < 20 and abs(g - b) < 20:
        return "neutral"
    else:
        return "coordinated"

def detect_outfit_yolo(image_path):
    results = model(image_path)[0]
    boxes = results.boxes
    classes = results.names

    detected_items = {
        "top": None,
        "bottom": None,
        "shoes": None,
        "accessories": [],
    }

    clothing_counter = 0

    for box in boxes:
        cls_id = int(box.cls[0])
        label = classes[cls_id].lower()
        print("Detected label:", label)

        mapped = CATEGORY_MAP.get(label)

        if mapped == "top" and not detected_items["top"]:
            detected_items["top"] = label
        elif mapped == "bottom" and not detected_items["bottom"]:
            detected_items["bottom"] = label
        elif mapped == "clothing":
            clothing_counter += 1
            if clothing_counter == 1 and not detected_items["top"]:
                detected_items["top"] = "clothing"
            elif clothing_counter == 2 and not detected_items["bottom"]:
                detected_items["bottom"] = "clothing"
        elif mapped == "shoes" and not detected_items["shoes"]:
            detected_items["shoes"] = label
        elif mapped == "accessory":
            detected_items["accessories"].append(label)

    if not detected_items["top"]:
        detected_items["top"] = "unknown"
    if not detected_items["bottom"]:
        detected_items["bottom"] = "unknown"
    if not detected_items["shoes"]:
        detected_items["shoes"] = "unknown"

    detected_items["color_palette"] = extract_dominant_color(image_path)
    detected_items["fit"] = "regular"

    return {
        "detected": detected_items,
        "raw_result": results  # 👈 return the actual YOLO result object
    }


def save_detection_image(image_path, result, output_path):
    """Draw bounding boxes on the image and save it."""
    import cv2
    from pathlib import Path

    im = result.plot()  # YOLO draws boxes on this
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)  # make dir if needed
    cv2.imwrite(str(output_path), im)

