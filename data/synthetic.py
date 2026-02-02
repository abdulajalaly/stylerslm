import random
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ontology import COLORS, STYLES, OCCASIONS, TEMPERATURE, SUBTYPES, FITS, OUTERWEAR


def generate(n=5000):
    rows = []
    for _ in range(n):
        shirt = random.choice(COLORS)
        pants = random.choice(COLORS)
        shoes = random.choice(COLORS)
        style = random.choice(STYLES)
        shirt_subtype = random.choice(SUBTYPES["shirt"])
        pants_subtype = random.choice(SUBTYPES["pants"])
        shoes_subtype = random.choice(SUBTYPES["shoes"])
        fit = random.choice(FITS)
        temperature = random.choice(TEMPERATURE)
        occasion = random.choice(OCCASIONS)
        outerwear = random.choice(OUTERWEAR)

        score = 0
        if shirt == pants:
            score += 1
        if style == "old_money" and shoes in ["black", "beige", "navy", "brown"]:
            score += 2
        if shoes == "navy" and style == "formal":
            score += 1
        if temperature == "cold" and shoes_subtype == "sandals":
            score -= 2
        if occasion == "business" and style == "casual" and shirt_subtype == "tee":
            score -= 1
        if occasion == "party" and style == "formal":
            score += 1
        # Winter logic: cold without outerwear -> penalty
        if temperature == "cold" and outerwear == "none":
            score -= 2
        # Summer logic: hot with outerwear -> penalty
        if temperature == "hot" and outerwear != "none":
            score -= 2

        rows.append([
            shirt, pants, shoes, style,
            shirt_subtype, pants_subtype, shoes_subtype,
            fit, temperature, occasion, outerwear,
            score
        ])

    columns = [
        "shirt", "pants", "shoes", "style",
        "shirt_subtype", "pants_subtype", "shoes_subtype",
        "fit", "temperature", "occasion", "outerwear",
        "score"
    ]
    df = pd.DataFrame(rows, columns=columns)
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "synthetic.csv")
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    generate()
