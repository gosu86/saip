from tg import expose

from repoze.what.predicates import All
from repoze.what.predicates import not_anonymous
from repoze.what.predicates import in_any_group

from testando.model import DBSession

from testando.lib.base                  import BaseController
from testando.controllers.error         import ErrorController
from testando.controllers.usuarios      import UsuariosController
from testando.controllers.proyectos     import ProyectosController
from testando.controllers.fases         import FasesController
from testando.controllers.items         import ItemsController

__all__ = ['DesarrollarController']
import logging
log = logging.getLogger(__name__)
class DesarrollarController(BaseController):
    log.debug('<-- In to: DesarrollarController -->')
    allow_only = All(
                     not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!.'),
                     in_any_group('Administrador','Configurador','Desarrollador',
                                  msg='Solo usuarios con los roles "Adminstrador", "Configurador" y/o "Desarrollador" pueden acceder a esta seccion!')
                    )

    proyectos=ProyectosController(DBSession)
    proyectos.template='genshi:testando.templates.desarrollar.proyectos.index'
    proyectos.page='Desarrollar'
    
    fases=FasesController(DBSession)
    fases.template='genshi:testando.templates.desarrollar.fases.index'
    fases.page='Desarrollar'
    
    items=ItemsController(DBSession)
    items.template='genshi:testando.templates.desarrollar.items.index'
    items.page='Desarrollar'
    
    error = ErrorController()
    @expose('testando.templates.desarrollar.index')
    def index(self):
        return dict(page='Desarrollar')
