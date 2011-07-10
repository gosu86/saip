from tg             import expose,redirect, validate,tmpl_context, request,config,url
from formencode        import validators
from repoze.what.predicates import All,not_anonymous,in_any_group

from sqlalchemy.sql import and_,or_


from testando.model                 import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.fase            import Fase,usuario_rol_fase_table
from testando.model.auth            import Usuario
from testando.model.auth            import Rol
from testando.model.tipoitem        import TipoItem
from testando.model.item            import Item
from testando.model.lineabase       import LineaBase
from testando.model.atributoextra   import AtributoExtra
from testando.model.adjunto         import Adjunto

from testando.lib.base                  import BaseController
from testando.controllers.error         import ErrorController
from testando.controllers.proyectos     import ProyectosController
from testando.controllers.fases         import FasesController
from testando.controllers.tiposDeItem   import TiposDeItemController
from testando.controllers.usuarios      import UsuariosController
from testando.controllers.items         import ItemsController
#from testando.controllers.lineasBase   import LineasBaseController

from testando.widgets.myWidgets     import hideMe

from string import find

import logging
from sqlalchemy.sql.functions import current_user
log = logging.getLogger(__name__)

__all__ = ['ConfigurarController']
class ConfigurarController(BaseController):
    log.debug('<-- In to: ConfigurarController -->')
    allow_only = All(
                     not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!.'),
                     in_any_group('Administradores','Configuradores',
                                  msg='Solo usuarios con los roles "Adminstrador" y/o "Configurador" pueden acceder a esta seccion!')
                     )
    proyectos=ProyectosController(DBSession)
    fases=FasesController(DBSession)
    tiposDeItem=TiposDeItemController(DBSession)
    usuarios=UsuariosController(DBSession)
    items=ItemsController(DBSession)
    error = ErrorController() 
    
    @expose('testando.templates.configurar.index')    
    def index(self, **kw):
        #return dict(page='Configurar')
        redirect('seleccion_de_proyectos')

    @expose('testando.templates.configurar.seleccion_de_proyectos')    
    def seleccion_de_proyectos(self,**kw):
        return dict(page='Configurar')
             
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose("json")
    def lista_de_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            if (sortname=='fases') or (sortname=='usuarios'):
                sortname='name'
            current_user=request.identity['user']
            offset = (int(page)-1) * int(rp)
            if (query):
                d={'lider_id':current_user.id}
                proyectos = DBSession.query(Proyecto).filter(Proyecto.estado!='Eliminado').filter_by(**d)
                if qtype=='name':
                    proyectos=proyectos.filter(Proyecto.name.like('%'+query+'%'))
                elif qtype=='estado':
                    proyectos=proyectos.filter(Proyecto.estado.like('%'+query+'%'))
                elif qtype=='empresa':
                    proyectos=proyectos.filter(Proyecto.empresa.like('%'+query+'%'))
            else:
                proyectos = DBSession.query(Proyecto).filter(and_(Proyecto.estado!='Eliminado',Proyecto.lider_id==current_user.id))
                
            total = proyectos.count()
            column = getattr(Proyecto, sortname)
            proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : proyecto.id,
                    'cell': [proyecto.id,
                            proyecto.name,
                            proyecto.empresa,
                            proyecto.estado,
                            (proyecto.tiene_fases()),
                            (proyecto.tiene_usuarios())]} for proyecto in proyectos]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @expose('json')    
    @expose('testando.templates.configurar.proyectos.vista_de_fases') 
    def vista_de_fases(self,*args, **kw):
        pid=int(kw['pid'])
        p=DBSession.query(Proyecto).filter_by(id=pid).first()
        estado=p.estado
        nombre=p.name
        tmpl_context.proyectoId = hideMe()
        tmpl_context.proyectoNombre = hideMe()
        
        referer=url('/configurar/seleccion_de_proyectos/')
        
        if estado=='Iniciado':
            iniciado=True
        else:
            iniciado=False
        return dict(page='Configurar', proyectoId=pid, iniciado=iniciado,proyectoNombre=nombre,referer=referer,title_nav='Lista de Proyectos')
    

    
    def get_usuarios(self,usuarios,fid,offset,rp):
        """
        Devuelve los usuarioa que no pertenecen a la fase seleccionada.
        @param usuarios: conjunto de usuarios
        @param fid: id de la fase a la que no tiene que pertenecer.: 
        """
        u=[]
        id=int(fid)
        cant=0
        off=0
        for usuario in usuarios:
            if off < offset:
                log.debug('continue')
            else:
                noEsta = True
                for fase in usuario.fases:
                    if fase.id == id:
                        noEsta = False
                if noEsta:
                    cant=cant+1
                    u.append(usuario)
                if cant==rp:
                    break
            off=off+1
        return u
    


    @expose('json')    
    @expose('testando.templates.configurar.fases.vista_de_usuarios') 
    def vista_de_usuarios(self,*args, **kw):
        """
        Muestra la pagina vista_de_usuarios.html
        """
        fid=int(kw['fid'])
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        value=str(f.proyecto_id)
        #log.debug('__________%s' %value)
        referer='/configurar/vista_de_fases/?pid='+ value
        return dict(page='Configurar', faseId=fid,faseNombre=nombre,referer=referer,title_nav='Lista de Fases')

         
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def usuarios_del_sistema(self, fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
        Devuelve la lista de los usuarios del sistema, filtrando los que ya pertenecen a la fase en configuracion.
        """
        try:
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                usuarios = DBSession.query(Usuario).filter_by(**d)
            else:
                usuarios = DBSession.query(Usuario)
                
               
            if fid:
                
                column = getattr(Usuario, sortname)
                usuarios = usuarios.order_by(getattr(column,sortorder)())                
                u=self.get_usuarios(usuarios,fid,offset,rp)
                total = usuarios.count()
                usuarios=u
            else:
                total = usuarios.count() 
                column = getattr(Usuario, sortname)
                usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
                  
            rows = [{'id'  : usuario.id,
                    'cell': [usuario.id,
                             usuario.name,
                             usuario.roles_select()]} for usuario in usuarios
                    ]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
                
    @expose('json')    
    @expose('testando.templates.configurar.fases.vista_de_tiposDeItem') 
    def vista_de_tiposDeItem(self,*args, **kw):
        fid=kw['fid']
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name        
        estado=f.estado
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        if estado!='Inicial':
            iniciado=True
        else:
            iniciado=False
        referer=url('/configurar/vista_de_fases/?pid='+str(f.proyecto.id))
        return dict(page='Configurar', faseId=fid,faseNombre=nombre,iniciado=iniciado,referer=referer,title_nav='Lista de Fases')        
        
    
    def get_tiposDeItem(self,tiposDeItem,fid,offset,rp):
        tdi=[]
        id=int(fid)
        cant=0
        off=0
        for tipoDeItem in tiposDeItem:
            if off < offset:
                log.debug('continue')
            elif tipoDeItem.fase_id != id:
                    cant=cant+1
                    tdi.append(tipoDeItem)
                    if cant==rp:
                        break
            off=off+1
        return tdi
        
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def tiposDeItem_del_sistema(self, fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """Devuelve la lista de tipos de items existente en el sistema filtrando los tipos de item de una fase seleccionada """
        try:
            fid=int(fid)
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                if qtype == 'name':
                    tiposDeItem = DBSession.query(TipoItem).filter(and_(TipoItem.fase_id!=fid,TipoItem.name.like('%'+query+'%')))
                elif qtype == 'codigo':
                    tiposDeItem = DBSession.query(TipoItem).filter(and_(TipoItem.fase_id!=fid,TipoItem.codigo.like('%'+query+'%')))
                else:
                    tiposDeItem = DBSession.query(TipoItem).filter(TipoItem.fase_id!=fid).filter_by(**d)
            else:
                tiposDeItem = DBSession.query(TipoItem).filter(TipoItem.fase_id!=fid)
            
            total = tiposDeItem.count() 
            column = getattr(TipoItem, sortname)
            tiposDeItem = tiposDeItem.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            rows = [{'id'  : tipoDeItem.id,
                    'cell': [tipoDeItem.id,
                             tipoDeItem.codigo,
                             tipoDeItem.name,
                             tipoDeItem.descripcion,
                             tipoDeItem.complejidad,
                             (', </br>'.join([(ce.name+': '+ce.tipo) for ce in tipoDeItem.campos_extra])),
                             tipoDeItem.fase.name,
                             tipoDeItem.fase.proyecto.name]
                             } for tipoDeItem in tiposDeItem ]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result        
        

    @expose('json')
    def cambiar_roles(self,**kw):
        idsyroles    =    kw['idsyroles']
        idsyroles    =    idsyroles.split(";")
        
        f_id    =    idsyroles[0]
        idsyroles.remove(f_id)
        idsyroles.pop()
        
        cantidad    =    len(idsyroles)
        
        f_id    =    int(f_id)
        conn = config['pylons.app_globals'].sa_engine.connect()
        for idyrol in idsyroles:
            idyrol=idyrol.split(',')
            u_id = int(idyrol[0])
            rol = int(idyrol[1])
            updt=usuario_rol_fase_table.update().where(and_(usuario_rol_fase_table.c.usuario_id==u_id, usuario_rol_fase_table.c.fases_id==f_id)).values(rol_id=rol)
            conn.execute(updt)
        conn.close()
                    
        msg    =    str(cantidad)    +    " roles cambiados con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)
        
    @expose('json')    
    @expose('testando.templates.configurar.fases.vista_de_items') 
    def vista_de_items(self,*args, **kw):
        referer=request.headers.get("Referer", "")        
                
        if find(referer,'configurar') >=0:
            page='Configurar'
            title_nav='Lista de items'
        else:
            page='Desarrollar'
            title_nav='Desarrollo de fases'
            
        fid=kw['fid']
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name        
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()

        return dict(page=page, faseId=fid,faseNombre=nombre, referer=referer,title_nav=title_nav )    
            
 
    @expose('testando.templates.configurar.fases.vista_de_lineasbase') 
    def vista_de_lineasbase(self,*args, **kw):
        fid=kw['fid']
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name        
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        value=str(f.proyecto_id)
        referer='/configurar/vista_de_fases/?pid='+ value
        return dict(page='Configurar', faseId=fid,faseNombre=nombre, referer=referer,title_nav='Lista de Fases' )    
                
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def lineas_base(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query,'fase_id':int(fid)}
                lineasBase = DBSession.query(LineaBase).filter_by(**d)
                lineasBase = lineasBase.filter(LineaBase.estado!='Inactiva')
            else:
                d = {'fase_id':int(fid)}
                lineasBase = DBSession.query(LineaBase).filter_by(**d)
                lineasBase = lineasBase.filter(LineaBase.estado!='Inactiva')
                
            total = lineasBase.count()
            log.debug('total lineas base %s' %total)
            column = getattr(LineaBase, sortname)
            lineasBase = lineasBase.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            total = lineasBase.count()
            log.debug('total lineas base 2 %s' %total)            
            rows = [{'id'  : lineaBase.id,
                    'cell': [lineaBase.id,
                            lineaBase.fecha_creacion,
                            lineaBase.estado,
                            len(lineaBase.items)
                            ]} for lineaBase in lineasBase]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result          
      
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def items_aprobados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            items = DBSession.query(Item)            
            if (query):
                if qtype=='name':
                    items   =   items.filter(Item.name.like('%'+query+'%'))
                elif qtype=='estado':
                    items   =   items.filter(Item.estado.like('%'+query+'%'))
                elif qtype=='codigo':
                    items   =   items.filter(Item.codigo.like('%'+query+'%'))
                                    
            d = {'fase_id':int(fid)}
            items = DBSession.query(Item).filter_by(**d)
                
            items = items.filter(and_(
                                      Item.historico==False,
                                      Item.estado=='Aprobado',
                                      or_(
                                          Item.linea_base.has(estado='Abierta'),
                                          Item.linea_base.has(estado='Comprometida'),
                                          Item.linea_base==None
                                          )
                                      )
                                 )
            items = items.filter(Item.estado!='Eliminado') 
                           
            total = items.count()
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            total = items.count()
            rows = [{'id'  : item.id,
                    'cell': [item.id,
                             item.codigo,                             
                            item.name,
                            item.version,
                            str(item.estado),                            
                            item.descripcion,
                            item.complejidad,
                            item.tipo_item.name]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result  
    
    
    @expose('json')        
    def aplicar_linea_base(self,**kw):
        lb=LineaBase()
        ids=kw['ids'].split(',')
        ids.pop()
        cant=len(ids)

        for id in ids:
            id=int(id)
            i=DBSession.query(Item).filter_by(id=id).first()
            lb.items.append(i)        
        lb.fase_id=i.fase_id
        DBSession.flush()
        items = DBSession.query(Item).filter(and_(
                                                  Item.historico==False,
                                                  Item.fase_id==i.fase_id
                                                  )
                                             )
        
        items_con_lba = items.filter(and_(
                                     Item.historico==False,
                                     Item.fase_id==i.fase_id,
                                     Item.linea_base.has(estado='Activa')
                                     )
                                )
        if items_con_lba.count()==items.count():
            i.fase.estado="Con Linea Base"
        else:
            i.fase.estado="Con Lineas Base Parciales"
            
        DBSession.flush()
        msg=str(cant)+' items ahora tienen linea base.'
        type= 'succes'   
            
        return dict(msg=msg,type=type)  

    @expose('json')        
    def abrir_linea_base(self,**kw):
        lb=DBSession.query(LineaBase).filter_by(id=int(kw['id'])).first()
        lb.estado='Abierta'
        lb.fase.estado='Con Lineas Base Parciales'     
        DBSession.flush()
        
        lb.marcar_items()
        msg='Linea base abierta con exito.'
        type= 'succes'   
            
        return dict(msg=msg,type=type)  

    
