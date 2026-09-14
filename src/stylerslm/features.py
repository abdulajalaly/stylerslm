"""Feature encoding shared by training and inference."""

from .ontology import COLORS, FITS, OCCASIONS, OUTERWEAR, STYLES, SUBTYPES, TEMPERATURE


def one_hot(value, options):
    return [int(value == option) for option in options]


def outfit_to_vector(shirt, pants, shoes, style, shirt_subtype, pants_subtype, shoes_subtype, fit, temperature, occasion, outerwear):
    return (
        one_hot(shirt, COLORS) + one_hot(pants, COLORS) + one_hot(shoes, COLORS)
        + one_hot(style, STYLES) + one_hot(shirt_subtype, SUBTYPES["shirt"])
        + one_hot(pants_subtype, SUBTYPES["pants"]) + one_hot(shoes_subtype, SUBTYPES["shoes"])
        + one_hot(fit, FITS) + one_hot(temperature, TEMPERATURE)
        + one_hot(occasion, OCCASIONS) + one_hot(outerwear, OUTERWEAR)
    )


INPUT_DIM = len(outfit_to_vector("", "", "", "", "", "", "", "", "", "", ""))