from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
from tipoitem import TipoItem


class Adjunto(DeclarativeBase):
    __tablename__ = 'adjuntos'
    
    #{ Columns
    
    id      =   Column(Integer, primary_key=True)
    
    name    =   Column(Unicode(150), nullable=False) 
    #}
    
    #{ Relations
    
    tipo_item_id    =   Column(Integer, ForeignKey('tipos_items.id'))
    #tipo_item (por backref en la relacion "items" en el modelo tipo_item.py)
    
    linea_base_id   =   Column(Integer, ForeignKey('lineas_bases.id'))
    #linea_base (por backref en la relacion "items" en el modelo linea_base.py)
    
    fase_id         =   Column(Integer, ForeignKey('fases.id'))
    
  #  campos_extra    = relationship(CampoExtra, order_by=CampoExtra.id, backref="item")
    
   # adjuntos        = relationship(Adjunto, order_by=Adjunto.id, backref="item")     
    #fase (por backref en la relacion "items" en el modelo fase.py)
    #}    
