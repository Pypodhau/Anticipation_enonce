import torch
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, hidden_size=256, nfeatures=1, num_layers=2, output_size=1, dropout=0.3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        self.lstm1 = nn.LSTM(input_size=nfeatures, hidden_size=hidden_size, num_layers=num_layers, batch_first=False, bidirectional=False, dropout=dropout)   #first lstm layer
        self.fc = nn.Linear(hidden_size, output_size) #linear layer to convert hidden processed data into 1 prediction
        self.out = nn.LogSoftmax()

    def forward(self, x, prev_state=None):
        x, prev_state = self.lstm1(x, prev_state)
        x = self.fc(x)
        #x = self.out(x)
        return x, prev_state