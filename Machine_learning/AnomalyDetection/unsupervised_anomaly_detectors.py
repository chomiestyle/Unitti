import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler

#MODEL_SELECTED = 'deepant' # Possible Values ['deepant', 'lstmae']
LOOKBACK_SIZE = 20





def read_modulate_data(data_file):
    """
        Data ingestion : Function to read and formulate the data
    """
    data = pd.read_csv(data_file)
    data.fillna(data.mean(), inplace=True)
    data.set_index("Time", inplace=True)
    #data.index = pd.to_datetime(data.index)
    df = data.copy()
    return data, df



def data_pre_processing(df):
    """
        Data pre-processing : Function to create data for Model
    """
    try:
        scaled_data = MinMaxScaler(feature_range = (0, 1))
        data_scaled_ = scaled_data.fit_transform(df)
        df.loc[:,:] = data_scaled_
        _data_ = df.to_numpy(copy=True)
        X = np.zeros(shape=(df.shape[0]-LOOKBACK_SIZE,LOOKBACK_SIZE,df.shape[1]))
        Y = np.zeros(shape=(df.shape[0]-LOOKBACK_SIZE,df.shape[1]))
        timesteps = []
        for i in range(LOOKBACK_SIZE-1, df.shape[0]-1):
            timesteps.append(df.index[i])
            Y[i-LOOKBACK_SIZE+1] = _data_[i+1]
            for j in range(i-LOOKBACK_SIZE+1, i+1):
                X[i-LOOKBACK_SIZE+1][LOOKBACK_SIZE-1-i+j] = _data_[j]
        return X,Y,timesteps

    except Exception as e:
        print("Error while performing data pre-processing : {0}".format(e))
        return None, None, None


class DeepAnT(torch.nn.Module):
    """
        Model : Class for DeepAnT model
    """

    def __init__(self, LOOKBACK_SIZE, DIMENSION):
        super(DeepAnT, self).__init__()
        self.conv1d_1_layer = torch.nn.Conv1d(in_channels=LOOKBACK_SIZE, out_channels=32, kernel_size=3)
        self.relu_1_layer = torch.nn.ReLU()
        self.maxpooling_1_layer = torch.nn.MaxPool1d(kernel_size=2)
        self.conv1d_2_layer = torch.nn.Conv1d(in_channels=32, out_channels=16, kernel_size=3)
        self.relu_2_layer = torch.nn.ReLU()
        self.maxpooling_2_layer = torch.nn.MaxPool1d(kernel_size=2,)
        self.flatten_layer = torch.nn.Flatten()
        #self.dense_1_layer = torch.nn.Linear(1136, 32)
        self.dense_1_layer = torch.nn.Linear(in_features=1088, out_features=64)
        self.relu_3_layer = torch.nn.ReLU()
        self.dropout_layer = torch.nn.Dropout(p=0.25)
        self.dense_2_layer = torch.nn.Linear(64, DIMENSION)

    def forward(self, x):
        x = self.conv1d_1_layer(x)
        x = self.relu_1_layer(x)
        x = self.maxpooling_1_layer(x)
        x = self.conv1d_2_layer(x)
        x = self.relu_2_layer(x)
        x = self.maxpooling_2_layer(x)
        x = self.flatten_layer(x)
        #print(x.size(1))
        #print(x.size(0))
        x = x.view(x.size(0), -1)

        x = self.dense_1_layer(x)
        x = self.relu_3_layer(x)
        x = self.dropout_layer(x)
        return self.dense_2_layer(x)


class LSTMAE(torch.nn.Module):
    """
        Model : Class for LSTMAE model
    """

    def __init__(self, LOOKBACK_SIZE, DIMENSION):
        super(LSTMAE, self).__init__()
        self.lstm_1_layer = torch.nn.LSTM(DIMENSION, 128, 1)
        self.dropout_1_layer = torch.nn.Dropout(p=0.2)
        self.lstm_2_layer = torch.nn.LSTM(128, 64, 1)
        self.dropout_2_layer = torch.nn.Dropout(p=0.2)
        self.lstm_3_layer = torch.nn.LSTM(64, 64, 1)
        self.dropout_3_layer = torch.nn.Dropout(p=0.2)
        self.lstm_4_layer = torch.nn.LSTM(64, 128, 1)
        self.dropout_4_layer = torch.nn.Dropout(p=0.2)
        self.linear_layer = torch.nn.Linear(128, DIMENSION)

    def forward(self, x):
        x, (_, _) = self.lstm_1_layer(x)
        x = self.dropout_1_layer(x)
        x, (_, _) = self.lstm_2_layer(x)
        x = self.dropout_2_layer(x)
        x, (_, _) = self.lstm_3_layer(x)
        x = self.dropout_3_layer(x)
        x, (_, _) = self.lstm_4_layer(x)
        x = self.dropout_4_layer(x)
        return self.linear_layer(x)




def make_train_step(model, loss_fn, optimizer):
    """
        Computation : Function to make batch size data iterator
    """
    def train_step(x, y):
        model.train()
        yhat = model(x)
        loss = loss_fn(y, yhat)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        return loss.item()
    return train_step

def compute(X,Y,MODEL_SELECTED,num_epoch):
    """
        Computation : Find Anomaly using model based computation
    """
    if str(MODEL_SELECTED) == "lstmae":
        model = LSTMAE(10,26)
        criterion = torch.nn.MSELoss(reduction='mean')
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
        train_data = torch.utils.data.TensorDataset(torch.tensor(X.astype(np.float32)), torch.tensor(X.astype(np.float32)))
        train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=32, shuffle=False)
        train_step = make_train_step(model, criterion, optimizer)
        for epoch in range(num_epoch):
            loss_sum = 0.0
            ctr = 0
            for x_batch, y_batch in train_loader:
                loss_train = train_step(x_batch, y_batch)
                loss_sum += loss_train
                ctr += 1
            print("Training Loss: {0} - Epoch: {1}".format(float(loss_sum/ctr), epoch+1))
        hypothesis = model(torch.tensor(X.astype(np.float32))).detach().numpy()
        loss = np.linalg.norm(hypothesis - X, axis=(1,2))
        return loss.reshape(len(loss),1)
    elif str(MODEL_SELECTED) == "deepant":
        model = DeepAnT(20,281)
        criterion = torch.nn.MSELoss(reduction='mean')
        optimizer = torch.optim.Adam(list(model.parameters()), lr=1e-5)
        train_data = torch.utils.data.TensorDataset(torch.tensor(X.astype(np.float32)), torch.tensor(Y.astype(np.float32)))
        train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=32, shuffle=False)
        train_step = make_train_step(model, criterion, optimizer)
        for epoch in range(num_epoch):
            loss_sum = 0.0
            ctr = 0
            for x_batch, y_batch in train_loader:
                loss_train = train_step(x_batch, y_batch)
                loss_sum += loss_train
                ctr += 1
            print("Training Loss: {0} - Epoch: {1}".format(float(loss_sum/ctr), epoch+1))
        hypothesis = model(torch.tensor(X.astype(np.float32))).detach().numpy()
        loss = np.linalg.norm(hypothesis - Y, axis=1)
        return loss.reshape(len(loss),1)
    else:
        print("Selection of Model is not in the set")
        return None

def compare_compute(folder_path,type_model):
    filename_datadog = 'C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/prueba_metricas2.csv'
    data, _data = read_modulate_data(filename_datadog)
    X, Y, T = data_pre_processing(data)
    for epoch in [1,10,20,30,40,50,60]:
        loss = compute(X, Y,MODEL_SELECTED=type_model,num_epoch=epoch)
        #_data['loss']=loss
        loss_df = pd.DataFrame(loss, columns=["loss"])
        loss_df.index = T
        #loss_df.index = pd.to_datetime(loss_df.index)
        loss_df["timestamp"] = T
        # loss_df["timestamp"] = pd.to_datetime(loss_df["timestamp"])
        loss_df.to_csv(folder_path+'/loss_value_{}_{}.csv'.format(epoch,type_model),index=False)





folder='C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/result_data'
compare_compute(folder_path=folder,type_model='deepant')

#file_name='C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/Canadian_climate_history.csv'


