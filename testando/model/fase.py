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
from testando.model.tipoitem import TipoItem
from testando.model.item import Item
from testando.model.auth import Usuario

usuario_rol_fase_table = Table('usuarios_roles_fases', metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('rol_id', Integer, ForeignKey('roles.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('fases_id', Integer, ForeignKey('fases.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

fase_tipoItem_table = Table('fases_tipos_items', metadata,
    Column('fase_id', Integer, ForeignKey('fases.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('tipo_item_id', Integer, ForeignKey('tipos_items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)
class Fase(DeclarativeBase):
    __tablename__ = 'fases'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(150), nullable=False)
    
    descripcion = Column(UnicodeText(255))
    
    estado = Column(Unicode(20), default='inicial')
    
    orden = Column(SMALLINT)
    
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    
    
    #}
    
    #{ Relations
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'))
    #proyecto (por backref en la relacion "fases" en el modelo proyecto.py)
    
    tipos_item = relationship('TipoItem', secondary=fase_tipoItem_table, backref="fases")
    
    items = relationship(Item, order_by=Item.id, backref="fase")
    
    usuarios = relation('Usuario', secondary=usuario_rol_fase_table, backref='fases')   
    #}    
