import  Robot.Emails.Database.Data_manage_SQLalchemy as db
from sqlalchemy import Column, Integer, String, Float,Table,ForeignKey,REAL, DateTime,TEXT,BOOLEAN
from sqlalchemy.orm import relationship




class Data_Email(db.Base):
    __tablename__ = 'Data_Email'

    id = Column(Integer, primary_key=True)
    date = Column('date', TEXT, nullable=True)
    #datetime=Column('datetime',DateTime,nullable=True)
    text=Column('text',TEXT,nullable=True)
    deliver_to=Column('deliver_to',TEXT,nullable=True)
    reply_to=Column('reply_to',TEXT,nullable=True)

    def __init__(self,text,deliver_to,reply_to,date):
        self.text=text
        self.deliver_to=deliver_to
        self.reply_to=reply_to
        self.date=date

