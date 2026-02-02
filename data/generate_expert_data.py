import pandas as pd
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tqdm import tqdm
from ontology import (
    COLORS, STYLES, OCCASIONS, TEMPERATURE,
    SUBTYPES, FITS, OUTERWEAR
)

class FashionBrain2026:
    def __init__(self):
        # 1. Defined Palettes for 2026
        self.earth_tones = {"beige", "brown", "olive", "cream", "green"}
        self.monochrome = {"black", "grey", "charcoal", "white"}
        self.pop_colors = {"red", "blue", "yellow"}
        
        # 2. Style Definitions (What defines these looks?)
        self.style_rules = {
            "gorpcore": {
                "items": ["cargos", "carpenter_pants", "fleece", "puffer", "windbreaker", "boots", "running_shoes"],
                "materials": ["goretex", "nylon", "fleece"],
                "colors": self.earth_tones | {"black", "charcoal"}
            },
            "old_money": {
                "items": ["polo", "oxford", "linen", "chino", "loafers", "sweater", "trench"],
                "colors": {"white", "beige", "navy", "cream", "brown"},
                "fit": {"regular", "slim"}
            },
            "athleisure": {
                "items": ["hoodie", "sweatpants", "joggers", "track_pants", "running_shoes", "sneakers", "gilet"],
                "fit": {"relaxed", "oversized", "regular"}
            },
            "streetwear": {
                "items": ["graphic_tee", "hoodie", "cargos", "baggy_jeans", "chunky_sneakers", "bomber", "varsity_jacket"],
                "fit": {"oversized", "relaxed"}
            },
            "business": { # Used as a style constraint for the "business" occasion
                "items": ["suit_jacket", "dress_shirt", "trousers", "oxford", "derbies", "chelsea_boots", "coat"],
                "forbidden": ["hoodie", "sweatpants", "shorts", "sandals"]
            }
        }

    def get_compatibility_score(self, row):
        """Checks if items physically/socially make sense together."""
        score = 1.0
        
        # Unpack
        shirt, pants, shoes, out = row['shirt_subtype'], row['pants_subtype'], row['shoes_subtype'], row['outerwear']
        style, occ, temp = row['style'], row['occasion'], row['temperature']
        fit = row['fit']

        # --- RULE 1: The "Anti-Clash" Logic (Hard Penalties) ---
        
        # Formal Clashes
        if style == "formal" or occ == "business":
            if pants in ["sweatpants", "joggers", "shorts", "swim_shorts", "cargos"]:
                return 0.0 # Never wear sweatpants to a meeting
            if shoes in ["slides", "sandals", "running_shoes"]:
                return 0.0
            if shirt in ["graphic_tee", "hoodie"]:
                return 0.1
        
        # Gym Clashes
        if occ == "gym":
            if shoes in ["loafers", "boots", "derbies", "chelsea_boots"]:
                return 0.0
            if pants in ["jeans", "chinos", "trousers"]:
                return 0.2
            if style not in ["athleisure", "streetwear"]:
                score -= 0.5

        # Weather Physics
        if temp == "freezing":
            if pants in ["shorts", "swim_shorts"]:
                return 0.0 # Frostbite
            if out in ["none", "gilet"]:
                score -= 0.6
            if out in ["puffer", "parka", "overcoat"]:
                score += 0.3
        
        if temp == "hot":
            if out not in ["none", "gilet"]:
                score -= 0.5 # Heatstroke
            if pants in ["sweatpants", "heavy_cotton"]:
                score -= 0.3

        # --- RULE 2: Style Consistency (Does it match the "Vibe"?) ---
        
        # Gorpcore Check
        if style == "gorpcore":
            if pants in self.style_rules["gorpcore"]["items"] or out in self.style_rules["gorpcore"]["items"]:
                score += 0.2
            if shoes == "loafers" or shirt == "dress_shirt":
                score -= 0.4

        # Old Money Check
        if style == "old_money":
            if shirt in ["graphic_tee", "hoodie"] or pants in ["cargos", "sweatpants"]:
                score -= 0.5
            if row['shirt'] in self.pop_colors: # Old money hates bright yellow/red
                score -= 0.2

        # Athleisure Check
        if style == "athleisure":
            if pants in ["jeans", "trousers"]:
                score -= 0.3
            if fit == "skinny": # 2026 Athleisure is loose
                score -= 0.2

        return score

    def get_color_score(self, row):
        """Rates color harmony."""
        palette = {row['shirt'], row['pants'], row['shoes']}
        if row['outerwear'] != "none":
            palette.add(row['outerwear']) # Note: Outerwear in ontology is subtypes, checking color col
            
        # We need to look at the COLOR columns, not subtypes
        c_shirt, c_pants, c_shoes = row['shirt'], row['pants'], row['shoes']
        
        score = 1.0
        
        # No Brown Shoes with Black Pants (The Golden Rule)
        if c_pants == "black" and c_shoes == "brown":
            return 0.4
        
        # Monochromatic fits are trendy
        if len(palette) == 1:
            score += 0.2
            
        # Sandwich Rule (Top matches Shoes)
        if c_shirt == c_shoes:
            score += 0.1
            
        return score

    def rate_outfit(self, row):
        base = 0.5
        
        compat = self.get_compatibility_score(row)
        if compat == 0.0: return 0.0 # Fail instantly
        
        colors = self.get_color_score(row)
        
        final = base * compat * colors
        
        # Cap at 1.0
        return max(0.0, min(1.0, final))

def generate_data(num_samples=50000):
    print(f"Generating {num_samples} expert 2026 fashion entries...")
    stylist = FashionBrain2026()
    data = []
    
    # Pre-calculate lists to speed up loop
    keys_shirt = SUBTYPES["shirt"]
    keys_pants = SUBTYPES["pants"]
    keys_shoes = SUBTYPES["shoes"]
    keys_out = SUBTYPES["outerwear"]

    for _ in tqdm(range(num_samples)):
        # 1. Randomly Assemble an Outfit
        row = {
            "shirt": random.choice(COLORS),
            "pants": random.choice(COLORS),
            "shoes": random.choice(COLORS),
            "style": random.choice(STYLES),
            "shirt_subtype": random.choice(keys_shirt),
            "pants_subtype": random.choice(keys_pants),
            "shoes_subtype": random.choice(keys_shoes),
            "fit": random.choice(FITS),
            "temperature": random.choice(TEMPERATURE),
            "occasion": random.choice(OCCASIONS),
            "outerwear": random.choice(keys_out) # Random subtype
        }
        
        # 2. Rate it
        row["score"] = stylist.rate_outfit(row)
        
        # 3. Add to dataset
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv("data/expert_data_2026.csv", index=False)
    print("Done! Saved to data/expert_data_2026.csv")

if __name__ == "__main__":
    generate_data()