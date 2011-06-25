from tg import expose

from tg                         import expose,redirect, validate,tmpl_context
from tg.decorators              import without_trailing_slash
from decorators                 import registered_validate, catch_errors
from tgext.crud                 import CrudRestController
from repoze.what.predicates     import All,not_anonymous,has_any_permission

from testando.model.auth        import Usuario

from repoze.what.predicates import All,not_anonymous,has_any_permission
from formencode     import validators
from testando.model import DBSession

from testando.lib.base                  import BaseController
from testando.controllers.error         import ErrorController
from testando.controllers.proyectos     import ProyectosController
from testando.controllers.fases         import FasesController
from testando.controllers.tiposDeItem   import TiposDeItemController
from testando.controllers.usuarios      import UsuariosController
from testando.controllers.roles         import RolesController
from testando.controllers.permisos      import PermisosController
__all__ = ['AdministrarController']
import logging
log = logging.getLogger(__name__)
class AdministrarController(BaseController):
    log.debug('<-- In to: AdministrarController -->')
    allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!'),
                     has_any_permission('AdministrarTodo',
                                        'AdministrarUsuarios',
                                        'AdministrarRoles',
                                        'AdministrarPermisos',
                                        'AdministrarProyectos',
                                        'AdministrarFases',
                                        'AdministrarTiposDeItem',
                                        msg='Solo usuarios con algun permiso de administracion pueden acceder a esta seccion!'))

    usuarios=UsuariosController(DBSession)
    proyectos=ProyectosController(DBSession)
    roles=RolesController(DBSession)
    permisos=PermisosController(DBSession)    

    error = ErrorController()
    @expose('testando.templates.administrar.index')    
    def index(self, **kw):
        return dict(page='Administrar')
    
    
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose("json")
    def users(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        offset = (int(page)-1) * int(rp)
        if (query):
            d = {qtype:query}
            usuarios = DBSession.query(Usuario).filter_by(**d)
        else:
            usuarios = DBSession.query(Usuario)
        
            total = usuarios.count() 
            log.debug('total %s' %str(total))
            column = getattr(Usuario, sortname)
            usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            log.debug('total %s' %str(total))
                
        rows = [{'id'  : usuario.id,
                'cell': [usuario.id,
                         usuario.name,
                         usuario.apellido,                             
                         usuario.email,
                         usuario.estado]} for usuario in usuarios
                ]
        result = dict(page=page, total=total, rows=rows) 
        log.debug('result %s' %str(result))
        return dict(page=page, total=total, rows=rows)    