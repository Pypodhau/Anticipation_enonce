import torch
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=256, nfeatures=1, num_layers=2, dropout=0.3):
        super().__init__()
        input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = nfeatures

        self.lstm1 = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True, bidirectional=False, dropout=dropout)   #first lstm layer
        self.fc = nn.Linear(hidden_size, nfeatures) #linear layer to convert hidden processed data into 1 prediction

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.fc(x)
        return x