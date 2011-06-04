from tg             import expose,redirect, validate,flash,tmpl_context
from tg.decorators  import override_template

from tgext.crud     import CrudRestController

from testando.model             import DBSession
from testando.model.fase        import Fase
from testando.model.tipoitem        import TipoItem
from testando.widgets.fase_w    import fase_new_form,fase_edit_filler,fase_edit_form
from testando.widgets.myWidgets import hideMe
from formencode     import validators

import logging

__all__ = ['FasesController']
log = logging.getLogger(__name__)
class FasesController(CrudRestController):
    log.debug('<-- In to FasesController -->')
    model       =   Fase
    new_form    =   fase_new_form
    edit_filler =   fase_edit_filler    
    edit_form   =   fase_edit_form
    
    template=''
    page=''

    @expose()
    def get_all(self,proyecto_Id=''):
        tmpl_context.proyectoId = hideMe()
        override_template(self.get_all,self.template)    
        return dict(page=self.page, proyectoId=proyecto_Id)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_fases(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None,pid=None):
        try:          
            offset = (int(page)-1) * int(rp)
            if (query):
                if pid==None:
                    d = {qtype:query}
                else:
                    d = {qtype:query,'proyecto_id':int(pid)}
                fases = DBSession.query(Fase).filter_by(**d)
            else:
                if pid==None:
                    fases = DBSession.query(Fase)
                else:
                    d = {'proyecto_id':int(pid)}
                    fases = DBSession.query(Fase).filter_by(**d)                
                
            
            total = fases.count()
            column = getattr(Fase, sortname)
            fases = fases.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)    
            rows = [{'id'  : fase.id,
                    'cell': [fase.id,
                             fase.name,
                             fase.estado,
                             fase.orden]} for fase in fases]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @expose('json')    
    @expose('testando.templates.configurar.fases.seleccionarTiposDeItem')
    def seleccionar_tiposDeItem(self, fase_Id,*args, **kw):
        tmpl_context.faseId = hideMe()    
        return dict(page=self.page, faseId=fase_Id)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def tiposDeItem_asignados(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            log.debug('<-- offset: %s -->' %offset)
            log.debug('<-- query: %s -->' %query)
            fase=DBSession.query(Fase).filter(Fase.id==query).first()
            log.debug('<-- fase: %s -->' %fase.name)
            tiposDeItem = fase.tipos_items
  
            log.debug('<-- tiposDeItem: %s -->' %len(tiposDeItem))    
            total = len(tiposDeItem)
            #log.debug('<-- total asignado: %s -->' %total)            
            #column = getattr(TipoItem, sortname)
            #tiposDeItem = tiposDeItem.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : tipoDeItem.id,
                    'cell': [tipoDeItem.id,
                            tipoDeItem.name
                            ]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result    
                    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def tiposDeItem_disponibles(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                tiposDeItem = DBSession.query(TipoItem).filter_by(**d)
            else:
                tiposDeItem = DBSession.query(TipoItem)
            
            total = tiposDeItem.count()
            column = getattr(TipoItem, sortname)
            tiposDeItem = tiposDeItem.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : tipoDeItem.id,
                    'cell': [tipoDeItem.id,
                            tipoDeItem.name
                            ]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result

    @expose('json')
    def asignar_tiposDeItem(self,**kw):
        
        ids    =    kw['ids']
        ids    =    ids.split(",")
        f_id    =    ids[0]
        
        ids.remove(f_id)
        ids.pop()
        
        cantidad    =    len(ids)
        f_id    =    int(f_id)
        fase = DBSession.query(Fase).filter(Fase.id==int(f_id)).first()
        for id in ids:
            tipoDeItem = DBSession.query(TipoItem).filter(TipoItem.id==int(id)).first()
            log.debug(" fase == %s" % (tipoDeItem.name))
            fase.tipos_items.append(tipoDeItem)
            
            DBSession.flush()
        msg    =    str(cantidad)    +    " Tipos de item asignados con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)
    
    @expose('json')
    def liberar_tiposDeItem(self,**kw):
        ids    =    kw['ids']
        ids    =    ids.split(",")
        
        f_id    =    ids[0]
        
        ids.remove(f_id)
        ids.pop()
        
        cantidad    =    len(ids)
        f_id    =    int(f_id)
        fase = DBSession.query(Fase).filter(Fase.id==int(f_id)).first()      
        for id in ids:
            tipoDeItem = DBSession.query(TipoItem).filter(TipoItem.id==int(id)).first()
            fase.tipos_items.remove(tipoDeItem)
            DBSession.flush()
            
        msg    =    str(cantidad)    +    " Tipos de item liberados con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)    
    
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        id = kw['id']
        log.debug("Inside post_fetch: id == %s" % (id))
        if (id != None):
            d = {'id':id}
            fase = DBSession.query(Fase).filter_by(**d).first()            
            nombre=fase.name
            if (fase.estado != 'activo'):
                DBSession.delete(fase)
                DBSession.flush()
                msg="El fase se ha eliminado con exito!."
                type="succes"
            else:
                msg="El fase esta ACTIVA! No se puede eliminar."
                type="error"
        return dict(msg=msg,nombre=nombre,type=type)
       
    @expose()
    def get_one(self, *args, **kw):
        redirect('../')
        