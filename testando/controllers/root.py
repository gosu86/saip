from tg import expose, flash, url, request, redirect,validate
from pylons.i18n import ugettext as _
from warnings import warn
        
from testando.lib.base import BaseController
from testando.controllers.error import ErrorController
from testando.controllers.administrar import AdministrarController
from testando.controllers.configurar import ConfigurarController
from testando.controllers.desarrollar import DesarrollarController
from formencode        import validators
from testando.model.auth import Usuario
from testando.model import DBSession
from testando.model.proyecto        import Proyecto
__all__ = ['RootController']
import logging
log = logging.getLogger(__name__)
class RootController(BaseController):
    log.debug('<-- In to: RootController -->')    
    administrar=AdministrarController()
    desarrollar=DesarrollarController()
    configurar=ConfigurarController()
      
    @expose()    
    def index(self, **kw):
        if not request.identity:
            redirect('/login')
        else:
            redirect('/menu')

    @expose('testando.templates.menu')
    def menu(self):
        return dict(page='Menu')

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def mis_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            current_user=request.identity['user']
            lider_id = current_user.id
            if (query):
                d = {qtype:query,'lider_id':lider_id}
                proyectos = DBSession.query(Proyecto).filter_by(**d)
            else:
                d = {'lider_id':lider_id}
                proyectos = DBSession.query(Proyecto).filter_by(**d)                
            
            total = proyectos.count()
            column = getattr(Proyecto, sortname)
            proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            for p in proyectos:
                log.debug("Lider == %s" % (p.lider.name))
            
            rows = [{'id'  : proyecto.id,
                    'cell': [proyecto.id,
                            proyecto.name,
                            proyecto.lider.name,
                            proyecto.descripcion,
                            proyecto.estado,
                            (', '.join([f.name for f in proyecto.fases]))]} for proyecto in proyectos]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
        
    @expose('testando.templates.login')
    def login(self, came_from=url('/menu/')):
        if request.identity:
            redirect('/menu')
        else:            
            """Start the user login."""
            login_counter = request.environ['repoze.who.logins']
            log.debug("login counter: %s",login_counter)
            if login_counter > 0:
                flash(_('Datos ingresados incorrectos, o no existen... Intente de nuevo.'), 'warning')

            return dict(page='Login', login_counter=str(login_counter),
            came_from=came_from)

    @expose()
    def post_login(self, came_from='/menu/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            log.debug("<-- post_login --> login counter: %s",login_counter)
            redirect('/login', came_from=came_from, __logins=login_counter)
            
        current_user=request.identity['user']
        if current_user.estado == 'Eliminado':
            flash(_('Acceso Denegado'), 'warning')
            redirect('/logout_handler')
        else:
            flash(_('Bienvenido, %s!') % current_user.name)
            redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        redirect('/login')
    error = ErrorController()