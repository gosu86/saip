from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

from testando.model.item import Item


class LineaBase(DeclarativeBase):
    __tablename__ = 'lineas_bases'

    
    id = Column(Integer, primary_key=True)
       
    fecha_creacion = Column(DateTime, default=datetime.now)

    items = relationship(Item, order_by=Item.id, backref="linea_base") 
    
    estado = Column(Unicode(25),default='Activa')
    
    fase_id = Column(Integer)  
 

