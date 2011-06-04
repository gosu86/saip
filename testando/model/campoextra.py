from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
#from testando.model.tipoitem import TipoItem


class CampoExtra(DeclarativeBase):
    __tablename__ = 'campos_extras'
    
    #{ Columns
    
    id      =   Column(Integer, primary_key=True)
    
    name    =   Column(Unicode(150), nullable=False)
    
    tipo    =   Column(Unicode(50))
    
    numero  =   Column(Integer)
    
    texto   =   Column(Unicode(255))
    
    fecha   =   Column(DateTime)
    
    #}
    
    #{ Relations
    
    tipo_item_id    =   Column(Integer, ForeignKey('tipos_items.id'))
    #tipo_item (por backref en la relacion "items" en el modelo tipo_item.py)
       
    item_id         =   Column(Integer, ForeignKey('items.id'))
    
    #fase (por backref en la relacion "items" en el modelo fase.py)
    #}    
