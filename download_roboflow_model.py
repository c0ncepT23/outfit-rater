# download_roboflow_model.py

from roboflow import Roboflow

# 👇 Your private API key (use only for development)
rf = Roboflow(api_key="3plvRAw6wU8jVCMLym0z")

# 👇 Connect to the project (cloned from public Clothing Detection)
project = rf.workspace("object-detection-bounding-box-fg9op").project("clothing-detection-scn9m")

# 👇 Download the model weights
model = project.version(1).download("yolov8")

print(f"✅ Model downloaded to: {model}")
