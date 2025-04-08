# vision/outfit_detector.py

import torch
import clip
from PIL import Image
from sklearn.cluster import KMeans
import cv2
from collections import Counter
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Category prompts
CATEGORY_LABELS = {
    "top": ["t-shirt", "shirt", "kurta", "hoodie", "blazer"],
    "bottom": ["jeans", "pants", "skirt", "shorts", "palazzos"],
    "shoes": ["sneakers", "slides", "boots", "loafers", "heels"]
}


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


def classify_image(image_path, categories):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    texts = clip.tokenize(categories).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image)
        text_features = clip_model.encode_text(texts)
        logits_per_image, _ = clip_model(image, texts)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

    best_idx = probs.argmax()
    return categories[best_idx]


def detect_outfit_from_image(image_path):
    outfit = {}
    outfit["color_palette"] = extract_dominant_color(image_path)

    for category, options in CATEGORY_LABELS.items():
        best_match = classify_image(image_path, options)
        outfit[category] = best_match

    # Estimate fit randomly for now — upgrade later with pose detection
    outfit["fit"] = "regular"
    outfit["accessories"] = ["watch"]  # Placeholder for now

    return outfit
