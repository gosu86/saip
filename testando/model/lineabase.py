from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
from testando.model.item import Item


class LineaBase(DeclarativeBase):
    __tablename__ = 'lineas_bases'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(150), nullable=False)
       
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    #}
    
    #{ Relations
    
    items = relationship(Item, order_by=Item.id, backref="linea_base")   
    
    #}    

