import torch
from dataset import OutfitDataset
from model.net import OutfitNet
from utils import INPUT_DIM

dataset = OutfitDataset(["data/synthetic.csv", "data/manual.csv"])
loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

model = OutfitNet(input_dim=INPUT_DIM)
optimizer = torch.optim.Adam(model.parameters(),lr=0.001)
loss_fn = torch.nn.MSELoss()

for epoch in range(20):
    total = 0

    for X,y in loader:
        pred = model(X)
        loss = loss_fn(pred,y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total += loss.item()

    print(f"Epoch {epoch}: {total}")

# Save the trained model
torch.save(model.state_dict(), "model/outfit_model.pth")
print("\nModel saved to model/outfit_model.pth")
