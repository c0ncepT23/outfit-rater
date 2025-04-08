# app.py

import streamlit as st
import os
import csv
from pathlib import Path
from datetime import datetime
from PIL import Image
from vision.yolo_detector import detect_outfit_yolo, save_detection_image
from rating_engine import rate_outfit

st.set_page_config(page_title="Outfit Rater AI", layout="centered")
st.title("🧥 Outfit Rater AI")
st.caption("Upload your fit, pick the vibe, and get instant feedback 🔥")

uploaded_file = st.file_uploader("📤 Upload an outfit image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    vibe = st.selectbox(
        "🧠 What vibe is this outfit for?",
        ["Chill", "Casual", "College", "Work", "Wedding", "Party", "Sport", "Travel"]
    )

    image_path = "vision/output/temp_uploaded.jpg"
    output_path = "vision/output/temp_result.jpg"

    # Save uploaded image
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Detect outfit
    result = detect_outfit_yolo(image_path)
    detected = result["detected"]
    score, feedback = rate_outfit(detected)

    # Draw bounding boxes
    save_detection_image(image_path, result=result["raw_result"], output_path=output_path)

    # Display results
    st.subheader("📸 Your Look (Detected):")
    st.image(Image.open(output_path), use_container_width=True)

    st.subheader("🎯 Detection:")
    st.write(f"**Top:** {detected['top']}")
    st.write(f"**Bottom:** {detected['bottom']}")
    st.write(f"**Shoes:** {detected['shoes']}")
    st.write(f"**Accessories:** {', '.join(detected['accessories']) or 'None'}")
    st.write(f"**Color Palette:** {detected['color_palette']}")
    st.write(f"**Fit:** {detected['fit']}")
    st.write(f"**Vibe:** {vibe}")

    st.subheader("⭐ Score:")
    st.markdown(f"<h2>{score}/100</h2>", unsafe_allow_html=True)

    st.subheader("💬 Feedback:")
    st.success(feedback)

    # 🔁 Auto-save to CSV
    log_path = Path("vision/output/outfit_log.csv")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_exists = log_path.exists()

    with open(log_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "image", "top", "bottom", "shoes", "accessories",
            "color_palette", "fit", "vibe", "score", "feedback"
        ])
        if not log_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "image": uploaded_file.name,
            "top": detected["top"],
            "bottom": detected["bottom"],
            "shoes": detected["shoes"],
            "accessories": ", ".join(detected["accessories"]),
            "color_palette": detected["color_palette"],
            "fit": detected["fit"],
            "vibe": vibe,
            "score": score,
            "feedback": feedback
        })

    st.success("✅ Outfit auto-saved to outfit_log.csv")
    # 📚 Outfit History Gallery
st.markdown("---")
st.header("📖 My Outfit History")

log_path = Path("vision/output/outfit_log.csv")

if log_path.exists():
    import pandas as pd
    df = pd.read_csv(log_path)

    # Optional vibe filter
    selected_vibe = st.selectbox("🔍 Filter by vibe", ["All"] + sorted(df["vibe"].unique().tolist()))
    if selected_vibe != "All":
        df = df[df["vibe"] == selected_vibe]

    # Sort most recent first
    df = df.sort_values(by="timestamp", ascending=False)

    for _, row in df.iterrows():
        img_name = Path(row["image"]).stem
        img_path = f"vision/output/{img_name}_pred.jpg"

        col1, col2 = st.columns([1, 2])
        with col1:
            if Path(img_path).exists():
                st.image(img_path, use_container_width=True)
            else:
                st.warning("Image not found")

        with col2:
            st.markdown(f"**🕒 {row['timestamp']}**")
            st.markdown(f"**🎯 Score:** `{row['score']}/100`")
            st.markdown(f"**🌈 Vibe:** `{row['vibe']}`")
            st.markdown(f"**👕 Top:** {row['top']}  \n**👖 Bottom:** {row['bottom']}  \n**👟 Shoes:** {row['shoes']}")
            st.markdown(f"**💬 Feedback:** {row['feedback']}")
        st.markdown("---")

else:
    st.info("No outfit history yet. Upload your first fit!")

