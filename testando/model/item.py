from sqlalchemy         import  Table, ForeignKey, Column
from sqlalchemy.orm     import  relationship, backref,relation
from sqlalchemy.types   import  Integer, Unicode,UnicodeText,Float,DateTime,BOOLEAN

from testando.model import DeclarativeBase, metadata, DBSession
from testando.model.atributoextra import AtributoExtra
from testando.model.adjunto import Adjunto

from datetime import datetime

item_padre_table = Table('items_padres', metadata,
    Column('hijo_id', Integer, ForeignKey('items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('padre_id', Integer, ForeignKey('items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

item_antecesor_table = Table('items_antecesores', metadata,
    Column('sucesor_id', Integer, ForeignKey('items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('antecesor_id', Integer, ForeignKey('items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

class Item(DeclarativeBase):
    __tablename__ = 'items'

    id              =   Column(Integer, primary_key=True)
    
    historico_id    =   Column(Integer)
    
    historico       =   Column(BOOLEAN,default=False)
    
    codigo          =   Column(Unicode(25))
    
    estado          =   Column(Unicode(25),default="En Desarrollo")
    
    name            =   Column(Unicode(150), nullable=False)
    
    descripcion     =   Column(UnicodeText(255))
    
    fecha_creacion  =   Column(DateTime, default=datetime.now)
       
    complejidad     =   Column(Integer)
        
    version         =   Column(Integer)    

    tipo_item_id    =   Column(Integer, ForeignKey('tipos_items.id'))
    
    linea_base_id   =   Column(Integer, ForeignKey('lineas_bases.id'))
    
    fase_id         =   Column(Integer, ForeignKey('fases.id'))

    atributos_extra =   relationship(AtributoExtra, order_by=AtributoExtra.id, backref="item")

    padres      = relation('Item',
                           primaryjoin=('items.c.id==items_padres.c.hijo_id'),
                           secondaryjoin=('items_padres.c.padre_id==items.c.id'),
                           secondary=item_padre_table,
                           backref='hijos')
    
    antecesores = relation('Item',
                           primaryjoin=('items.c.id==items_antecesores.c.sucesor_id'),
                           secondaryjoin=('items_antecesores.c.antecesor_id==items.c.id'),
                           secondary=item_antecesor_table,
                           backref='sucesores')

    adjuntos        = relationship(Adjunto, order_by=Adjunto.id, backref="item")
    
    @property
    def lineaBase(self):
        if self.linea_base_id != None:
            return self.linea_base.estado
        else:
            return 'No tiene'
        
        
        
        
        