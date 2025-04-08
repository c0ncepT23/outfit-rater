# rating_engine.py

def rate_outfit(detected):
    score = 50
    feedback = []

    top = detected.get("top")
    bottom = detected.get("bottom")
    shoes = detected.get("shoes")
    accessories = detected.get("accessories", [])
    color = detected.get("color_palette")
    fit = detected.get("fit")

    if top != "unknown" and bottom != "unknown":
        score += 10
        feedback.append("Fit looks clean and intentional.")

    if color in ["coordinated", "neutral"]:
        score += 5
        feedback.append("Color palette is well coordinated.")

    if shoes != "unknown":
        score += 5
        feedback.append("Footwear fits the vibe.")
    else:
        feedback.append("Footwear could use a style upgrade.")

    if accessories:
        score += 5
        feedback.append("Accessories elevate the look.")
    else:
        feedback.append("Try adding one accessory to polish the fit.")

    if fit == "regular":
        feedback.append("Outfit is safe and clean, but could use a personal twist.")
    else:
        score += 5
        feedback.append("Fit adds personality to the look.")

    score = min(score, 100)
    feedback.append("Confidence levels: high 🔥")

    return score, " ".join(feedback)
