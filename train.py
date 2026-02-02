import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import os

from dataset import OutfitDataset
from model.net import OutfitNet
from utils import INPUT_DIM

def train():
    # --- CONFIGURATION ---
    DATA_PATH = "data/expert_data_2026.csv"
    MODEL_PATH = "model/outfit_model.pth"
    BATCH_SIZE = 64        # Larger batch size for larger dataset
    LEARNING_RATE = 0.0005 # Lower LR for stability with deep networks
    EPOCHS = 30            # Enough time to learn complex rules
    
    # 1. Check for Data
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        print("Please run 'python data/generate_expert_data.py' first to create the training data.")
        return

    # 2. Setup Device (Mac Metal / Nvidia CUDA / CPU)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print(">>> Using Mac MPS (Metal Performance Shaders) acceleration.")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print(">>> Using Nvidia CUDA acceleration.")
    else:
        device = torch.device("cpu")
        print(">>> Using CPU (No acceleration detected).")

    # 3. Load & Split Data
    print(f"Loading dataset from {DATA_PATH}...")
    full_dataset = OutfitDataset(DATA_PATH)
    
    # 80% Training (Learn), 20% Validation (Test)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"Data ready: {len(train_dataset)} training samples, {len(val_dataset)} validation samples.")

    # 4. Initialize Network
    model = OutfitNet(input_dim=INPUT_DIM).to(device)
    
    # Loss function: MSE is great for "Scoring" (0.0 to 1.0)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 5. Training Loop
    best_val_loss = float('inf')
    os.makedirs("model", exist_ok=True)

    print("\n--- Starting Training ---")
    for epoch in range(EPOCHS):
        # A. Training Phase
        model.train()
        train_loss = 0.0
        
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        avg_train = train_loss / len(train_loader)

        # B. Validation Phase (No Grad)
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
        
        avg_val = val_loss / len(val_loader)

        # C. Logging
        print(f"Epoch {epoch+1:02d}/{EPOCHS} | Train Loss: {avg_train:.5f} | Val Loss: {avg_val:.5f}")

        # D. Smart Save (Only save if we improved)
        if avg_val < best_val_loss:
            best_val_loss = avg_val
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"    ⭐ New Best Model Saved! (Loss: {best_val_loss:.5f})")

    print("\n--- Training Complete ---")
    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train()