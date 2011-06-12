from tg import expose, redirect, validate, request, tmpl_context
from formencode        import validators

from sqlalchemy.sql import and_, or_, not_

from repoze.what.predicates import All,not_anonymous,in_any_group

from testando.model import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.fase            import Fase,usuario_rol_fase_table
from testando.model.auth            import Usuario
from testando.model.tipoitem        import TipoItem

from testando.lib.base                  import BaseController
from testando.controllers.error         import ErrorController
from testando.controllers.usuarios      import UsuariosController
from testando.controllers.proyectos     import ProyectosController
from testando.controllers.fases         import FasesController
from testando.controllers.items         import ItemsController

from testando.widgets.myWidgets     import hideMe

__all__ = ['DesarrollarController']
import logging
log = logging.getLogger(__name__)
class DesarrollarController(BaseController):
    log.debug('<-- In to: DesarrollarController -->')
    allow_only = All(
                     not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!.'),
                     in_any_group('Administrador','Configuradores','Desarrolladores',
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
        redirect('seleccion_de_proyectos')
        
    @expose('testando.templates.desarrollar.seleccion_de_proyectos')    
    def seleccion_de_proyectos(self,**kw):
        return dict(page='Desarrollar')
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            if (sortname=='fases') or (sortname=='usuarios'):
                sortname='name'
            current_user=request.identity['user']
            offset = (int(page)-1) * int(rp)
            if (query):
                d={qtype:query}
                proyectos = DBSession.query(Proyecto).filter(and_(Proyecto.usuarios.any(id = current_user.id),Proyecto.estado=='Iniciado')).filter_by(**d)
            else:
                proyectos = DBSession.query(Proyecto).filter(and_(Proyecto.usuarios.any(id = current_user.id),Proyecto.estado=='Iniciado'))
            log.debug('proyectos: %s' %proyectos)
            total = proyectos.count()
            column = getattr(Proyecto, sortname)
            proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)

            rows = [{'id'  : proyecto.id,
                    'cell': [proyecto.id,
                            proyecto.name,
                            proyecto.lider.name,
                            proyecto.descripcion,
                            proyecto.empresa]} for proyecto in proyectos]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result

    @expose('json')    
    @expose('testando.templates.desarrollar.proyectos.vista_de_fases') 
    def vista_de_fases(self,*args, **kw):
        pid=int(kw['pid'])
        p=DBSession.query(Proyecto).filter_by(id=pid).first()
        nombre=p.name
        tmpl_context.proyectoId = hideMe()
        tmpl_context.proyectoNombre = hideMe()

        return dict(page='Desarrollar', proyectoId=pid,proyectoNombre=nombre)            

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def fases_asignadas(self,pid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            current_user    =   request.identity['user']
            offset = (int(page)-1) * int(rp)
            #proyectos = DBSession.query(Proyecto).filter(Proyecto.usuarios.any(id = current_user.id)).filter_by(**d)
            if (query):
                d = {qtype:query,'proyecto_id':int(pid)}
                fases   =   DBSession.query(Fase).filter_by(**d)
                fases   =   fases.filter(Fase.usuarios.any(id = current_user.id))
            else:
                d = {'proyecto_id':int(pid)}
                fases = DBSession.query(Fase).filter_by(**d)
                fases   =   fases.filter(Fase.usuarios.any(id = current_user.id))
                
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
    
    @expose('testando.templates.desarrollar.fases.desarrollo_de_fases') 
    def desarrollo_de_fases(self,fid=None):
        fid=int(fid)
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name        
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()        
        return dict(page='Desarrollar',faseId=fid,faseNombre=nombre)

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def tiposDeItem_asignados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query,'fase_id':int(fid)}
                tiposDeItem = DBSession.query(TipoItem).filter_by(**d)
            else:
                d = {'fase_id':int(fid)}
                tiposDeItem = DBSession.query(TipoItem).filter_by(**d)
                
            total = tiposDeItem.count()
            
            column = getattr(TipoItem, sortname)
            tiposDeItem = tiposDeItem.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : tipoDeItem.id,
                    'cell': [tipoDeItem.id,
                            tipoDeItem.name,
                            tipoDeItem.descripcion,
                            tipoDeItem.complejidad,
                            (', </br>'.join([(ce.name+': '+ce.tipo) for ce in tipoDeItem.campos_extra]))]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result            