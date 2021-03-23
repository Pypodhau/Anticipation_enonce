import torch
import torch.nn as nn
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

def parse_window(passengers, window):
    result = []
    data = []
    for i in range(window):
        data = passengers[i*12:(i+1)*12]
        result.append(data)
    return result

def sliding_window(passengers, window):
    X = []
    y = []
    data = []
    i=0
    while(i+window+1<len(passengers)):
        data = passengers[i :i+window]
        X.append(data)
        y.append(passengers[i+window+1])
        i+=1
    return X, y

class Model(nn.Module):
    def __init__(self, input_size=1, hidden_size=256, output_size=1, num_layers=1, seq_length=12, batch_size=1):
        super().__init__()
        input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size
        self.seq_length = seq_length
        self.batch_size = batch_size

        self.lstm1 = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True, bidirectional=False)   #first lstm layer
        #self.lstm2 = nn.LSTM(input_size=hidden_size, hidden_size=hidden_size*2, num_layers=num_layers, batch_first=True, bidirectional=False)    #second lstm layer
        self.fc = nn.Linear(hidden_size, output_size) #linear layer to convert hidden processed data into 1 prediction

    def forward(self, x, device):
        h0_0 = torch.randn(self.num_layers, x.size(0), self.hidden_size).to(device)  #hidden layer random init
        c0_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        x, (hn, cn) = self.lstm1(x, (h0_0, c0_0))
        """
        h0_1 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size*2))
        c0_1 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size*2))
        x, (hn, cn) = self.lstm2(x.view(len(x) ,self.batch_size , -1), (h0_1,c0_1))
        """
        x = self.fc(x)

        return x

######### DATA handling #########

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#import data
flight_data = sns.load_dataset("flights")
# 144 mois de données = 12*12

passengers = flight_data['passengers'].values.astype(float)

scaler = MinMaxScaler(feature_range=(-1, 1))
data_normalized = scaler.fit_transform(passengers.reshape(-1, 1))

X_train, y_train = sliding_window(data_normalized, 12)
test_dataset = parse_window(data_normalized,12)

X_train = torch.FloatTensor(X_train)
y_train = torch.FloatTensor(y_train)

X_train = torch.reshape(X_train, (X_train.shape[0], -1, 1)).to(device)
y_train = torch.reshape(y_train, (y_train.shape[0], 1, 1)).to(device)

######### MODEL #########
#model
model = Model().to(device)
loss_function = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

epochs = 250

for i in range(epochs):
    model.train()
    optimizer.zero_grad()
    y_pred = model(X_train, device).to(device)

    single_loss = loss_function(y_pred, y_train)
    single_loss.backward()
    optimizer.step()
    if i%5 == 1:
        print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

print(f'epoch: {i:3} loss: {single_loss.item():10.10f}')

pred_data = []
real_pred_data = []
pred = model(X_train, device).to(device)

#moving back tensors to CPU to treat tensors as numpy array
pred = pred.cpu()

for p in pred:
    pred_data.append(p.data.numpy())

for p in pred_data:
    real_pred_data.append(scaler.inverse_transform(p)[0][0])

print(real_pred_data)

#hidden_size - the number of LSTM blocks per layer.
#input_size - the number of input features per time-step.
#num_layers - the number of hidden layers.
#number of LSTM blocks = hidden_size * num_layers


#input_dim : (seq_len, batch_size, input_size).#mode batch_first = False
#input_dim : (batch_size, seq_len, input_size).#mode batch_first = True

#seq_len - the number of time steps in each input stream.
#batch - the size of each batch of input sequences.