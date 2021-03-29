
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

filename_1='C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/result_data/loss_value_10_deepant.csv'
filename_2='C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/prueba_metricas.csv'
def get_data(filename_loss,filename_data, cols=None):
    data_loss=pd.read_csv(filename_loss)

    #print(data_loss)
    for i in data_loss.columns:
        print(i)
    max_index=data_loss['loss'].idxmax()
    print(max_index)
    max_value = data_loss.iloc[max_index]
    print(max_value)
    time=max_value['timestamp']
    data = pd.read_csv(filename_data)

    data.fillna(data.mean(), inplace=True)
    data.set_index("Time", inplace=True)
    #data.index = pd.to_datetime(data.index)
    print(data)
    data_loss['timestamp'] = data_loss['timestamp'].apply(lambda x: datetime.fromtimestamp(x / 1000))
    #data['Time'] = data['Time'].apply(lambda x: datetime.fromtimestamp(x / 1000))
    return data_loss

def visualization(loss_df,n_epochs):
    """
        Visualization
    """
    plt.figure(figsize=(20, 10))
    sns.set_style("darkgrid")
    print(loss_df["loss"])
    ax = sns.distplot(loss_df["loss"], bins=100, label="Frequency")
    ax.set_title("Frequency Distribution | Kernel Density Estimation")
    ax.set(xlabel='Anomaly Confidence Score', ylabel='Frequency (sample)')
    plt.axvline(1.80, color="k", linestyle="--")
    plt.legend()

    plt.figure(figsize=(20, 10))
    ax = sns.lineplot(x="timestamp", y="loss", data=loss_df, color='g', label="Anomaly Score")
    ax.set_title("Anomaly Confidence Score vs Timestamp")
    ax.set(ylabel="Anomaly Confidence Score", xlabel="Timestamp")
    plt.legend()
    plt.show()
    plt.savefig('C:/Users/56979/PycharmProjects/Unitti/Machine_learning/AnomalyDetection/result_data/{}.png'.format(n_epochs), dpi=300)

loss_data=get_data(filename_1,filename_2)
visualization(loss_data,n_epochs=10)