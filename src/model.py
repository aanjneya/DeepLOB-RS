from torch import nn

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, (1,2))
        self.conv2 = nn.Conv2d(32, 32, (1,2))
        self.relu = nn.LeakyReLU()
        self.lstm = nn.LSTM(32*138,64,batch_first=True)
        self.linear = nn.Linear(64,3)

    def forward(self, x):
        x = x.unsqueeze(1)
        ts = self.relu(self.conv1(x))
        ts = self.relu(self.conv2(ts))
        ts = ts.permute([0,2,1,3])
        ts = ts.reshape(ts.shape[0], ts.shape[1], -1)
        lstm_out, _ = self.lstm(ts)
        last_out = lstm_out[:,-1,:]
        state = self.linear(last_out)
        return state