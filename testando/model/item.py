from sqlalchemy         import  Table, ForeignKey, Column
from sqlalchemy.orm     import  relationship, backref,relation
from sqlalchemy.types   import  Integer, Unicode,UnicodeText,Float,DateTime,BOOLEAN

from testando.model import DeclarativeBase, metadata, DBSession
from testando.model.atributoextra import AtributoExtra
from testando.model.adjunto import Adjunto

from datetime import datetime

import logging
from sqlalchemy.sql.functions import current_user
log = logging.getLogger(__name__)

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
        
        
    def nueva_version(self,kw=None,adjunto_id=None):
        self.historico         =   True
        self.linea_base         =   None
        item                =   Item()
        if kw!=None and kw.has_key('name'):
            item.name           =   kw['name']
        else:
            item.name           =   self.name        
        item.fase           =   self.fase
        item.codigo         =   self.codigo
        item.version        =   self.version+ 1
        item.tipo_item      =   self.tipo_item
        
        if kw!=None and kw.has_key('descripcion'):
            item.descripcion           =   kw['descripcion']
        else:
            item.descripcion           =   self.descripcion         

        if kw!=None and kw.has_key('complejidad'):
            item.complejidad           =   kw['complejidad']
        else:
            item.complejidad           =   self.complejidad
                    
        item.historico_id   =   self.historico_id
        
        if kw!=None and kw.has_key('atributos_extra'):
            
            if isinstance(kw['atributos_extra'],unicode):
                kw['atributos_extra']=kw['atributos_extra'].split()
                
            for id in kw['atributos_extra']:
                aeo          =   DBSession.query(AtributoExtra).filter_by(id=int(id)).first()
                aen          =   AtributoExtra()
                aen.valor    =   kw['atributos_extra_'+str(id)]
                aen.campo_extra_id  =   aeo.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
        else:
            for ae in self.atributos_extra:
                aen          =   AtributoExtra()
                aen.valor    =   ae.valor
                aen.campo_extra_id  =   ae.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
           
        if kw!=None and kw.has_key('padres'):
            item.padres=[]
            if isinstance(kw['padres'],unicode):
                kw['padres']=kw['padres'].split()
            for id in kw['padres']:
                log.debug('id %s' %id)
                p=DBSession.query(Item).filter_by(id=int(id)).first()
                item.padres.append(p)
        else:
            if kw!=None and kw.has_key('name'):
                item.padres=[]
            else:
                item.padres=[]             
                for p in self.padres:
                    item.padres.append(p)
                    
        for h in self.hijos:
            item.hijos.append(h)               
               
        if kw!=None and kw.has_key('antecesores'):
            item.antecesores=[]
            if isinstance(kw['antecesores'],unicode):
                kw['antecesores'].split            
            for id in kw['antecesores']:
                a=DBSession.query(Item).filter_by(id=int(id)).first()
                item.antecesores.append(a)
        else:
            if kw!=None and kw.has_key('name'):            
                item.antecesores=[]
            else:
                for a in self.antecesores:
                    item.antecesores.append(a)
        for s in self.sucesores:
            item.sucesores.append(s)        
        
        if adjunto_id==None:
            for a in self.adjuntos:
                adjunto=Adjunto()
                adjunto.name    =   a.name
                adjunto.filecontent =   a.filecontent
                adjunto.item    =   item
                DBSession.add(adjunto)
        else:
            for a in self.adjuntos:
                if adjunto_id!=a.id:
                    adjunto=Adjunto()
                    adjunto.name    =   a.name
                    adjunto.filecontent =   a.filecontent
                    adjunto.item    =   item
                    DBSession.add(adjunto)
                                
        return item         
        
        