"""PyTorch dataset for outfit CSV files."""

import pandas as pd
import torch

from .features import outfit_to_vector


class OutfitDataset(torch.utils.data.Dataset):
    def __init__(self, path):
        paths = path if isinstance(path, (list, tuple)) else [path]
        self.df = pd.concat([pd.read_csv(item) for item in paths], ignore_index=True)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        row = self.df.iloc[index]
        values = [row[column] for column in ("shirt", "pants", "shoes", "style", "shirt_subtype", "pants_subtype", "shoes_subtype", "fit", "temperature", "occasion", "outerwear")]
        return torch.tensor(outfit_to_vector(*values), dtype=torch.float32), torch.tensor([row.score], dtype=torch.float32)