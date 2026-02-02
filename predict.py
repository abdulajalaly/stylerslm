import torch
import os
from model.net import OutfitNet
from utils import outfit_to_vector, INPUT_DIM

_model = None


def load_model():
    """Load the trained model (loads once and caches)."""
    global _model
    if _model is None:
        model_path = "model/outfit_model.pth"
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                "Please train the model first by running: python train.py"
            )
        _model = OutfitNet(input_dim=INPUT_DIM)
        _model.load_state_dict(torch.load(model_path))
        _model.eval()
    return _model


def predict_outfit(shirt, pants, shoes, style, shirt_subtype, pants_subtype, shoes_subtype, fit, temperature, occasion, outerwear):
    """
    Predict the score for an outfit combination.

    Args:
        shirt, pants, shoes: color strings (from ontology.COLORS)
        style: from ontology.STYLES
        shirt_subtype, pants_subtype, shoes_subtype: from ontology.SUBTYPES
        fit: from ontology.FITS
        temperature: from ontology.TEMPERATURE
        occasion: from ontology.OCCASIONS
        outerwear: from ontology.OUTERWEAR

    Returns:
        float - predicted outfit score
    """
    model = load_model()
    x = outfit_to_vector(
        shirt, pants, shoes, style,
        shirt_subtype, pants_subtype, shoes_subtype,
        fit, temperature, occasion, outerwear
    )
    with torch.no_grad():
        x_tensor = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        pred = model(x_tensor)
        return pred.item()
