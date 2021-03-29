import  Robot.Emails.Database.Data_manage_SQLalchemy as db
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from Robot.Emails.Database.email_info import *

import datetime
import datetime
import json
import eml_parser
import os

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

def get_email_data(m_path):
    ep = eml_parser.EmlParser()
    ep.decode_email(m_path)
    text=ep.get_raw_body_text(ep.msg)
    date=ep.msg['Date']
    deliver_to=ep.msg.get('Delivered-To')
    reply_to=ep.msg.get('Reply-To')
    #print(text[0][1])
    data_email={'text':text[0][1],'date':date,'deliver_to':deliver_to,'reply_to':reply_to}
    return data_email





## Clase para manejar una base de datos
class Manage_Database():

    def __init__(self):
        self.engine = db.engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = declarative_base()
        # 2 - generate database schema
        self.Base.metadata.create_all(self.engine)

    def add_email_to_database(self, dict):
        print(dict)
        #session=self.Session()
        old_email = self.session.query(Data_Email).filter_by(text=dict['text']).filter_by(date=dict['date']).first()
        #old_email=None
        if old_email==None:
            print('se agrega este mail')
            new_email=Data_Email(text=dict['text'],deliver_to=dict['deliver_to'],reply_to=dict['reply_to'],date=dict['date'])
            self.session.add(new_email)
            self.session.commit()

    def emails_from_directory(self,path_directory):
        listing = os.listdir(path_directory)

        for fle in listing:
            if str.lower(fle[-3:]) == "eml":

                try:
                    mail_path=path_directory + '/' + fle
                    dictionary = get_email_data(m_path=mail_path)
                    self.add_email_to_database(dict=dictionary)
                    print('paso ')
                except:
                    print('Por aca se fue al except')
                    continue

    def close_session(self):
        self.session.close()