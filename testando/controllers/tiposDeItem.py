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
from decorators import registered_validate, register_validators, catch_errors

errors = ()
try:
    from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
    errors =  (IntegrityError, DatabaseError, ProgrammingError)
except ImportError:
    pass
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
        
    @without_trailing_slash
    @expose('testando.templates.administrar.tiposDeItem.new')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)
        
    @expose('testando.templates.administrar.tiposDeItem.index')
    def get_all(self):
        log.debug('get_all -> kw = %s' %str(kw))
        override_template(self.get_all,self.template)    
        return dict(page=self.page)
        #return dict()

    @expose('testando.templates.administrar.tiposDeItem.edit')
    def edit(self, *args, **kw):
        log.debug("len(kw) %s" %len(kw))
        if len(kw)>0:
            override_template(self.edit,'genshi:testando.templates.administrar.tiposDeItem.agregar_attr')
        log.debug('edit -> kw = %s' %str(kw))
        """Display a page to edit the record."""
    #        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        tdi=DBSession.query(TipoItem).filter_by(id=int(kw[pk])).first()
        attr_extra=tdi.campos_extra
        log.debug('attr_extra = %s' %attr_extra)
        value['_method'] = 'PUT'
        log.debug('value = %s' %value)
        return dict(value=value, model="Tipo De Item", attr_extra=attr_extra,pk_count=len(pks))
        
        
    @expose()
    def put(self, *args, **kw):
        """update"""
        log.debug('put -> kw = %s' %str(kw))
        log.debug('ARGS %s' %str(args))
        
        pks = self.provider.get_primary_fields(self.model)
        log.debug('put -> pks = %s' %str(pks))
        
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]
                log.debug('put -> kw[pk] = %s' %str(kw[pk]))
        tdi=DBSession.query(TipoItem).filter_by(id=int(kw[pk])).first()                
        if kw.has_key('name'):                        
            tdi.name=kw['name']
            tdi.descripcion=kw['descripcion']
            tdi.complejidad=kw['complejidad']
        
            attr_ids = kw['attr_to_modify'].split(',')        
            log.debug('attr_to_modify %s' %attr_ids)
            
            if (len(attr_ids)>0  and attr_ids[0] != ''):
                for id in attr_ids:
                    id=int(id)
                    ae=DBSession.query(CampoExtra).filter_by(id=id).first()
                    nombre=kw['attr_nombre['+str(id)+']']
                    tipo=kw['attr_tipo['+str(id)+']']
                    ae.name=nombre
                    ae.tipo=tipo
    
            attr_ids = kw['attr_to_delete'].split(',')
            log.debug('attr_to_delete %s' %attr_ids)
    
            if (len(attr_ids)>0 and attr_ids[0] != ''):
                for id in attr_ids:       
                        id=int(id)
                        ae=DBSession.query(CampoExtra).filter_by(id=id).first()
                        DBSession.delete(ae)
            DBSession.flush()             

        keys=kw.keys()
        for key_nombre in keys:
            if find(key_nombre,'new_attr_nombre') >= 0:
                key_tipo=replace(key_nombre,'new_attr_nombre','new_attr_tipo')
                nombre=kw[key_nombre]
                tipo=kw[key_tipo]
                campoExtra=CampoExtra()
                campoExtra.name=nombre
                campoExtra.tipo=tipo
                campoExtra.tipo_item_id=tdi.id
                DBSession.add(campoExtra)
        DBSession.flush()
                        
        
        estadoFase=tdi.fase.estado
        redirect('/configurar/vista_de_tiposDeItem/?fId='+str(tdi.fase_id)+'&nombre='+tdi.fase.name+'&estado='+estadoFase)
                
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
        if (id != None):
            d = {'id':id}
            tipoitem = DBSession.query(TipoItem).filter_by(**d).first()            
            nombre=tipoitem.name
            DBSession.delete(tipoitem)
            DBSession.flush()    
            msg="El tipo de Item "+nombre+" se ha eliminado con exito!."
            type="succes"
        return dict(msg=msg, type=type)
            
    @expose()
    #@registered_validate(error_handler=new)
    #@catch_errors(errors, error_handler=new)    
    def post(self, *args, **kw):
        log.debug('post -> kw = %s' %str(kw))       
        ti=self.provider.create(self.model, params=kw)
        keys=kw.keys()
        for key_nombre in keys:
            if find(key_nombre,'new_attr_nombre') >= 0:
                key_tipo=replace(key_nombre,'new_attr_nombre','new_attr_tipo')
                nombre=kw[key_nombre]
                tipo=kw[key_tipo]
                campoExtra=CampoExtra()
                campoExtra.name=nombre
                campoExtra.tipo=tipo
                campoExtra.tipo_item_id=ti.id
                DBSession.add(campoExtra)
                DBSession.flush()
        nombreFase=ti.fase.name
        estadoFase=ti.fase.estado
        raise redirect('/configurar/vista_de_tiposDeItem/?fId='+kw['fase_id']+'&nombre='+nombreFase+'&estado='+estadoFase)

