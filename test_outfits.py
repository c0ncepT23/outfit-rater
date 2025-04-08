# test_outfits.py

import json
from outfit_rating import rate_outfit

def load_sample_outfits(path):
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    sample_data = load_sample_outfits("data/sample_inputs.json")

    for idx, outfit in enumerate(sample_data, 1):
        print(f"\n👕 Outfit #{idx}")
        occasion = outfit.pop("occasion", "casual")  # remove from dict, pass separately
        result = rate_outfit(outfit, occasion)
        print(f"Score: {result['score']}/100")
        print("Feedback:", result["feedback"])
