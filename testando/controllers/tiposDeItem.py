from tgext.crud import CrudRestController
from testando.model.tipoitem import TipoItem
from testando.widgets.tipoDeItem_w import *
from tg import expose, flash, require, url, request, redirect, validate,tmpl_context
from repoze.what.predicates import not_anonymous
#===============================================================================
# Imports for FlexiGrid Widget
from testando.model import DeclarativeBase, metadata, DBSession
from testando.model.campoextra     import CampoExtra
from tg.decorators import *
from formencode import validators
import logging
from tw.forms import TextField
from string import find, replace
#===============================================================================
log = logging.getLogger(__name__)
class TiposDeItemController(CrudRestController):

    model = TipoItem
    edit_form = tipoitem_edit_form
    edit_filler = tipoitem_edit_filler
    new_form = tipoitem_add_form
    template=''
    page=''
#===============================================================================
#===============================================================================
#    @expose('testando.templates.administrar.tiposDeItem.get_one')
#    def get_one(self, *args, **kw):
# 
#        tmpl_context.form = tipoitem_view_form
#        value = {'name':'nombre'}
#        return dict(value=value)
#===============================================================================
    @expose()
    def get_one(self, *args, **kw):
        redirect('../')
    
    @expose('testando.templates.tipoitem.index')
    def get_all(self):
        override_template(self.get_all,self.template)    
        return dict(page=self.page)
        #return dict()
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def fetch(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            #____________________________________________
            # hacer esto para cada dato del tipo numerico
            if (qtype=="id"):
                id=int(query)
            #_____________________________________________
            
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                tipositems = DBSession.query(TipoItem).filter_by(**d)
            else:
                tipositems = DBSession.query(TipoItem)
            
            total = tipositems.count()
            column = getattr(TipoItem, sortname)
            tipositems = tipositems.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)    
            rows = [{'id'  : tipoitem.id,
                    'cell': [
                             tipoitem.id,
                             tipoitem.name,
                             tipoitem.descripcion,
                             tipoitem.complejidad,
                             (','.join([ce.name for ce in tipoitem.campos_extra]))]
                     } for tipoitem in tipositems]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
#--flexi--flexi--flexi--flexi--flexi--flexi--flexi--flexi--flexi--flexi
#===============================================================================
    
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        id = kw['id']
        log.debug("Inside post_fetch: id == %s" % (id))
        if (id != None):
            d = {'id':id}
            tipoitem = DBSession.query(TipoItem).filter_by(**d).first()            
            nombre=tipoitem.name
            DBSession.delete(tipoitem)
            DBSession.flush()    
            #===================================================================
        return dict(msg=nombre)
            
    @expose()
    def post(self, *args, **kw):       
        ti=self.provider.create(self.model, params=kw)
        keys=kw.keys()
        for key_nombre in keys:
            if find(key_nombre,'nombre') >= 0:
                key_tipo=replace(key_nombre,'nombre','tipo')
                nombre=kw[key_nombre]
                tipo=kw[key_tipo]
                campoExtra=CampoExtra()
                campoExtra.name=nombre
                campoExtra.tipo=tipo
                campoExtra.tipo_item_id=ti.id
                DBSession.add(campoExtra)
                DBSession.flush()        
        raise redirect('./')
