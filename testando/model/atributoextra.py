from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from testando.model.campoextra import CampoExtra
from datetime import datetime

class AtributoExtra(DeclarativeBase):
    __tablename__ = 'atributos_extras'
    
    id      =   Column(Integer, primary_key=True)
       
    valor   =   Column(Unicode(128))
       
    item_id =   Column(Integer, ForeignKey('items.id'))
    
    campo_extra_id =   Column(Integer, ForeignKey('campos_extra.id'))
    
    campo_extra       = relationship(CampoExtra)