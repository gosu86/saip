from tgext.crud     import CrudRestController
from tg             import redirect, request
from tg.decorators  import override_template,validate,without_trailing_slash,expose
from sqlalchemy.sql import and_

from testando.model                 import DBSession
from testando.model.item            import Item
from testando.model.tipoitem        import TipoItem
from testando.model.atributoextra   import AtributoExtra

from formencode import validators

import logging

log = logging.getLogger(__name__)
class ItemsController(CrudRestController):
    log.debug('<-- In to ProyectosItems -->')
        
    model = Item
    
    @expose('testando.templates.desarrollar.items.index')
    def get_all(self):
        override_template(self.get_all,self.template)    
        return dict(page=self.page)

    @without_trailing_slash
    @expose('testando.templates.desarrollar.items.new')
    def new(self, *args, **kw):
        
        referer=request.headers.get("Referer", "")
        log.debug("referer == %s" % (referer))
        log.debug('kw %s' %str(kw))
        tdiid=int(kw['tdiid'])
        tdi=DBSession.query(TipoItem).filter_by(id=tdiid).first()
        fase_id=tdi.fase_id
        fase_orden=tdi.fase.orden
        
        cant=len(DBSession.query(Item).filter(and_(Item.fase_id==fase_id,Item.tipo_item_id==tdi.id)).all())
        cod=str(tdi.codigo)
        cod= cod+'-'+str(cant)
        version=1.0
        
        tipo_item_id=tdi.id
        attr_extra=tdi.campos_extra
        posibles_antecesores=False
        if fase_orden > 1:
            posibles_antecesores=DBSession.query(Item).filter(and_(Item.fase_id==1,Item.historico_id==None))
            
        posibles_padres=DBSession.query(Item).filter(and_(Item.fase_id==fase_id,Item.historico_id==None))
        return dict(page="Desarrollar",
                    attr_extra=attr_extra,
                    fase_id=fase_id,
                    fase_orden=fase_orden,
                    tipo_item_id=tipo_item_id,
                    posibles_padres=posibles_padres,
                    posibles_antecesores=posibles_antecesores,
                    referer=referer,
                    title_nav='Desarrollo de fases',
                    codigo=cod,
                    version=version)
    
    @expose()
    def post(self, *args, **kw):
        log.debug('post -> kw = %s' %str(kw))
        
        fid=kw['fase_id']
               
        i=self.provider.create(self.model, params=kw)
        ti=i.tipo_item
        i.fase.estado='En Desarrollo'
        
        for ce in ti.campos_extra:
            ae                  =   AtributoExtra()
            ae.valor            =   kw[str(ce.name)]
            ae.item_id          =   i.id
            ae.campo_extra_id   =   ce.id            
            DBSession.add(ae)            
        DBSession.flush()
        i.historico_id=i.id
        DBSession.flush()  
        raise redirect('/desarrollar/desarrollo_de_fases/?fid='+fid)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_Items(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            #____________________________________________
            # hacer esto para cada dato del tipo numerico
            if (qtype=="id"):
                id=int(query)
            #_____________________________________________
            
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                items = DBSession.query(Item).filter_by(**d)
            else:
                items = DBSession.query(Item)
            
            total = items.count()
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)    
            rows = [{'id'  : item.id,
                    'cell': [item.id, item.name, item.descripcion]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        id = kw['id']
        log.debug("Inside post_fetch: id == %s" % (id))
        if (id != None):
            d = {'id':id}
            item = DBSession.query(Item).filter_by(**d).first()
            nombre=item.name
            DBSession.delete(item)
            DBSession.flush()
            msg="El item se ha eliminado."

        return dict(msg=msg,nombre=nombre)
    
    
    @expose('testando.templates.desarrollar.items.edit')
    def edit(self, *args, **kw):
        referer=request.headers.get("Referer", "")        
        log.debug("len(kw) %s" %len(kw))
        
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]

        i=DBSession.query(Item).filter_by(id=int(kw[pk])).first()

        fase_id=i.fase_id
        fase_orden=i.fase.orden
        
        posibles_antecesores=False
        if fase_orden > 1:
            posibles_antecesores=DBSession.query(Item).filter(and_(Item.fase_id==(fase_orden-1),
                                                                   Item.historico==False)).all()
            
        posibles_padres=DBSession.query(Item).filter(and_(Item.fase_id==fase_id,
                                                          Item.id!=i.id,
                                                          Item.historico==False)).all()

        for h in i.hijos:
            if h in posibles_padres:
                posibles_padres.remove(h)

        
        return dict(page="Desarrollar",
                    posibles_padres=posibles_padres,
                    posibles_antecesores=posibles_antecesores,
                    referer=referer,
                    title_nav='Desarrollo de fases',
                    item=i)
        
        
    @expose()
    def put(self, *args, **kw):
        """update"""
        log.debug('-------- PUTTING --------')
        log.debug('kw-> kw = %s' %str(kw))
        log.debug('ARGS %s' %str(args))
        
        pks = self.provider.get_primary_fields(self.model)
        log.debug('put -> pks = %s' %str(pks))
        
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]
                log.debug('put -> kw[pk] = %s' %str(kw[pk]))            
        
        i                   =   DBSession.query(Item).filter_by(id=int(kw[pk])).first()
        i.historico         =   True
        
        item                =   Item()
        item.name           =   kw['name']
        item.fase           =   i.fase
        item.codigo         =   i.codigo
        item.version        =   i.version+0.1
        item.tipo_item      =   i.tipo_item
        item.descripcion    =   kw['descripcion']
        item.complejidad    =   kw['complejidad']
        item.historico_id   =   i.historico_id
        
        if kw.has_key('atributos_extra'):
            for id in kw['atributos_extra']:
                aeo          =   DBSession.query(AtributoExtra).filter_by(id=int(id)).first()
                aen          =   AtributoExtra()
                aen.valor    =   kw['atributos_extra_'+id]
                aen.campo_extra_id  =   aeo.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
                log.debug('ae = %s' %str(aen))
                log.debug('attr extra valor = %s' %str(kw['atributos_extra_'+id]))
                log.debug('attr extra id = %s' %str(id))
                    
        if kw.has_key('padres'):
            item.padres=[]             
            for id in kw['padres']:
                p=DBSession.query(Item).filter_by(id=int(id)).first()
                item.padres.append(p)
        else:
            item.padres=[]
        
        if kw.has_key('antecesores'):
            item.antecesores=[]             
            for id in kw['antecesores']:
                a=DBSession.query(Item).filter_by(id=int(id)).first()
                item.antecesores.append(a)
        else:
            item.antecesores=[]


        DBSession.flush() 


        redirect('/desarrollar/desarrollo_de_fases/?fid='+str(item.fase_id))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
