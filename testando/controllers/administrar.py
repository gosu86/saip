from tg                         import expose, validate
from repoze.what.predicates     import All,not_anonymous,has_any_permission

from formencode     import validators

from testando.model                 import DBSession
from testando.model.auth            import Usuario, Rol, Permiso
from testando.model.proyecto        import Proyecto

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
        """
        Muestra la pagina index con el menu para el modulo 'Administrar'
        """
        return dict(page='Administrar')
            
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose("json")
    def lista_de_usuarios(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
            Provee la lista de usuarios existentes en el sistema. Sin discriminar su estado
        """
        offset = (int(page)-1) * int(rp)
        if (query):
            usuarios = DBSession.query(Usuario)
            if qtype=='name':
                usuarios = usuarios.filter(Usuario.name.like('%'+query+'%'))
            elif qtype=='apellido':
                usuarios = usuarios.filter(Usuario.apellido.like('%'+query+'%'))
            elif qtype=='email':
                usuarios = usuarios.filter(Usuario.email.like('%'+query+'%'))
            elif qtype=='estado':
                usuarios = usuarios.filter(Usuario.estado.like('%'+query+'%'))
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
        return dict(page=page, total=total, rows=rows)

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_roles(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
            Provee la lista de roles disponibles en el sistema.
        """        
        offset = (int(page)-1) * int(rp)
        if (query):
            roles = DBSession.query(Rol)
            if qtype=='name':
                roles = roles.filter(Rol.name.like('%'+query+'%'))
        else:
            roles = DBSession.query(Rol)           
        total = roles.count()
        column = getattr(Rol, sortname)
        roles = roles.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
        rows = [{'id'  : rol.id,
                'cell': [rol.id,
                         rol.name,
                        (', </br>'.join([p.permiso_name for p in rol.permisos]))
                        ]} for rol in roles
                ]
        result = dict(page=page, total=total, rows=rows)
        return result    
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_permisos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
            Provee la lista de permisos disponibles en el sistema.
        """                
        try:    
            offset = (int(page)-1) * int(rp)
            if (query):
                permisos = DBSession.query(Permiso)
                if qtype=='name':
                    permisos = permisos.filter(Permiso.permiso_name.like('%'+query+'%'))                
            else:
                permisos = DBSession.query(Permiso)
            total = permisos.count()
            column = getattr(Permiso, sortname)
            permisos = permisos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            rows = [{'id'  : permiso.id,
                    'cell': [permiso.id,
                            permiso.permiso_name,
                            permiso.descripcion,
                            (', </br> '.join([r.name for r in permiso.roles]))
                            ]} for permiso in permisos
                    ]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
            Provee la lista de proyectos existentes en el sistema.
        """                
        try:
            offset = (int(page)-1) * int(rp)
            if (query):
                proyectos = DBSession.query(Proyecto)
                if qtype=='name':
                    proyectos = proyectos.filter(Proyecto.name.like('%'+query+'%'))
                elif qtype == 'lider':
                    lideres =  DBSession.query(Usuario).filter(Usuario.name.like('%'+query+'%')).all()
                    proyectos = []
                    for l in lideres:
                        proyectos.extend(l.mis_proyectos)       
            else:
                proyectos = DBSession.query(Proyecto)
                
            if qtype == 'lider':
                total = len(proyectos)  
            else:
                total = proyectos.count()
                column = getattr(Proyecto, sortname)
                proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp) 
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