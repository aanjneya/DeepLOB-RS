import torch
from torch.utils.data import DataLoader, Dataset

class LOBDataset(Dataset):
    def __init__(self, df, window_size):
        self.df = df
        self.window_size = window_size
        self.data = torch.tensor(self.df.to_numpy()).float()

    def __len__(self):
        return self.df.height - self.window_size

    def __getitem__(self, idx):
        return self.data[idx:idx+self.window_size]