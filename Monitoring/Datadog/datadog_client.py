import re
from datadog import initialize, api
import pandas as pd
import time





class DatadogClient:

    def __init__(self, app_key, api_key):
        initialize(app_key=app_key, api_key=api_key)

    def get_series(self, start, end, query):
        """Get time series points.
        Args:
            start (int): Unix timestamp.
            end (int): Unix timestamp.
            query (string): Datadog query.
        """
        j = api.Metric.query(start=start, end=end, query=query)
        if 'errors' in j:
            msg = 'Datadog: %s' % j['errors']
            raise RuntimeError(msg)
        if 'status' in j and j['status'] != 'ok':
            msg = 'Datadog: API status was NOT ok: %s' % j['status']
            raise RuntimeError(msg)

        series = []

        for d in j['series']:
            sre = re.search(',?host:([^,\}]+)', d['scope'])
            host = '*' if sre is None else sre.group(1)

            # p = [ timestamp, value ]
            series += [{'src_metric': d['metric'],
                        'scope': d['scope'],
                        'host': host,
                        'time': int(p[0]),
                        'raw_value': p[1]
                        } for p in d['pointlist']]

        return sorted(series, key=lambda d: d['time'])

    def save_series(self,filename,series):
        df = pd.DataFrame.from_dict(series)
        df.to_csv(filename)

    def extract_datadog_data(start_time, end_time, time_window, save=False, path=''):
        """ DESCRIPTION: This method extract data of metrics from datadog, between the start time and the end time using the time window.
                         Looks for time to ensure that dont surpise 1600 APIs metris in 1 hour.

            INPUT: start_time: time where start the data that is required (UNIX timestamp)
                   end_time: time where ends the data that is required (UNIX timestamp)
                   time_window: window of time for each API request to datadog (int -> seconds)
                   save: use it if you want to save the data to a csv file (bool)
                   path: path for the csv file storage (string)

            RETURN: Pandas dataframe with requested data (pandas dataframe)"""

        querys_number = 0  # Number of queries that have been processes
        max_queries_number = 1600
        storage = pd.DataFrame()
        temporal_storage = pd.DataFrame()
        while (int(start_time) < int(end_time)):  # Loop moving from start_time throught time_window to end_time
            start_time_format = datetime.utcfromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S')
            print(f'From date time: {start_time_format}')
            if querys_number >= max_queries_number:  # Manage of maximum queries per hour of Datadog
                print('Maximum amount of queries reached')
                print('Waiting 1 hour to proceed')
                time.sleep(3600)
                max_queries_number += 1600

            metrics_names = api.Metric.list(from_epoch=start_time)['metrics']
            metrics_names_format = [name + '{*}' for name in
                                    metrics_names]  # Add to all metrics the {*} meaning it will take the mean data from all host
            metrics_names_batchs = [','.join(metrics_names_format[i * 50:(i + 1) * 50]) for i in range((len(
                metrics_names_format) + 50 - 1) // 50)]  # Separete metrics in batchs of 50 because queries cant be for more than 50 metrics and a join for every batch to complete the format of the query

            for metrics_names_batch in metrics_names_batchs:
                querys_number += 1
                print(f'Loading query number {querys_number}...')
                try:  # Try query request and storage in pandas dataframe
                    api_result = api.Metric.query(start=start_time, end=str(int(start_time) + time_window),
                                                  query=metrics_names_batch)
                    temporal_storage['Time'] = np.array(api_result['series'][0]['pointlist'])[:, 0]
                    for i in range(len(api_result['series'])):
                        temporal_storage[api_result['series'][i]['metric']] = np.array(
                            api_result['series'][i]['pointlist'])[:, 1]
                    storage = storage.append(temporal_storage)
                except TypeError as e:
                    print(f'Query error: {e}\nStart time of the query: {start_time_format}')
                except IndexError as e:
                    print(f'Empty data from the query response: {e}\nStart time of the query: {start_time_format}')
                temporal_storage = pd.DataFrame()

            start_time = str(int(start_time) + time_window)

        if save == True:
            storage.to_csv(path)

        return storage



    def post_metric(self, metric, points, host):
        """Post the given points to a specified metric with host information.
        Args:
            metric (str): Destination metric name.
            points (one of belows):
                p value
                (p time, p value)
                [(p_1 time, p_1 value), ..., (p_n time, p_n value)]
            host: Metric source.
        """
        api.Metric.send(metric=metric, points=points, host=host)

    def __get_snapshot(self, start, end, query):
        """Get a snapshot for the given query in the period.
        Args:
            start (int): Unix timestamp.
            end (int): Unix timestamp.
            query (string): Datadog query.
        """
        j = api.Graph.create(metric_query=query, start=start, end=end)
        return j['snapshot_url']



api_key='22cdc02ac429438fc4ecf839eaedeffd'
app_key='c773b07f21514de37dee348537b60de35bee0ef3'

my_example=DatadogClient(api_key=api_key,app_key=app_key)
end = int(time.time())
start = end - (60 * 60 * 24*2)
filename='C:/Users/56979/PycharmProjects/Unitti/Monitoring/Datadog/data/prueba_data.csv'
query='system.cpu.idle{*}'
val=my_example.get_series(start=start,end=end,query=query)
print(val)
my_example.save_series(filename=filename,series=val)