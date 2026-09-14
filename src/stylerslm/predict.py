"""Model loading and single-outfit inference."""

from pathlib import Path

import torch

from .features import INPUT_DIM, outfit_to_vector
from .model import OutfitNet

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "model" / "outfit_model.pth"
_model = None


def load_model(model_path=DEFAULT_MODEL_PATH):
    global _model
    if _model is None:
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}. Run `python train.py` first.")
        _model = OutfitNet(input_dim=INPUT_DIM)
        _model.load_state_dict(torch.load(model_path, map_location="cpu"))
        _model.eval()
    return _model


def predict_outfit(shirt, pants, shoes, style, shirt_subtype, pants_subtype, shoes_subtype, fit, temperature, occasion, outerwear):
    features = outfit_to_vector(shirt, pants, shoes, style, shirt_subtype, pants_subtype, shoes_subtype, fit, temperature, occasion, outerwear)
    with torch.no_grad():
        return load_model()(torch.tensor(features, dtype=torch.float32).unsqueeze(0)).item()