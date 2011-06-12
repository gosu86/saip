from tg             import expose,redirect, validate,flash,tmpl_context
from tg.decorators  import override_template

from tgext.crud     import CrudRestController

from testando.model         import DBSession
from testando.model.item    import Item
from testando.widgets.item_w import *

from tg.decorators import *
from formencode import validators
from tw.forms import TextField
from string import find, replace
from decorators import registered_validate, register_validators, catch_errors

import logging
from repoze.what.predicates import has_permission, not_anonymous, All
#===============================================================================
log = logging.getLogger(__name__)

class ItemsController(CrudRestController):
    log.debug('<-- In to ProyectosItems -->')
        
    model = Item
    new_form = item_add_form 
    edit_form = item_edit_form
    edit_filler=item_edit_filler
    template=''
    page=''
    
    @expose('testando.templates.desarrollar.items.index')
    def get_all(self):
        override_template(self.get_all,self.template)    
        return dict(page=self.page)

    @without_trailing_slash
    @expose('testando.templates.desarrollar.items.new')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)

    
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
