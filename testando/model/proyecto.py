# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
from testando.model.fase import Fase


usuario_rol_proyecto_table = Table('usuarios_roles_proyectos', metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('rol_id', Integer),
    Column('proyecto_id', Integer, ForeignKey('proyectos.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

__all__ = ['Proyecto']
class Proyecto(DeclarativeBase):
    __tablename__ = 'proyectos'
    
    #{ Columns
    
    id              =   Column(Integer, primary_key=True)
    
    name            =   Column(Unicode(150), nullable=False)
    
    empresa         =   Column(UnicodeText(128))
    
    descripcion     =   Column(UnicodeText(255))
    
    estado          =   Column(Unicode(20), default='Activo')
    
    fecha_creacion  =   Column(DateTime, default=datetime.now)
    
    #}
    
    #{ Relations
    fases       = relationship(Fase, order_by=Fase.orden, backref="proyecto")
    
    usuarios    = relation('Usuario', secondary=usuario_rol_proyecto_table, backref='proyectos')
    
    lider_id    = Column(Integer, ForeignKey('usuarios.id'))   
    #}    
    
    #{ Special methods

#    def __repr__(self):
#        return ('<Proyecto: nombre=%s>' % self.nombre).encode('utf-8')

 #   def __unicode__(self):
 #       return self.nombre

    #}
