from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

from testando.model.item import Item

import logging
from sqlalchemy.sql.functions import current_user
log = logging.getLogger(__name__)
class LineaBase(DeclarativeBase):
    __tablename__ = 'lineas_bases'

    
    id = Column(Integer, primary_key=True)
       
    fecha_creacion = Column(DateTime, default=datetime.now)

    items = relationship(Item, order_by=Item.id, backref="linea_base") 
    
    estado = Column(Unicode(25),default='Activa')
    
    fase_id         = Column(Integer, ForeignKey('fases.id')) 
 

    def marcar_items(self):
        log.debug('items %s' %self.items)
        for i in self.items:
            i.estado="En Revision"
            for p in i.padres:
                if p.linea_base!=None:
                    if p.linea_base!=self and p.linea_base.estado!='Comprometida':
                        p.linea_base.estado='Comprometida'
                        DBSession.flush()
                        log.debug('padre %s' %p.name)
                        p.linea_base.marcar_items()
            for h in i.hijos:
                if h.linea_base!=None:
                    if h.linea_base!=self and h.linea_base.estado!='Comprometida':
                        h.linea_base.estado='Comprometida'
                        DBSession.flush()
                        log.debug('hijo %s' %h.name)                    
                        h.linea_base.marcar_items()
            for a in i.antecesores:
                if a.linea_base!=None:
                    if a.linea_base!=self and a.linea_base.estado!='Comprometida':
                        a.linea_base.estado='Comprometida'
                        DBSession.flush()
                        log.debug('antecesor %s' %a.name)                    
                        a.linea_base.marcar_items()
            for s in i.sucesores:
                if s.linea_base!=None:
                    if s.linea_base!=self and s.linea_base.estado!='Comprometida':
                        s.linea_base.estado='Comprometida'
                        DBSession.flush()
                        log.debug('sucesor %s' %s.name)                    
                        s.linea_base.marcar_items()  
        DBSession.flush()
        
        
        
        