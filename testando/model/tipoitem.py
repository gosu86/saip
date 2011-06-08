from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
from testando.model.item     import Item
from testando.model.campoextra     import CampoExtra

class TipoItem(DeclarativeBase):
    __tablename__ = 'tipos_items'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(150), nullable=False)
    
    descripcion = Column(UnicodeText(255))
    
    fecha_creacion = Column(DateTime, default=datetime.now)
       
    complejidad = Column(Integer)
    
    #}
    
    #{ Relations
    
    #fase (por backref en la relacion "tipos_items" en el modelo fase.py)
    
    fase_id = Column(Integer, ForeignKey('fases.id'))
    
    items           = relationship(Item, order_by=Item.id, backref="tipo_item")
    
    campos_extra    = relationship(CampoExtra, order_by=CampoExtra.id, backref="tipo_item")
    
    #adjuntos        = relationship(Adjunto, order_by=Adjunto.id, backref="tipo_item")   
    #}    
