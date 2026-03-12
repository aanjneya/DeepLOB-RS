import torch
from torch.utils.data import DataLoader, Dataset

class LOBDataset(Dataset):
    def __init__(self, df, window_size):
        self.window_size = window_size

        x_df = df.drop("label")
        self.x_data = torch.tensor(x_df.to_numpy()).float()

        y_df = df.select("label")
        self.y_data = torch.tensor(y_df.to_numpy()).long().squeeze()

    def __len__(self):
        return len(self.x_data) - self.window_size

    def __getitem__(self, idx):
        return self.x_data[idx:idx+self.window_size], self.y_data[idx+self.window_size-1]