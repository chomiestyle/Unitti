from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

def connect_database(param_dic):
    connect = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(param_dic['user'], param_dic['password'], param_dic['host'],param_dic['port'] ,param_dic['database'])
    engine = create_engine(connect,pool_size=50, max_overflow=20,pool_timeout=120)
    return engine


#### Actualizar todas las bases de datos

param_dic = {'host': 'localhost', 'database': 'Email', 'user': 'postgres', 'password': 'sleepy1992', 'port': 5433}

###Aca trabajo con las bases de datos ya creadas y las actualizo cada una

diccionarios=[param_dic]

engine = connect_database(diccionarios[0])
Base = declarative_base()

