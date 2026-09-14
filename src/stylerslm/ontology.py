"""Allowed categorical values used by the feature encoder."""

COLORS = ["white", "black", "grey", "navy", "beige", "brown", "cream", "charcoal", "olive", "burgundy", "red", "blue", "green", "yellow", "silver", "gold"]
STYLES = ["casual", "smart_casual", "formal", "old_money", "streetwear", "minimal", "athleisure", "gorpcore", "vintage"]
OCCASIONS = ["university", "business", "date", "party", "gym", "travel", "club", "lounge"]
TEMPERATURE = ["freezing", "cold", "mild", "warm", "hot"]
FITS = ["skinny", "slim", "regular", "relaxed", "oversized", "cropped"]
SUBTYPES = {
    "shirt": ["tee", "graphic_tee", "long_sleeve", "polo", "henley", "oxford", "dress_shirt", "flannel", "overshirt", "hoodie", "sweatshirt", "sweater", "turtleneck", "cardigan"],
    "pants": ["jeans", "chinos", "trousers", "pleated_trousers", "shorts", "swim_shorts", "cargos", "carpenter_pants", "sweatpants", "joggers", "track_pants"],
    "shoes": ["sneakers", "chunky_sneakers", "running_shoes", "loafers", "boots", "chelsea_boots", "derbies", "slides", "sandals"],
    "outerwear": ["none", "blazer", "suit_jacket", "denim_jacket", "bomber", "varsity_jacket", "leather_jacket", "gilet", "trench", "overcoat", "peacoat", "puffer", "parka", "windbreaker"],
}
OUTERWEAR = SUBTYPES["outerwear"]