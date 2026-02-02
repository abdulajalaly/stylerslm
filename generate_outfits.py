"""
Generate top outfit recommendations from a wardrobe and context.

Usage:
    wardrobe = [
        {"category": "shirt", "color": "white", "subtype": "oxford"},
        {"category": "pants", "color": "black", "subtype": "chinos"},
        ...
    ]
    context = {"occasion": "business", "temperature": "mild", "style": "formal"}
    top = generate_outfits(wardrobe, context, top_k=3)
"""

import itertools
from predict import predict_outfit
from ontology import COLORS, STYLES, OCCASIONS, TEMPERATURE, SUBTYPES, FITS


def _default_context():
    return {
        "occasion": "business",
        "temperature": "mild",
        "style": "formal",
        "fit": "regular",
    }


def generate_outfits(wardrobe, context=None, top_k=3):
    """
    Accept wardrobe (list of items) and context (dict), return top_k outfit recommendations.

    Each wardrobe item: {"category": "shirt"|"pants"|"shoes", "color": str, "subtype": str}
    Context can include: occasion, temperature, style, fit, outerwear (optional; defaults used if missing).

    Returns:
        list of (score, outfit_dict) for top_k outfits, sorted by score descending.
    """
    if context is None:
        context = _default_context()
    ctx = _default_context()
    ctx.update(context)

    shirts = [i for i in wardrobe if i.get("category") == "shirt"]
    pants_list = [i for i in wardrobe if i.get("category") == "pants"]
    shoes_list = [i for i in wardrobe if i.get("category") == "shoes"]

    if not shirts or not pants_list or not shoes_list:
        return []

    results = []
    for s, p, sh in itertools.product(shirts, pants_list, shoes_list):
        score = predict_outfit(
            s["color"], p["color"], sh["color"],
            ctx["style"],
            s.get("subtype") or SUBTYPES["shirt"][0],
            p.get("subtype") or SUBTYPES["pants"][0],
            sh.get("subtype") or SUBTYPES["shoes"][0],
            ctx.get("fit") or "regular",
            ctx["temperature"],
            ctx["occasion"],
            ctx.get("outerwear") or "none",
        )
        outfit = {"shirt": s, "pants": p, "shoes": sh}
        results.append((score, outfit))

    results.sort(key=lambda r: r[0], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    wardrobe = [
        {"category": "shirt", "color": "white", "subtype": "oxford"},
        {"category": "shirt", "color": "navy", "subtype": "dress_shirt"},
        {"category": "pants", "color": "black", "subtype": "trousers"},
        {"category": "pants", "color": "beige", "subtype": "chinos"},
        {"category": "shoes", "color": "black", "subtype": "loafers"},
        {"category": "shoes", "color": "brown", "subtype": "loafers"},
    ]
    context = {"occasion": "business", "temperature": "mild", "style": "formal"}

    top = generate_outfits(wardrobe, context, top_k=3)
    print("Top 3 outfits:")
    for i, (score, outfit) in enumerate(top, 1):
        s, p, sh = outfit["shirt"], outfit["pants"], outfit["shoes"]
        print(f"  {i}. Score {score:.2f} — Shirt: {s['color']} {s['subtype']} | Pants: {p['color']} {p['subtype']} | Shoes: {sh['color']} {sh['subtype']}")
