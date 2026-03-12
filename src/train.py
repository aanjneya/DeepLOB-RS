from torch import nn, optim, device, cuda
from torch.utils.data import Dataset, DataLoader
from model import Model
from dataset import LOBDataset


class Train:
    def __init__(self,df):
        self.loss = None
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.model = Model()
        self.model.to(self.device)
        self.data = LOBDataset(df, window_size=100)
        self.loader = DataLoader(dataset=self.data, batch_size=32)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)


    def train(self, epochs):
        for epoch in range(epochs):
            for x_batch, y_batch in self.loader:
                x_batch, y_batch = x_batch.to(self.device), y_batch.to(self.device)
                self.optimizer.zero_grad()
                y_pred = self.model(x_batch)
                self.loss = self.criterion(y_pred, y_batch)
                self.loss.backward()
                self.optimizer.step()
            print(f"Loss: {self.loss.item()}")