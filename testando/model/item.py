from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
#from testando.model.tipoitem import TipoItem
from testando.model.campoextra import CampoExtra

class Item(DeclarativeBase):
    __tablename__ = 'items'
    
    #{ Columns
    id              =   Column(Integer, primary_key=True)
    
    historico_id    =   Column(Integer)
    
    name            =   Column(Unicode(150), nullable=False)
    
    descripcion     =   Column(UnicodeText(255))
    
    fecha_creacion  =   Column(DateTime, default=datetime.now)
       
    complejidad     =   Column(Integer)
        
    version         =   Column(Integer)    
    #}
    
    #{ Relations
    
    tipo_item_id    =   Column(Integer, ForeignKey('tipos_items.id'))
    #tipo_item (por backref en la relacion "items" en el modelo tipo_item.py)
    
    linea_base_id   =   Column(Integer, ForeignKey('lineas_bases.id'))
    #linea_base (por backref en la relacion "items" en el modelo linea_base.py)
    
    fase_id         =   Column(Integer, ForeignKey('fases.id'))

    campos_extra    =   relationship(CampoExtra, order_by=CampoExtra.id, backref="item")

    padre_id        =   Column(Integer, ForeignKey('items.id'))
    padre           =   relationship("Item",
                        primaryjoin=('items.c.id==items.c.padre_id'),
                        remote_side='Item.id',
                        backref=backref("hijos"))    
      
      
    antecesor_id    =   Column(Integer, ForeignKey('items.id'))
    antecesor       =   relationship("Item",
                        primaryjoin=('items.c.id==items.c.antecesor_id'),
                        remote_side='Item.id',
                        backref=backref("sucesores"))    

        
    #adjuntos        = relationship(Adjunto, order_by=Adjunto.id, backref="item")     
    #fase (por backref en la relacion "items" en el modelo fase.py)
    #}    
