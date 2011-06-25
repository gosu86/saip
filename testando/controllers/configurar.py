from tg             import expose,redirect, validate,tmpl_context, request,config,url
from formencode        import validators
from repoze.what.predicates import All,not_anonymous,in_any_group

from sqlalchemy.sql import select
from sqlalchemy.sql import and_

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


    #lineasBase=LineasBaseController(DBSession)
    #lineasBase.template='genshi:testando.templates.configurar.lineasBase.index'
    #lineasBase.page='configurar'
 
    error = ErrorController()

    def tiene_fases(self,m):
        c=len(m.fases)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'
        
    def tiene_usuarios(self,m):
        c=len(m.usuarios)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'

    def tiene_tiposDeItem(self,m):
        c=len(m.tiposDeItem)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'
        
    def tiene_items(self,m):
        c=len(m.items)
        if c > 0:
            return 'si ' +'('+str(c)+')' 
        else:
            return 'no'        
    
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
                
            log.debug('query: %s' %proyectos)
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
                f=proyecto.fases[0]
                log.debug('orden %s' % str(f.orden))
                if len(f.usuarios)!=0:
                    proyecto.estado = 'Iniciado'
                    DBSession.flush()
                    msg="El proyecto se ha Iniciado."
                    type="succes"
                else:
                    msg="La primera fase del proyecto no posee usuarios."
                    type="notice"                    
            else:
                msg="El proyecto ya se encuentra Iniciado."
                type="notice"
        return dict(msg=msg,nombre=nombre,type=type)    

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
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def fases_asignadas(self,pid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {'proyecto_id':int(pid)}
                fases = DBSession.query(Fase).filter_by(**d)
                if qtype == 'name':
                    fases=fases.filter(Fase.name.like('%'+query+'%'))
                elif qtype == 'estado':
                    fases=fases.filter(Fase.estado.like('%'+query+'%'))                    
            else:
                d = {'proyecto_id':int(pid)}
                fases = DBSession.query(Fase).filter_by(**d)
                
            total       =   fases.count()
            column      =   getattr(Fase, sortname)
            fases       =   fases.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            
            rows = [{'id'  : fase.id,
                    'cell': [fase.id,
                            fase.name,
                            fase.descripcion,
                            fase.estado,
                            fase.orden,
                            self.tiene_usuarios(fase),
                            self.tiene_tiposDeItem(fase),
                            self.tiene_items(fase)]} for fase in fases]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    def get_usuarios(self,usuarios,fid,offset,rp):
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
    
    def roles_select(self,id,selected=None):

            selectINI='<select id="'+str(id)+'">'
            op1='<option value=1>Aprobador</option>'
            op2='<option value=2>Desarrollador</option>'
            op3='<option value=3>Aprobador y Desarrollador</option>'            
            if selected==1:
                log.debug('1')
                op1='<option value=1 selected="true">Aprobador</option>'
            elif selected==2:
                log.debug('2')
                op2='<option value=2 selected="true">Desarrollador</option>'
                
            elif selected==3:
                log.debug('3')
                op3='<option value=3 selected="true":>Aprobador y Desarrollador</option>'

            selectFIN='</select>'
            select=selectINI+op1+op2+op3+selectFIN
            
            return select

        
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def usuarios_del_sistema(self, fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
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
                             self.roles_select(usuario.id)]} for usuario in usuarios
                    ]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
        
    @expose('json')    
    @expose('testando.templates.configurar.fases.vista_de_usuarios') 
    def vista_de_usuarios(self,*args, **kw):
        fid=int(kw['fid'])
        f=DBSession.query(Fase).filter_by(id=fid).one()
        nombre=f.name
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        value=str(f.proyecto_id)
        #log.debug('__________%s' %value)
        referer='/configurar/vista_de_fases/?pid='+ value
        return dict(page='Configurar', faseId=fid,faseNombre=nombre,referer=referer,title_nav='Lista de Fases')
    
    def get_rol(self,uid,fid):
        uid=int(uid)
        fid=int(fid)
        conn = config['pylons.app_globals'].sa_engine.connect()
        se=select([usuario_rol_fase_table.c.rol_id],and_(usuario_rol_fase_table.c.usuario_id==uid, usuario_rol_fase_table.c.fases_id==fid))
        
        result=conn.execute(se)
        row=result.fetchone() 
        rol=int(row['rol_id'])

        conn.close()
        select_tag=self.roles_select(uid,rol) 
        return select_tag
        
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def usuarios_asignados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query}
                usuarios = DBSession.query(Usuario).filter(Usuario.fases.any(id = fid)).filter_by(**d)

            else:
                d = {'id':int(fid)}
                usuarios = DBSession.query(Usuario).filter(Usuario.fases.any(id = fid))
                
            total = usuarios.count()
            
            column = getattr(Usuario, sortname)
            usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            rows = [{'id'  : u.id,
                    'cell': [u.id,
                            u.name,
                            self.get_rol(u.id,fid),
                            ]} for u in usuarios]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
        
    @expose('json')
    def agregar_usuarios(self,**kw):
        idsyroles    =    kw['idsyroles']
        idsyroles    =    idsyroles.split(";")

        f_id    =    idsyroles[0]
        idsyroles.remove(f_id)
        idsyroles.pop()
        
        current_user=request.identity['user']
        current_user_id =current_user.id
        reload=False
        cantidad    =    len(idsyroles)
        
        f_id    =    int(f_id)
        f=DBSession.query(Fase).filter_by(id=f_id).first()
        p=f.proyecto
        conn = config['pylons.app_globals'].sa_engine.connect()
        for idyrol in idsyroles:
            idyrol=idyrol.split(',')
            u_id = int(idyrol[0])
            if u_id == current_user_id:
                reload=True
            rol = int(idyrol[1])
            ins=usuario_rol_fase_table.insert().values(usuario_id=u_id,rol_id=rol,fases_id=f_id)
            ins.compile().params
            conn.execute(ins)
            log.debug('p %s' %p.name)
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            log.debug('u %s' %u.name)
            r=DBSession.query(Rol).filter(Rol.rol_name=='Desarrolladores').first()
            log.debug('r %s' %r.name)
            u.roles.append(r)
            p.usuarios.append(u)
            DBSession.flush()
        conn.close()
        log.debug('succes %s' %'usuarios agregados con exito!')
            
        msg    =    str(cantidad)    +    " usuarios agregados con exito!"
        type="succes"
        
        return dict(msg=msg,type=type, reload=reload)
    
    @expose('json')
    def quitar_usuarios(self,**kw):
        ids    =    kw['ids']
        ids    =    ids.split(",")

        f_id    =    ids[0]
        ids.remove(f_id)
        ids.pop()
        log.debug('ids %s' %ids)
        c1    =    len(ids)
        c2=0
        f_id    =    int(f_id)
        f=DBSession.query(Fase).filter_by(id=f_id).first()
        p=f.proyecto
        current_user=request.identity['user']
        current_user_id =current_user.id
        reload=False
        
        for id in ids:
            u_id = int(id)
            if u_id == current_user_id:
                reload=True
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            log.debug('u %s' %u.name)
            f.usuarios.remove(u)
            fases_del_usuario=DBSession.query(Fase).filter(Fase.usuarios.any(id = u_id))
            fases_del_proyecto=fases_del_usuario.filter_by(proyecto_id=p.id)
            r=DBSession.query(Rol).filter(Rol.rol_name==u'Desarrolladores').first()
            
            if len(u.fases)==0:
                log.debug('u %s' %u.name)
                r.usuarios.remove(u)
                log.debug('u %s' %u.name)
            if fases_del_proyecto.count()==0:
                log.debug('c2 %s' %c2)
                c2=c2+1
                log.debug('cant u %s' %len(p.usuarios))
                p.usuarios.remove(u)
                log.debug('cant u %s' %len(p.usuarios))
                
        DBSession.flush()
        if c2>0:
            msg_proyectos=str(c2)+" usuarios ya no forman parte de este proyecto."
        else:
            msg_proyectos=''
        msg    =    str(c1)    +    " usuarios quitados de la fase con exito!"
        type="succes"
        
        return dict(msg=msg,type=type,msg_p=msg_proyectos,reload=reload)
        
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
        
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def tiposDeItem_asignados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query,'fase_id':int(fid)}
                if qtype == 'name':
                    tiposDeItem = DBSession.query(TipoItem).filter(and_(TipoItem.fase_id!=fid,TipoItem.name.like('%'+query+'%')))
                elif qtype == 'codigo':
                    tiposDeItem = DBSession.query(TipoItem).filter(and_(TipoItem.fase_id!=fid,TipoItem.codigo.like('%'+query+'%')))
                else:
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
                            tipoDeItem.complejidad,
                            (', </br>'.join([(ce.name+': '+ce.tipo) for ce in tipoDeItem.campos_extra]))]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
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
                #log.debug('tiposDeItem: %s' %tiposDeItem)
            
            total = tiposDeItem.count() 
            column = getattr(TipoItem, sortname)
            tiposDeItem = tiposDeItem.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            #log.debug('tiposDeItem: %s' %tiposDeItem)                  
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
        value=str(f.proyecto_id)
        #referer='/configurar/vista_de_fases/?pid='+ value
        return dict(page=page, faseId=fid,faseNombre=nombre, referer=referer,title_nav=title_nav )    
    
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
            total = items.count()
            log.debug('total 2 %s' %total)            
            rows = [{'id'  : item.id,
                    'cell': [item.id,
                             item.codigo,                             
                            item.name,
                            item.version,
                            item.descripcion,
                            item.complejidad,
                            str(item.estado),
                            item.tipo_item.name]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result                     
        
    @expose('testando.templates.configurar.items.historial')    
    def historial(self, iid=None,**kw):
        referer=request.headers.get("Referer", "")        
                
        if find(referer,'configurar') >=0:
            page='Configurar'
        else:
            page='Desarrollar'
                    
        i=DBSession.query(Item).filter_by(id=int(iid)).first()
        #referer='/configurar/vista_de_items/?fid='+str(i.fase.id)
        return dict(page=page,item=i,referer=referer,title_nav="Lista de Items")
        
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def items_historial(self,iid=None, page='1', rp='25', sortname='version', sortorder='desc', qtype=None, query=None):
        i=DBSession.query(Item).filter_by(id=int(iid)).first()
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {'historico_id':i.historico_id}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(Item.historico==True)
                if qtype=='name':
                    items   =   items.filter(Item.name.like('%'+query+'%'))
                elif qtype=='estado':
                    items   =   items.filter(Item.estado.like('%'+query+'%'))
                elif qtype=='codigo':
                    items   =   items.filter(Item.codigo.like('%'+query+'%'))
                elif qtype=='version':
                    items   =   items.filter_by(version=int(query))                    
            else:
                d = {'historico_id':i.historico_id}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(Item.historico==True)
                
            total = items.count()
            log.debug('total %s' %total)
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            total = items.count()
            log.debug('total 2 %s' %total)            
            rows = [{'id'  : item.id,
                    'cell': [item.id,
                             item.codigo,
                            item.name,
                            item.version,
                            item.descripcion,
                            item.complejidad,
                            str(item.estado),
                            item.tipo_item.name]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result          
        
 
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
            if (query):
                d = {'fase_id':int(fid)}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(and_(Item.historico==False,Item.estado=='Aprobado',Item.linea_base_id==None))
                if qtype=='name':
                    items   =   items.filter(Item.name.like('%'+query+'%'))
                elif qtype=='estado':
                    items   =   items.filter(Item.estado.like('%'+query+'%'))
                elif qtype=='codigo':
                    items   =   items.filter(Item.codigo.like('%'+query+'%'))                
            else:
                d = {'fase_id':int(fid)}
                items = DBSession.query(Item).filter_by(**d)
                items = items.filter(and_(Item.historico==False,Item.estado=='Aprobado',Item.linea_base_id==None))
                
            total = items.count()
            log.debug('total item aprobados %s' %total)
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            total = items.count()
            log.debug('total item aprobados %s' %total)            
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

        msg=str(cant)+' items ahora tienen linea base.'
        type= 'succes'   
            
        return dict(msg=msg,type=type)  

    @expose('json')        
    def abrir_linea_base(self,**kw):
        lb=DBSession.query(LineaBase).filter_by(id=int(kw['id'])).first()
        lb.estado='Abierta'     
        DBSession.flush()

        msg='Linea base abierta con exito.'
        type= 'succes'   
            
        return dict(msg=msg,type=type)  


    def nueva_version(self,kw,adjunto_id=None):
        i                   =   DBSession.query(Item).filter_by(id=int(kw['itemid'])).first()
        i.historico         =   True
        
        item                =   Item()
        if kw.has_key('name'):
            item.name           =   kw['name']
        else:
            item.name           =   i.name        
        item.fase           =   i.fase
        item.codigo         =   i.codigo
        item.version        =   i.version+ 1
        item.tipo_item      =   i.tipo_item
        
        if kw.has_key('descripcion'):
            item.descripcion           =   kw['descripcion']
        else:
            item.descripcion           =   i.descripcion         

        if kw.has_key('complejidad'):
            item.complejidad           =   kw['complejidad']
        else:
            item.complejidad           =   i.complejidad
                    
        item.historico_id   =   i.historico_id
        
        if kw.has_key('atributos_extra'):
            
            if type(kw['atributos_extra'])==type(u''):
                a=kw['atributos_extra']
                kw['atributos_extra']=[]
                kw['atributos_extra'].append(a)
            for id in kw['atributos_extra']:
                log.debug('id = %s' %str(id))
                aeo          =   DBSession.query(AtributoExtra).filter_by(id=int(id)).first()
                aen          =   AtributoExtra()
                aen.valor    =   kw['atributos_extra_'+str(id)]
                aen.campo_extra_id  =   aeo.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
                log.debug('ae = %s' %str(aen))
                log.debug('attr extra valor = %s' %str(kw['atributos_extra_'+id]))
                log.debug('attr extra id = %s' %str(id))
        else:
            for ae in i.atributos_extra:
                aen          =   AtributoExtra()
                aen.valor    =   ae.valor
                aen.campo_extra_id  =   ae.campo_extra_id
                log.debug('ae = %s' %str(aen))
                DBSession.add(aen)
                item.atributos_extra.append(aen)
           
        if kw.has_key('padres'):
            item.padres=[]             
            for id in kw['padres']:
                p=DBSession.query(Item).filter_by(id=int(id)).first()
                item.padres.append(p)
        else:
            if kw.has_key('name'):
                item.padres=[]
            else:
                item.padres=[]             
                for p in i.padres:
                    item.padres.append(p)                
        
        if kw.has_key('antecesores'):
            item.antecesores=[]             
            for id in kw['antecesores']:
                a=DBSession.query(Item).filter_by(id=int(id)).first()
                item.antecesores.append(a)
        else:
            if kw.has_key('name'):            
                item.antecesores=[]
            else:
                for a in i.antecesores:
                    item.antecesores.append(a)
        
        
        if adjunto_id==None:
            for a in i.adjuntos:
                adjunto=Adjunto()
                adjunto.name    =   a.name
                adjunto.filecontent =   a.filecontent
                adjunto.item    =   item
                DBSession.add(adjunto)
        else:
            for a in i.adjuntos:
                if adjunto_id!=a.id:
                    adjunto=Adjunto()
                    adjunto.name    =   a.name
                    adjunto.filecontent =   a.filecontent
                    adjunto.item    =   item
                    DBSession.add(adjunto)
                                
        return item        

    @expose('json')        
    def revertir(self,**kw):          
        id                  =   kw['id'].split(',')
        kw['itemid']        =   int(id[1])
        log.debug('En revertir => itemid %s' %str(kw['itemid']))
        item                =   self.nueva_version(kw)
        i_actual            =   DBSession.query(Item).filter_by(id=int(id[0])).first()
        i_actual.historico  =   True
        item.version        =   i_actual.version+1
        
        ok=False
        relaciones= len(item.padres) + (item.antecesores)
        for p in item.padres:
            if p.estado=='Eliminado':
                item.padres.remove(p)
                relaciones=relaciones-1
                
        if item.fase.orden >1:
            for a in item.antecesores:
                if a.estado=='Eliminado':
                    item.antecesores.remove(a)
                    relaciones=relaciones-1
            if len(item.antecesores)>0:
                ok=True
                DBSession.flush()
        else:
            ok=True
            DBSession.flush()
             
        if ok: 
            msg='El item se ha revertido con exito!'
            type='succes'
        else:
            msg='El item no se puede revertir, NO se todas sus relaciones esta rotas'
            type='error'        
        return dict(msg=msg,type=type,id=str(item.id)) 
    
