from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

class AtributoExtraFecha(DeclarativeBase):
    __tablename__ = 'atributos_extras_fecha'
    
    id      =   Column(Integer, primary_key=True)
    
    name    =   Column(Unicode(150), nullable=False)
    
    valor   =   Column(DateTime)
       
    item_id =   Column(Integer, ForeignKey('items.id'))