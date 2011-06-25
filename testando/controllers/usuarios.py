from tg             import expose,redirect, validate,tmpl_context
from tg.decorators  import without_trailing_slash
from decorators import registered_validate, catch_errors
from tgext.crud     import CrudRestController
from repoze.what.predicates import All,not_anonymous,has_any_permission
from testando.model             import DBSession
from testando.model.auth        import Usuario
from testando.widgets.usuario_w import usuario_new_form,usuario_edit_filler,usuario_edit_form

from formencode     import validators

import logging
errors=()
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


    @expose('testando.templates.administrar.usuarios.index')
    def get_all(self):   
        return dict(page="Administrar")


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
    
    @expose('testando.templates.administrar.usuarios.edit')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        
        value['_method'] = 'PUT'
        referer='/administrar/usuarios/'
        return dict(value=value, model=self.model.__name__, pk_count=len(pks), referer=referer, title_nav='Lista de Usuarios')
    
    
    @without_trailing_slash
    @expose('testando.templates.administrar.usuarios.new')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        referer='/administrar/usuarios/'
        return dict(value=kw, model=self.model.__name__, referer=referer, title_nav='Lista de Usuarios')

   
    
    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        #self.provider.create(self.model, params=kw)
        u=Usuario()

        u.name=kw['name']
        u.usuario_name=kw['usuario_name']
        u.email=kw['email']
        u.apellido=kw['apellido']
        u._set_password(kw['_password'])
        
        DBSession.add(u)
        DBSession.flush()        
        raise redirect('./')
    
    @expose()
    def put(self, *args, **kw):
        """update"""
        id=kw['name']
        log.debug('id: %s' %id )
        log.debug('ARGS: %s' %str(args))
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]
        d={'id':kw[pk]}
        u=DBSession.query(Usuario).filter_by(**d).first()
        log.debug('usuario.name: %s' %u.name )
        u=DBSession.query(Usuario).filter_by(**d).first()
        log.debug('usuario.name: %s' %u.name )
        u.name=kw['name']
        u.usuario_name=kw['usuario_name']
        u.email=kw['email']
        u.apellido=kw['apellido']
        u.estado=kw['estado']
        pas=len(kw['password'])
        if(pas!=0):
            u._set_password(kw['_password'])
        
        
        DBSession.flush()
        u.email=kw['email']
        u.empresa=kw['apellido']
        u.estado=kw['estado']
        pas=len(kw['password'])
        log.debug('pass: %s' %pas )
        if(pas>0):
            u._set_password(kw['_password'])
        
        
        DBSession.flush()
        redirect('../' * len(pks))    