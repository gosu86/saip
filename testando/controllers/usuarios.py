from tg             import expose,redirect, validate,flash
from tg.decorators  import override_template

from tgext.crud     import CrudRestController

from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model             import DBSession
from testando.model.auth        import Usuario
from testando.widgets.usuario_w import usuario_new_form,usuario_edit_filler,usuario_edit_form

from formencode     import validators

import logging

__all__ = ['UsuariosController']
log = logging.getLogger(__name__)
class UsuariosController(CrudRestController):
    allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!'),
                     has_any_permission('AdministrarTodo',
                                        'AdministrarUsuarios',
                                        msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarUsuarios" acceder a esta seccion!'))       
    model       =   Usuario
    new_form    =   usuario_new_form
    edit_filler =   usuario_edit_filler
    edit_form   =   usuario_edit_form
     
    template    =   ''
    page        =   ''

    @expose('testando.templates.usuario.index')
    def get_all(self):
        override_template(self.get_all,self.template)    
        return dict(page=self.page)
             
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def fetch(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                usuarios = DBSession.query(Usuario).filter_by(**d)
            else:
                usuarios = DBSession.query(Usuario)
            total = usuarios.count()
            column = getattr(Usuario, sortname)
            usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)    
            rows = [{'id'  : usuario.id,
                    'cell': [usuario.id,
                             usuario.name,
                             usuario.apellido,                             
                             usuario.email,
                             usuario.estado]} for usuario in usuarios
                    ]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result

    @expose()
    def get_one(self, *args, **kw):
        redirect('../')
    
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        id = kw['id']
        log.debug("Inside post_fetch: id == %s" % (id))
        if (id != None):
            d = {'id':id}
            u = DBSession.query(Usuario).filter_by(**d).first()
            nombre=u.name
            DBSession.delete(u)
            DBSession.flush()
            msg="El usuario se ha eliminado con exito!."
        return dict(msg=msg,nombre=nombre)