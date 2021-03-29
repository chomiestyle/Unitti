import requests
import json








def get_active_query(url,db):
    alias_db = ["rexmas_prod", "manager_mas_prod"]
    payload = json.dumps({
      "api_id": "get_current_queries",
      "environment": "manager_prodkernel",
      "customer_domain": "prodkernel",
      "domain": "manager",
      "session_id": "023590ad51d6a2ea77bc20aebdfbfca2",
      "alias_db": alias_db[db]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


from datetime import datetime
import pandas as pd
import os

def save_querys(filename,time_max,data):
    pid_array,state_array,query_array=[],[],[]
    new_df=pd.DataFrame(columns=['pid','state','query'])
    for q in data:
        time = q['tiempo']
        datetime_obj = datetime.strptime(time, '%H:%M:%S.%f')
        if datetime_obj>time_max:
            pid=q['pid']
            state=q['state']
            query=q['query']
            pid_array.append(pid)
            state_array.append(state)
            query_array.append(query)

    new_df['pid']=pid_array
    new_df['state']=state_array
    new_df['query']=query_array

    if os.path.isfile(filename):
        print('El archivo existe.')
        old_df=pd.read_csv(filename)
        old_df.append(new_df, ignore_index = True)
        old_df.to_csv(filename)
    else:
        print('El no archivo existe.')
        new_df.to_csv(filename)
def save_text_query(text,filename):
    file1 = open(filename, "w")
    # \n is placed to indicate EOL (End of Line)
    file1.write(text+" \n")
    file1.close()  # to change file access modes



def recolect_per_5min(time_max,filename):
    datetime_obj = datetime.strptime(time_max, '%H:%M:%S.%f')
    print(datetime_obj.time())
    url = "https://351baqjau5.execute-api.us-east-1.amazonaws.com/DEVKERNEL"
    request_text=get_active_query(url=url,db=1)
    print(request_text)
    data=request_text[50:]
    print(data)
    save_text_query(text=data,filename=filename)
    #save_querys(filename=filename,time_max=datetime_obj.time(),data=data)

file='C:/Users/56979/PycharmProjects/Unitti/Monitoring/Datadog/active_query.csv'
file_2='C:/Users/56979/PycharmProjects/Unitti/Monitoring/Datadog/querys.txt'
recolect_per_5min(time_max='00:01:00.0000',filename=file_2)