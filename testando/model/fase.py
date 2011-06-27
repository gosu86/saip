# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation,relationship, backref
from sqlalchemy import Table, ForeignKey, Column,UniqueConstraint
from sqlalchemy.types import Integer, Unicode
from testando.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

# modelos relacionados
from testando.model.tipoitem import TipoItem
from testando.model.item import Item
from testando.model.auth import Usuario

usuario_rol_fase_table = Table('usuarios_roles_fases', metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('rol_id', Integer,primary_key=True),
    Column('fases_id', Integer, ForeignKey('fases.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

class Fase(DeclarativeBase):
    __tablename__ = 'fases'

    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(150), nullable=False)
    
    descripcion = Column(UnicodeText(255))
    
    estado = Column(Unicode(20), default='Inicial')
    
    orden = Column(SMALLINT)
    
    fecha_creacion = Column(DateTime, default=datetime.now)

    tiposDeItem       = relationship(TipoItem, backref="fase")

    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))

    items = relationship(Item, order_by=Item.id, backref="fase")
    
    usuarios = relation('Usuario', secondary=usuario_rol_fase_table, backref='fases')

    def tiene_usuarios(self):
        c=len(self.usuarios)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'

    def tiene_tiposDeItem(self):
        c=len(self.tiposDeItem)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'
        
    def tiene_items(self):
        c=len(self.items)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'  