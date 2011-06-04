from tg             import expose,redirect, validate,flash,tmpl_context, request
from formencode        import validators
from repoze.what.predicates import All
from repoze.what.predicates import not_anonymous
from repoze.what.predicates import in_any_group

from testando.model                 import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.fase            import Fase

from testando.lib.base                  import BaseController
from testando.controllers.error         import ErrorController

from testando.controllers.proyectos     import ProyectosController
from testando.controllers.fases         import FasesController
from testando.controllers.tiposDeItem   import TiposDeItemController

from testando.controllers.usuarios      import UsuariosController
from testando.controllers.items         import ItemsController
from testando.widgets.myWidgets     import hideMe
#from testando.controllers.lineasBase    import LineasBaseController

__all__ = ['ConfigurarController']
import logging
log = logging.getLogger(__name__)
class ConfigurarController(BaseController):
    log.debug('<-- In to: ConfigurarController -->')
    allow_only = All(
                     not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!.'),
                     in_any_group('Administrador','Configurador',
                                  msg='Solo usuarios con los roles "Adminstrador" y/o "Configurador" pueden acceder a esta seccion!')
                     )
    
    proyectos=ProyectosController(DBSession)
    proyectos.template='genshi:testando.templates.configurar.proyectos.index'
    proyectos.page='Configurar'
    
    fases=FasesController(DBSession)
    fases.template='genshi:testando.templates.configurar.fases.index'
    fases.page='Configurar'

    tiposDeItems=TiposDeItemController(DBSession)
    tiposDeItems.template='genshi:testando.templates.configurar.tiposDeItems.index'
    tiposDeItems.page='Configurar'
    
    usuarios=UsuariosController(DBSession)
    usuarios.template='genshi:testando.templates.configurar.usuarios.index'
    usuarios.page='Configurar'       
        
    items=ItemsController(DBSession)
    items.template='genshi:testando.templates.configurar.items.index'
    items.page='Configurar'

    #lineasBase=LineasBaseController(DBSession)
    #lineasBase.template='genshi:testando.templates.configurar.lineasBase.index'
    #lineasBase.page='configurar'
 
    error = ErrorController()
    
    @expose('testando.templates.configurar.index')    
    def index(self, **kw):
        return dict(page='Configurar')

    @expose('testando.templates.configurar.seleccion_de_proyectos')    
    def seleccion_de_proyectos(self, tipo=None,**kw):
        log.debug('tipo: %s' %tipo)
        configuracion=False
        fase=False
        lineabase=False
        if tipo == 'configuracion':
            configuracion=True
        elif tipo == 'fases':
            fase=True
        elif tipo == 'lineasbase':
            lineabase=True
        return dict(page='Configurar',conf=configuracion,fases=fase,lineasbase=lineabase)

    def tiene_fases(self,p):
        if len(p.fases) > 0:
            return 'si'
        else:
            return 'no'
        
    def tiene_usuarios(self,p):
        if len(p.usuarios) > 0:
            return 'si'
        else:
            return 'no'
             
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            if (sortname=='fases') or (sortname=='usuarios'):
                sortname='name'
            current_user=request.identity['user']
            offset = (int(page)-1) * int(rp)
            if (query):
                d={qtype:query,'lider_id':current_user.id}
                proyectos = DBSession.query(Proyecto).filter_by(**d)
            else:
                d={'lider_id':current_user.id}
                proyectos = DBSession.query(Proyecto).filter_by(**d)
            
            total = proyectos.count()
            column = getattr(Proyecto, sortname)
            proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)

            
            rows = [{'id'  : proyecto.id,
                    'cell': [proyecto.id,
                            proyecto.name,
                            proyecto.empresa,
                            proyecto.estado,
                            (self.tiene_fases(proyecto)),
                            (self.tiene_usuarios(proyecto))]} for proyecto in proyectos]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def iniciar_proyecto(self,**kw):
        id = kw['id']
        if (id != None):
            d = {'id':id}
            proyecto = DBSession.query(Proyecto).filter_by(**d).first()
            nombre=proyecto.name
            if (proyecto.estado != 'Iniciado'):
                proyecto.estado = 'Iniciado'
                DBSession.flush()
                msg="El proyecto se ha Iniciado."
                type="succes"
            else:
                msg="El proyecto ya se encuentra Iniciado."
                type="notice"
        return dict(msg=msg,nombre=nombre,type=type)    
    
    @expose('json')    
    @expose('testando.templates.configurar.proyectos.asignacion_de_fases') 
    def asignacion_de_fases(self, proyecto_Id,*args, **kw):
        tmpl_context.proyectoId = hideMe()    
        return dict(page='Asignar Fases', proyectoId=proyecto_Id)

    @expose('json')    
    @expose('testando.templates.configurar.proyectos.vista_de_fases') 
    def vista_de_fases(self, proyecto_Id,*args, **kw):
        tmpl_context.proyectoId = hideMe()    
        return dict(page='Vista de Fases', proyectoId=proyecto_Id)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def fases_asignadas(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            fases = DBSession.query(Fase).filter(Fase.proyecto_id==query)
                
            total = fases.count()
            
            column = getattr(Fase, sortname)
            fases = fases.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : fase.id,
                    'cell': [fase.id,
                            fase.name,
                            fase.descripcion,
                            fase.estado,
                            fase.orden]} for fase in fases]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result    
                    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def fases_disponibles(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                fases = DBSession.query(Fase).filter_by(**d)
            else:
                d = {'estado':'inactivo','proyecto_id':None}
                fases = DBSession.query(Fase).filter_by(**d)
            
            total = fases.count()
            column = getattr(Fase, sortname)
            fases = fases.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : fase.id,
                    'cell': [fase.id,
                            fase.name,
                            fase.descripcion,
                            fase.estado,
                            fase.orden]} for fase in fases]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result

    @expose('json')
    def asignar_fases(self,**kw):
        ids    =    kw['ids']
        ids    =    ids.split(",")

        p_id    =    ids[0]
        log.debug(" id == %s" % (p_id))
        ids.remove(p_id)
        ids.pop()
        
        cantidad    =    len(ids)
        
        p_id    =    int(p_id)
        
        for id in ids:
            fase = DBSession.query(Fase).filter(Fase.id==int(id)).first()
            fase.proyecto_id=p_id
            DBSession.flush()
        msg    =    str(cantidad)    +    " fases asignadas con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)
    
    @expose('json')
    def quitar_fases(self,**kw):
        ids    =    kw['ids']
        ids    =    ids.split(",")

        ids.pop()
        cantidad    =    len(ids)
        
        for id in ids:
            fase = DBSession.query(Fase).filter(Fase.id==int(id)).first()
            fase.proyecto_id=None
            DBSession.flush()
            
        msg    =    str(cantidad)    +    " fases liberadas con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)
    