from tg             import expose,redirect, validate,flash,tmpl_context, request,config
from formencode        import validators
from repoze.what.predicates import All
from repoze.what.predicates import not_anonymous
from repoze.what.predicates import in_any_group

from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_

from testando.model                 import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.fase            import Fase,usuario_rol_fase_table
from testando.model.auth            import Usuario
from testando.model.tipoitem        import TipoItem
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

    tiposDeItem=TiposDeItemController(DBSession)
    tiposDeItem.template='genshi:testando.templates.configurar.tiposDeItems.index'
    tiposDeItem.page='Configurar'
    
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
    
    @expose('testando.templates.configurar.index')    
    def index(self, **kw):
        #return dict(page='Configurar')
        redirect('seleccion_de_proyectos')

    @expose('testando.templates.configurar.seleccion_de_proyectos')    
    def seleccion_de_proyectos(self,**kw):
        return dict(page='Configurar')
             
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

            # botonIniciar = '<input type="submit" value="Iniciar" onClick=doCommandFases("Iniciar",$("#proyectosConfigurarFlexi"))>'
            # botonVerFases = '<input type="submit" class="clickclass" value="Ver Fases">'
            #-------------------------------- botones=botonIniciar+botonVerFases
            
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
    @expose('testando.templates.configurar.proyectos.vista_de_fases') 
    def vista_de_fases(self,*args, **kw):
        pId=kw['pId']
        estado=kw['estado']
        nombre=kw['nombre']
        tmpl_context.proyectoId = hideMe()
        tmpl_context.proyectoNombre = hideMe()
        if estado=='Iniciado':
            iniciado=True
        else:
            iniciado=False
        return dict(page='Vista de Fases', proyectoId=pId, iniciado=iniciado,proyectoNombre=nombre)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def fases_asignadas(self,pid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query,'proyecto_id':int(pid)}
                fases = DBSession.query(Fase).filter_by(**d)
            else:
                d = {'proyecto_id':int(pid)}
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
            op1='<option value=1>Aprovador</option>'
            op2='<option value=2>Desarrollador</option>'
            op3='<option value=3>Aprovador y Desarrollador</option>'            
            if selected==1:
                log.debug('1')
                op1='<option value=1 selected="true">Aprovador</option>'
            elif selected==2:
                log.debug('2')
                op2='<option value=2 selected="true">Desarrollador</option>'
                
            elif selected==3:
                log.debug('3')
                op3='<option value=3 selected="true":>Aprovador y Desarrollador</option>'

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
        fId=kw['fId']
        nombre=kw['nombre']
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        return dict(page='Vista de Usuarios', faseId=fId,faseNombre=nombre)
    
    def get_rol(self,uid,fid):
        uid=int(uid)
        fid=int(fid)
        conn = config['pylons.app_globals'].sa_engine.connect()
        se=select([usuario_rol_fase_table.c.rol_id],and_(usuario_rol_fase_table.c.usuario_id==uid, usuario_rol_fase_table.c.fases_id==fid))
        log.debug('se = %s' %se)
        
        result=conn.execute(se)
        row=result.fetchone() 
        rol=int(row['rol_id'])
        
        log.debug('uid_id %s' %uid)
        log.debug('rol_id %s' %rol)
        log.debug('fid_id %s' %fid)
        conn.close()
        select_tag=self.roles_select(uid,rol) 
        # log.debug('select = %s' %select)   
        #=======================================================================
        #sel=self.roles_select(uid,3)
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
            log.debug('rows = %s' %rows) 
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
        
        cantidad    =    len(idsyroles)
        
        f_id    =    int(f_id)
        f=DBSession.query(Fase).filter_by(id=f_id).first()
        p=f.proyecto
        conn = config['pylons.app_globals'].sa_engine.connect()
        for idyrol in idsyroles:
            idyrol=idyrol.split(',')
            u_id = int(idyrol[0])
            rol = int(idyrol[1])
            ins=usuario_rol_fase_table.insert().values(usuario_id=u_id,rol_id=rol,fases_id=f_id)
            ins.compile().params
            log.debug('ins.params: %s' %ins.compile().params)
            log.debug('con: %s' %conn)
            conn.execute(ins)
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            p.usuarios.append(u)
            DBSession.flush()
        conn.close()
        
            
        msg    =    str(cantidad)    +    " usuarios agregados con exito!"
        type="succes"
        
        return dict(msg=msg,type=type)
    
    @expose('json')
    def quitar_usuarios(self,**kw):
        ids    =    kw['ids']
        ids    =    ids.split(",")

        f_id    =    ids[0]
        ids.remove(f_id)
        ids.pop()
        
        c1    =    len(ids)
        c2=0
        f_id    =    int(f_id)
        f=DBSession.query(Fase).filter_by(id=f_id).first()
        p=f.proyecto
        for id in ids:
            u_id = int(id)
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            f.usuarios.remove(u)
            fases_del_usuario=DBSession.query(Fase).filter(Fase.usuarios.any(id = u_id))
            fases_del_proyecto=fases_del_usuario.filter_by(proyecto_id=p.id)
            if fases_del_proyecto.count()==0:
                c2=c2+1
                p.usuarios.remove(u)
            DBSession.flush()
        if c2>0:
            msg_proyectos=str(c2)+" usuarios ya no forman parte de este proyecto."
        else:
            msg_proyectos=''
        log.debug('msg_proyectos:= %s' %msg_proyectos)
        msg    =    str(c1)    +    " usuarios quitados de la fase con exito!"
        type="succes"
        
        return dict(msg=msg,type=type,msg_p=msg_proyectos)

    #===========================================================================
    # @expose('testando.templates.configurar.fases.vista_de_tiposDeItem')
    # def vista_de_tiposDeItem(self,*args, **kw):
    #    tiId=int(kw['fId'])
    #    tiposDeItems=DBSession.query(TipoItem)filter)_by('id':tiId)
    #===========================================================================
        
    @expose('json')    
    @expose('testando.templates.configurar.fases.vista_de_tiposDeItem') 
    def vista_de_tiposDeItem(self,*args, **kw):
        fId=kw['fId']
        #estado=kw['estado']
        nombre=kw['nombre']
        tmpl_context.faseId = hideMe()
        tmpl_context.faseNombre = hideMe()
        #=======================================================================
        # if estado=='Iniciado':
        #    iniciado=True
        # else:
        #    iniciado=False
        #=======================================================================
        return dict(page='Vista de Tipos de Item', faseId=fId,faseNombre=nombre)        
        
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
                            tipoDeItem.complejidad]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
        
    #===========================================================================
    # @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    # @expose('json')
    # def tiposDeItem_del_sistema(self, fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
    #    try:
    #        offset = (int(page)-1) * int(rp)
    #        if (query):
    #            d = {qtype:query}
    #            usuarios = DBSession.query(Usuario).filter_by(**d)
    #        else:
    #            usuarios = DBSession.query(Usuario)
    #            
    #           
    #        if fid:
    #            
    #            column = getattr(Usuario, sortname)
    #            usuarios = usuarios.order_by(getattr(column,sortorder)())                
    #            u=self.get_usuarios(usuarios,fid,offset,rp)
    #            total = usuarios.count()
    #            usuarios=u
    #        else:
    #            total = usuarios.count() 
    #            column = getattr(Usuario, sortname)
    #            usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
    #              
    #        rows = [{'id'  : usuario.id,
    #                'cell': [usuario.id,
    #                         usuario.name,
    #                         self.roles_select(usuario.id)]} for usuario in usuarios
    #                ]
    #        result = dict(page=page, total=total, rows=rows)
    #    except:
    #        result = dict() 
    #    return result        
    #    
    #===========================================================================
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        