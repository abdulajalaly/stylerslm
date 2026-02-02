import pandas as pd
import torch
from utils import one_hot, outfit_to_vector

class OutfitDataset(torch.utils.data.Dataset):
    def __init__(self, path):
        """path: single CSV path (str) or list of CSV paths to combine."""
        if isinstance(path, (list, tuple)):
            dfs = [pd.read_csv(p) for p in path]
            self.df = pd.concat(dfs, ignore_index=True)
        else:
            self.df = pd.read_csv(path)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        x = outfit_to_vector(
            row.shirt, row.pants, row.shoes,
            row.style,
            row.shirt_subtype, row.pants_subtype, row.shoes_subtype,
            row.fit, row.temperature, row.occasion, row.outerwear
        )
        y = row.score
        return torch.tensor(x, dtype=torch.float32), torch.tensor([y], dtype=torch.float32)
