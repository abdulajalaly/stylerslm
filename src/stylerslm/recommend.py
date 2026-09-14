"""Generate ranked outfit combinations from a wardrobe."""

import itertools

from .ontology import SUBTYPES
from .predict import predict_outfit


def generate_outfits(wardrobe, context=None, top_k=3):
    defaults = {"occasion": "business", "temperature": "mild", "style": "formal", "fit": "regular", "outerwear": "none"}
    settings = {**defaults, **(context or {})}
    shirts = [item for item in wardrobe if item.get("category") == "shirt"]
    pants = [item for item in wardrobe if item.get("category") == "pants"]
    shoes = [item for item in wardrobe if item.get("category") == "shoes"]
    if not shirts or not pants or not shoes:
        return []

    results = []
    for shirt, trouser, shoe in itertools.product(shirts, pants, shoes):
        score = predict_outfit(
            shirt["color"], trouser["color"], shoe["color"], settings["style"],
            shirt.get("subtype", SUBTYPES["shirt"][0]), trouser.get("subtype", SUBTYPES["pants"][0]),
            shoe.get("subtype", SUBTYPES["shoes"][0]), settings["fit"], settings["temperature"],
            settings["occasion"], settings["outerwear"],
        )
        results.append((score, {"shirt": shirt, "pants": trouser, "shoes": shoe}))
    return sorted(results, key=lambda result: result[0], reverse=True)[:top_k]