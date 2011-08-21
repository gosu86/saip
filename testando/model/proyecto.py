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


usuario_proyecto_table = Table('usuarios_proyectos', metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
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
    
    fases       = relationship(Fase, order_by=Fase.orden, backref="proyecto")
    
    usuarios    = relation('Usuario', secondary=usuario_proyecto_table, backref='proyectos')
    
    lider_id    = Column(Integer, ForeignKey('usuarios.id'))
    
    def tiene_fases(self):
        c=len(self.fases)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'
        
    def tiene_usuarios(self):
        c=len(self.usuarios)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'
    def es_iniciable(self):
        resp={}
        resp['iniciable']=True
        if self.estado=='Iniciado':
            resp['iniciable']=False
            resp['ya_iniciado']=True
        else:
            if self.tiene_fases()=='no':
                resp['iniciable']=False
                resp['sin_fases']=True
            if self.tiene_usuarios()=='no':
                resp['iniciable']=False
                resp['sin_usuarios']=True
        return resp