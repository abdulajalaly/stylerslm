from ontology import (
    COLORS,
    STYLES,
    OCCASIONS,
    TEMPERATURE,
    SUBTYPES,
    FITS,
    OUTERWEAR,
)

# Feature order for encoding (must match dataset and predict)
def one_hot(value, options):
    return [1 if value == o else 0 for o in options]


def outfit_to_vector(shirt, pants, shoes, style, shirt_subtype, pants_subtype, shoes_subtype, fit, temperature, occasion):
    """Build feature vector in same order as dataset (for predict)."""
    return (
        one_hot(shirt, COLORS) +
        one_hot(pants, COLORS) +
        one_hot(shoes, COLORS) +
        one_hot(style, STYLES) +
        one_hot(shirt_subtype, SUBTYPES["shirt"]) +
        one_hot(pants_subtype, SUBTYPES["pants"]) +
        one_hot(shoes_subtype, SUBTYPES["shoes"]) +
        one_hot(fit, FITS) +
        one_hot(temperature, TEMPERATURE) +
        one_hot(occasion, OCCASIONS)
    )


# Input dimension for the model (must match outfit_to_vector length)
INPUT_DIM = (
    len(COLORS) * 3 +
    len(STYLES) +
    len(SUBTYPES["shirt"]) + len(SUBTYPES["pants"]) + len(SUBTYPES["shoes"]) +
    len(FITS) +
    len(TEMPERATURE) +
    len(OCCASIONS) +
    len(OUTERWEAR)
)
