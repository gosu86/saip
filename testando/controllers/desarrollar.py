from tg import expose, redirect, validate, request, tmpl_context,config,url
from formencode        import validators

from sqlalchemy.sql import and_, select

from repoze.what.predicates import All,not_anonymous,in_any_group

from testando.model import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.fase            import Fase,usuario_rol_fase_table
from testando.model.auth            import Usuario
from testando.model.tipoitem        import TipoItem
from testando.model.item            import Item

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
    fases=FasesController(DBSession)   
    items=ItemsController(DBSession)

    
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
        
        referer=url('/desarrollar/seleccion_de_proyectos')
        return dict(page='Desarrollar', proyectoId=pid,proyectoNombre=nombre,referer=referer,title_nav='Lista de Proyectos')            

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


    def get_rol(self,uid,fid):
        uid=int(uid)
        fid=int(fid)
        conn = config['pylons.app_globals'].sa_engine.connect()
        se=select([usuario_rol_fase_table.c.rol_id],and_(usuario_rol_fase_table.c.usuario_id==uid, usuario_rol_fase_table.c.fases_id==fid))        
        result=conn.execute(se)
        row=result.fetchone() 
        rol=int(row['rol_id'])

        conn.close()
         
        return rol

    @expose('testando.templates.desarrollar.fases.desarrollo_de_fases') 
    def desarrollo_de_fases(self,fid=None):
        a   =   False
        d   =   False
        ad  =   False
        
        uid =   request.identity['user'].id       
        fid =   int(fid)
        rol =   self.get_rol(uid, fid)
        if rol == 1:
            a   =   True           
        elif rol ==2:
            d   =   True         
        elif rol ==3:
            ad  =   True                
            
        f=DBSession.query(Fase).filter_by(id=fid).one()
        referer=url('/desarrollar/vista_de_fases/?pid='+str(f.proyecto.id))
       
        
        nombre=f.name        
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()        
        return dict(page='Desarrollar',faseId=fid,faseNombre=nombre,A=a,D=d,AD=ad,referer=referer,title_nav='Lista de Fases')

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
                             tipoDeItem.codigo,
                            tipoDeItem.name,
                            tipoDeItem.descripcion,
                            (', </br>'.join([(ce.name+': '+ce.tipo) for ce in tipoDeItem.campos_extra]))]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result    
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def items_creados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {'fase_id':int(fid)}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(Item.historico==False)
                if qtype=='name':
                    items   =   items.filter(Item.name.like('%'+query+'%'))
                elif qtype=='estado':
                    items   =   items.filter(Item.estado.like('%'+query+'%'))
                elif qtype=='codigo':
                    items   =   items.filter(Item.codigo.like('%'+query+'%'))                
                elif qtype=='version':
                    items   =   items.filter_by(version=int(query))
            else:
                d = {'fase_id':int(fid)}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(Item.historico==False)
                
            total = items.count()
            log.debug('total %s' %total)
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : item.id,
                    'cell': [item.id,
                            item.codigo,
                            item.name,
                            item.version,
                            item.estado,
                            item.descripcion,
                            item.complejidad,
                            item.tipo_item.name,
                            item.lineaBase]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result                
            
    @expose('json')        
    def comprometer(self,**kw):
        i=DBSession.query(Item).filter_by(id=int(kw['id'])).first()
        i.linea_base.estado="Comprometida"
        i.linea_base.marcar_items()
        DBSession.flush()
        msg='El item ha pasado al estado de revision.'
        type= 'notice'
        return dict(msg=msg,type=type)      
    
    @expose('json')        
    def aprobar(self,**kw):
        ids=kw['ids'].split(',')
        ids.pop()
        cant=len(ids)
        error=0
        msg=''
        type=''
        cods=''
        for id in ids:
            id=int(id)
            i=DBSession.query(Item).filter_by(id=id).first()
            if i.estado == 'Terminado' or i.estado == 'En Revision':
                i.estado='Aprobado'
            else:
                error=error+1
                cods=cods+i.codigo+','
                
        DBSession.flush()
        
        dif=cant-error
        if dif!=0:
            msg=str(dif)+' items se han aprobado con exito'
            type= 'succes'
        if error!=0:
            error=str(error) +' items ('+cods+') no se han aprobado!'        
            
        return dict(msg=msg,type=type,error=error)        
                
    @expose('json')        
    def terminar(self,**kw):
        ids=kw['ids'].split(',')
        ids.pop()
        cant=len(ids)
        error=0
        msg=''
        type=''
        cods=''        
        for id in ids:
            id=int(id)
            i=DBSession.query(Item).filter_by(id=id).first()
            if i.estado != 'Aprobado':
                i.estado='Terminado'
            else:
                error=error+1
                cods=cods+i.codigo+','
                
        DBSession.flush()
        
        dif=cant-error
        if dif!=0:
            msg=str(dif)+' items se han terminado con exito'
            type= 'succes'
        if error!=0:
            error=str(error) +' items ('+cods+') no han cambiado, tienen estado "Aprobado"!'
        return dict(msg=msg,type=type,error=error)      
    
       
    @expose('json')
    def eliminar_item(self,**kw):        
        item = DBSession.query(Item).filter_by(id = int(kw['id'])).first()
        item.estado='Eliminado'
        item.padres=[]
        item.hijos=[]
        item.antecesores=[]
        item.sucesores=[]
        DBSession.flush()
        msg="El item se ha eliminado."
        return dict(msg=msg)    
    