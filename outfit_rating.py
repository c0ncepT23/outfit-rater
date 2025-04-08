# outfit_rating.py

def rate_outfit(outfit_details, occasion="casual"):
    """
    Smart scoring of an outfit based on categories like fit, color, occasion, creativity, and more.
    """
    score = 0
    feedback = []

    # Extract parts
    top = outfit_details.get("top", "")
    bottom = outfit_details.get("bottom", "")
    shoes = outfit_details.get("shoes", "")
    color = outfit_details.get("color_palette", "")
    fit = outfit_details.get("fit", "")
    accessories = outfit_details.get("accessories", [])

    # 1️⃣ Fit & Structure (20 pts)
    if fit == "tailored":
        score += 18
        feedback.append("Tailored fit — sharp and intentional.")
    elif fit == "regular":
        score += 14
        feedback.append("Fit looks clean and intentional.")
    else:  # loose, oversized
        score += 8
        feedback.append("Fit feels relaxed — might work depending on the style.")

    # 2️⃣ Color Coordination (15 pts)
    if color == "coordinated":
        score += 13
        feedback.append("Color palette is well coordinated.")
    elif color == "neutral":
        score += 11
        feedback.append("Neutral palette — always safe and stylish.")
    elif color == "bright":
        score += 8
        feedback.append("Bold color choices — could be a fashion statement or a clash.")
    else:
        score += 5
        feedback.append("Color combo seems a bit off — might need better balance.")

    # 3️⃣ Occasion Match (20 pts)
    formal_wear = ["blazer", "suit", "kurta"]
    casual_wear = ["t-shirt", "hoodie", "shirt"]
    party_wear = ["dress", "heels", "jumpsuit"]

    occasion_score = 10  # default

    if occasion == "wedding" and top in formal_wear:
        occasion_score = 20
        feedback.append("Perfectly matched for a wedding. Regal vibes.")
    elif occasion == "classroom" and top in casual_wear:
        occasion_score = 18
        feedback.append("On point for a classroom fit.")
    elif occasion == "sports" and shoes == "sneakers":
        occasion_score = 17
        feedback.append("Athletic and ready — sports appropriate.")
    elif occasion == "casual":
        occasion_score = 15
        feedback.append("Chill outfit for a casual day.")

    score += occasion_score

    # 4️⃣ Footwear + Accessories (15 pts)
    footwear_score = 0
    if shoes in ["sneakers", "loafers", "heels"]:
        footwear_score += 8
        feedback.append("Footwear fits the vibe.")
    elif shoes == "slides":
        footwear_score += 5
        feedback.append("Slides are comfy but context-sensitive.")
    else:
        footwear_score += 4
        feedback.append("Footwear could use a style upgrade.")

    if accessories:
        footwear_score += 5
        feedback.append("Accessories elevate the look.")
    else:
        footwear_score += 2
        feedback.append("Try adding one accessory to polish the fit.")

    score += footwear_score

    # 5️⃣ Creativity / Personality (10 pts)
    if color == "bright" or shoes == "heels" or top in ["kurta", "jumpsuit", "dress"]:
        score += 8
        feedback.append("There's personality and effort in this fit.")
    else:
        score += 5
        feedback.append("Outfit is safe and clean, but could use a personal twist.")

    # 6️⃣ Swagger / Confidence (10 pts)
    if color in ["coordinated", "bright"] and fit != "loose":
        score += 8
        feedback.append("Confidence levels: high 🔥")
    else:
        score += 5
        feedback.append("Chill look — not loud, but still composed.")

    # Clamp to 100
    score = min(score, 100)

    return {
        "score": score,
        "feedback": " ".join(feedback)
    }


# 🔁 Example usage:
if __name__ == "__main__":
    outfit = {
        "top": "kurta",
        "bottom": "pants",
        "shoes": "slides",
        "accessories": ["watch", "ring"],
        "color_palette": "coordinated",
        "fit": "regular"
    }
    occasion = "wedding"
    result = rate_outfit(outfit, occasion)
    print(f"Score: {result['score']}/100")
    print("Feedback:", result["feedback"])
