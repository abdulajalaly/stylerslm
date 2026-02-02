# ontology.py

COLORS = [
    "white", "black", "grey", "navy", "beige", "brown", # Basics
    "cream", "charcoal", "olive", "burgundy",           # Essential Neutrals
    "red", "blue", "green", "yellow",                   # Primaries
    "silver", "gold"                                    # Accents/Jewelry
]

STYLES = [
    "casual",
    "smart_casual",  # Crucial bridge category (Dates/Office)
    "formal",
    "old_money",     # "Quiet Luxury"
    "streetwear",
    "minimal",
    "athleisure",    # Gym-to-street (Huge in 2026)
    "gorpcore",      # Technical/Outdoor (Arc'teryx, Patagonia style)
    "vintage"        # Retro/Thrifted vibe
]

OCCASIONS = [
    "university",
    "business",
    "date",
    "party",
    "gym",           # Added
    "travel",        # Added (Airport fits are a big category)
    "club",          # Added (Distinct from "party")
    "lounge"         # Added (Home/Grocery run)
]

TEMPERATURE = [
    "freezing",      # Needs heavy layering
    "cold",
    "mild",
    "warm",
    "hot"
]

CATEGORIES = [
    "shirt",
    "pants",
    "shoes",
    "outerwear"      # Renamed from 'jacket' to be more inclusive
]

# Subtypes per category (The biggest update)
SUBTYPES = {
    "shirt": [
        "tee", "graphic_tee", "long_sleeve", # Casual
        "polo", "henley", "oxford", "dress_shirt", # Smart
        "flannel", "overshirt", # Layers
        "hoodie", "sweatshirt", "sweater", "turtleneck", "cardigan" # Knits/Fleece
    ],
    "pants": [
        "jeans", "chinos", "trousers", "pleated_trousers", # Standard
        "shorts", "swim_shorts", # Summer
        "cargos", "carpenter_pants", # Streetwear/Workwear
        "sweatpants", "joggers", "track_pants" # Athleisure
    ],
    "shoes": [
        "sneakers", "chunky_sneakers", "running_shoes", # Athletic
        "loafers", "boots", "chelsea_boots", "derbies", # Smart/Boots
        "slides", "sandals" # Summer
    ],
    "outerwear": [
        "none",
        "blazer", "suit_jacket", # Formal
        "denim_jacket", "bomber", "varsity_jacket", # Casual light
        "leather_jacket", "gilet", # Vests
        "trench", "overcoat", "peacoat", # Smart heavy
        "puffer", "parka", "windbreaker" # Technical/Cold
    ]
}

FITS = [
    "skinny",       # Still exists for some
    "slim",
    "regular",
    "relaxed",
    "oversized",
    "cropped"       # Trendy fit for pants/jackets
]

MATERIALS = [
    "cotton", "heavy_cotton",
    "wool", "merino", "cashmere",
    "linen",
    "denim",
    "leather", "suede",
    "polyester", "nylon", "goretex", # Tech/Gorpcore materials
    "corduroy", "velvet",
    "silk", "viscose"
]

# Helper aliases for the logic engine
OUTERWEAR = SUBTYPES["outerwear"]