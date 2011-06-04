from tg import expose

from repoze.what.predicates import All,not_anonymous,has_any_permission

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
    usuarios.template='genshi:testando.templates.administrar.usuarios.index'
    usuarios.page='Administrar'

    roles=RolesController(DBSession)
    roles.template='genshi:testando.templates.administrar.roles.index'
    roles.page='Administrar'

    permisos=PermisosController(DBSession)
    permisos.template='genshi:testando.templates.administrar.permisos.index'
    permisos.page='Administrar'
        
    proyectos=ProyectosController(DBSession)
    proyectos.template='genshi:testando.templates.administrar.proyectos.index'
    proyectos.page='Administrar'
    
    fases=FasesController(DBSession)
    fases.template='genshi:testando.templates.administrar.fases.index'
    fases.page='Administrar'
        
    tiposDeItem=TiposDeItemController(DBSession)
    tiposDeItem.template='genshi:testando.templates.administrar.tiposDeItem.index'
    tiposDeItem.page='Administrar'

    error = ErrorController()
    @expose('testando.templates.administrar.index')    
    def index(self, **kw):
        return dict(page='Administrar')