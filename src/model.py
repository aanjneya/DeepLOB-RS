from torch import nn

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, (1,2))
        self.conv2 = nn.Conv2d(32, 32, (1,2))
        self.m = nn.LeakyReLU()

    def forward(self, x):
        x = x.unsqueeze(1)
        temp = self.m(self.conv1(x))
        temp = self.m(self.conv2(temp))
        return temp