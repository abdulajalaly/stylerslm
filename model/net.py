import torch.nn as nn

class OutfitNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        
        # A "Bigger" Network: Deep MLP
        # Structure: Input -> [128 neurons] -> [64 neurons] -> [32 neurons] -> Score
        self.net = nn.Sequential(
            # Layer 1: Expand features to find combinations
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),      # Helps model learn faster
            nn.ReLU(),
            nn.Dropout(0.2),          # Prevents overfitting (ignoring 20% of connections randomly)

            # Layer 2: Compress information
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),

            # Layer 3: Refine logic
            nn.Linear(64, 32),
            nn.ReLU(),

            # Output Layer: Single score (0.0 to 1.0)
            nn.Linear(32, 1),
            nn.Sigmoid()              # Forces output to be between 0 and 1
        )

    def forward(self, x):
        return self.net(x)