from tgext.crud import CrudRestController

from tg import redirect,tmpl_context
from tg.decorators import  expose,validate,without_trailing_slash,override_template
from formencode import validators

from testando.widgets.tipoDeItem_w import *

from testando.model import DBSession
from testando.model.campoextra     import CampoExtra
from testando.model.atributoextra import AtributoExtra
from testando.model.tipoitem import TipoItem

from string import find, replace

import logging

log = logging.getLogger(__name__)
class TiposDeItemController(CrudRestController):

    model       =   TipoItem
    new_form    =   tipoitem_add_form
    edit_form   =   tipoitem_edit_form
    edit_filler =   tipoitem_edit_filler

    @expose('testando.templates.administrar.tiposDeItem.index')
    def get_all(self, **kw):
        """Muestra la pagina index.html de tipos de item, en la cual se muestra la lista de tipos de item existentes en el sistema."""
        override_template(self.get_all,self.template)    
        return dict(page=self.page)
        
    @without_trailing_slash
    @expose('testando.templates.administrar.tiposDeItem.new')
    def new(self, *args, **kw):
        """Muestra la pagina new.html con el form para la creacion de un nuevo tipo de item."""
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)

    @expose() 
    def post(self, *args, **kw):
        """ Guarda un tipo de item nuevo en la base de datos """     
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

        raise redirect('/configurar/vista_de_tiposDeItem/?fid='+kw['fase_id'])
        
    @expose('testando.templates.administrar.tiposDeItem.edit')
    def edit(self, *args, **kw):
        """Muestra la pagina edit.html con el form para la edicion de tipo de item seleccionado"""
        if len(kw)>0:
            override_template(self.edit,'genshi:testando.templates.administrar.tiposDeItem.agregar_attr')
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        tdi=DBSession.query(TipoItem).filter_by(id=int(kw[pk])).first()
        attr_extra=tdi.campos_extra
        faseNoIniciada=True
        if len(tdi.fase.items)>0:
            faseNoIniciada=False  
        value['_method'] = 'PUT'

        return dict(value=value,
                    model="Tipo De Item",
                    attr_extra=attr_extra,
                    faseNoIniciada=faseNoIniciada)
             
    @expose()
    def put(self, *args, **kw):
        """Actualiza en la BD los cambios realizados a un tipo de item."""
      
        pks = self.provider.get_primary_fields(self.model)
        
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]

        tdi=DBSession.query(TipoItem).filter_by(id=int(kw[pk])).first()                
        if kw.has_key('name'):                        
            tdi.name=kw['name']
            tdi.descripcion=kw['descripcion']
            tdi.codigo=kw['codigo']
        
            attr_ids = kw['attr_to_modify'].split(',')        
            
            if (len(attr_ids)>0  and attr_ids[0] != ''):
                for id in attr_ids:
                    id=int(id)
                    ae=DBSession.query(CampoExtra).filter_by(id=id).first()
                    nombre=kw['attr_nombre['+str(id)+']']
                    tipo=kw['attr_tipo['+str(id)+']']
                    ae.name=nombre
                    ae.tipo=tipo
    
            attr_ids = kw['attr_to_delete'].split(',')
    
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
                self.actualizar_items(tdi,campoExtra)
        DBSession.flush()

        redirect('/configurar/vista_de_tiposDeItem/?fid='+str(tdi.fase_id))
                
    def actualizar_items(self,tdi,ce):
        """Actualiza los atributos extra de los items que son del tipo de item al cual se le agregaron campos extras."""
        for i in tdi.items:
            ae=AtributoExtra()
            ae.item_id=i.id
            ae.campo_extra_id=ce.id
            DBSession.add(ae)

    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        """Elimina un tipo de item del sistema."""
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