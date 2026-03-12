from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from model import Model
from dataset import LOBDataset


class Train:
    def __init__(self,df):
        self.model = Model()
        self.data = LOBDataset(df, window_size=100)
        self.loader = DataLoader(dataset=self.data, batch_size=32)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)



