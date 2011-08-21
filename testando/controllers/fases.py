from tg             import expose,redirect, validate,flash,tmpl_context,config, request
from tg.decorators  import override_template
from tg.decorators  import without_trailing_slash
from decorators import registered_validate, register_validators, catch_errors
from tgext.crud     import CrudRestController
from sqlalchemy.sql import and_, or_, not_,select
from testando.model             import DBSession
from testando.model.fase            import Fase,usuario_rol_fase_table
from testando.model.auth        import Rol
from testando.model.auth            import Usuario
from testando.model.item            import Item
from testando.model.campoextra  import CampoExtra
from testando.model.tipoitem        import TipoItem
from testando.model.proyecto        import Proyecto
from testando.widgets.fase_w    import fase_new_form,fase_edit_filler,fase_edit_form
from testando.widgets.myWidgets import hideMe
from formencode     import validators
from string import find

errors = ()
try:
    from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
    errors =  (IntegrityError, DatabaseError, ProgrammingError)
except ImportError:
    pass

import logging

__all__ = ['FasesController']
log = logging.getLogger(__name__)
class FasesController(CrudRestController):
    model       =   Fase
    new_form    =   fase_new_form
    edit_filler =   fase_edit_filler    
    edit_form   =   fase_edit_form
   
    @without_trailing_slash
    @expose('testando.templates.administrar.fases.new')
    def new(self, *args, **kw):
        """Muestra la pagina new.html con el from para la creacion de un nueva fase."""
        kw['orden']=len(DBSession.query(Proyecto).filter_by(id=int(kw['proyecto_id'])).first().fases)+1
        tmpl_context.widget = self.new_form
        referer='/configurar/vista_de_fases/?pid='+str(kw['proyecto_id'])
        return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Fases')
    
    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        """ Guarda una fase nueva en la base de datos """
        self.provider.create(self.model, params=kw)
        raise redirect('/configurar/vista_de_fases/?pid='+kw['proyecto_id'])    

    @expose('testando.templates.administrar.fases.edit')
    def edit(self, *args, **kw):
        """Muestra la pagina edit.html con el form para la edicion de una fase seleccionada."""
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        referer='/configurar/vista_de_fases/?pid='+str(value['proyecto_id'])
        return dict(value=value, model=self.model.__name__, pk_count=len(pks),referer=referer,title_nav='Lista de Fases')

    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """Actualiza en la BD los cambios realizados a una fase."""
        pks = self.provider.get_primary_fields(self.model)
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw[pk] = args[i]

        fase=self.provider.update(self.model, params=kw)
        pid=fase.proyecto.id
        redirect('/configurar/vista_de_fases/?pid='+str(pid))
            
    @validate(validators={"id":validators.Int()})
    @expose('json')
    def post_delete(self,**kw):
        """ Elimina una fase del sistema."""
        borrada=False
        if (kw['id'] != None):
            fase = DBSession.query(Fase).filter_by(id=int(kw['id'])).first()
            p=fase.proyecto
            if (fase.estado == 'Inicial'):
                r=DBSession.query(Rol).filter(Rol.rol_name=='Desarrolladores').first()
                for u in fase.usuarios:
                    if (len(u.fases)-1)==0:
                        u.roles.remove(r)
                        p.usuarios.remove(u)
                    else: 
                        c=0    
                        for f in u.fases:
                            if f.proyecto_id==p.id:
                                c=c+1
                        if (c-1)==0:
                            p.usuarios.remove(u)
                DBSession.delete(fase)
                DBSession.flush()
                borrada=True
        return dict(borrada=borrada)
             
    @expose('json')
    def importar_TiposDeItem(self,**kw):
        """Gestiona la importacino de items"""
        ids    =    kw['ids']
        ids    =    ids.split(",")
        f_id    =    ids[0]
        ids.remove(f_id)
        ids.pop()
        
        cantidad    =    len(ids)
    
        f_id    =    int(f_id)
        conn = config['pylons.app_globals'].sa_engine.connect()
        names=''
        for id in ids:
            id=int(id)
            tdi=DBSession.query(TipoItem).filter_by(id=id).first()
            existeTDI=DBSession.query(TipoItem).filter(or_(
                                                           and_(TipoItem.fase_id==f_id,TipoItem.name==tdi.name),
                                                           and_(TipoItem.fase_id==f_id,TipoItem.codigo==tdi.codigo))
                                                       )
            if existeTDI.count() > 0:
                names=names+tdi.name+', '
            else:
                ins=TipoItem.__table__.insert().values(name=tdi.name,codigo=tdi.codigo,descripcion=tdi.descripcion,complejidad=tdi.complejidad,fase_id=f_id)
                ins.compile().params
                result=conn.execute(ins)
                newTDIid=int(result.inserted_primary_key[0])
                for ce in tdi.campos_extra:
                    ins=CampoExtra.__table__.insert().values(name=ce.name, tipo=ce.tipo, tipo_item_id=newTDIid)
                    ins.compile().params
                    conn.execute(ins)                
        conn.close()

        names=names.split(',')
        names.pop()
   
        cantNames=len(names)        
        cantidad=cantidad- cantNames       
   
        msg=''
        type=""
        error=''      
        if cantidad > 0:    
            msg    =    str(cantidad)    +    " tipos de item importados con exito!"
            type="succes"
        if cantNames > 0:
            error = 'Los tipos de item '+str(names)+'no pudieron importarse, existen tipos de item con mismo nombre y/o codigo en la fase destino.'
        return dict(msg=msg,type=type, error=error)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def tiposDeItem_asignados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """Devuelve los tipos de item pertenecientes a la fase seleccionada. """
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
                            (', </br>'.join([(ce.name+': '+ce.tipo) for ce in tipoDeItem.campos_extra]))]} for tipoDeItem in tiposDeItem]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def items_creados(self,solo_e=None,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            offset = (int(page)-1) * int(rp)
            d = {'fase_id':int(fid)}
            items = DBSession.query(Item).filter_by(**d)
            items = items.filter(Item.historico==False) 

            referer=request.headers.get("Referer", "")        
            if (find(referer,'desarrollar') >=0): 
                if solo_e==None:
                    items = items.filter(Item.estado!='Eliminado')
                else:
                    items = items.filter(Item.estado=='Eliminado')
                                 
            if (query):                
                if qtype=='name':
                    items   =   items.filter(Item.name.like('%'+query+'%'))
                elif qtype=='estado':
                    items   =   items.filter(Item.estado.like('%'+query+'%'))
                elif qtype=='codigo':
                    items   =   items.filter(Item.codigo.like('%'+query+'%'))                
                elif qtype=='version':
                    items   =   items.filter_by(version=int(query))

                
            total = items.count()
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            total = items.count()           
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

    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')    
    def usuarios_asignados(self,fid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        """
        
        """
        
        try:
            offset = (int(page)-1) * int(rp)
            
            if (query):
                d = {qtype:query}
                usuarios = DBSession.query(Usuario).filter(Usuario.fases.any(id = int(fid))).filter_by(**d)

            else:
                usuarios = DBSession.query(Usuario).filter(Usuario.fases.any(id = int(fid)))
                
            total = usuarios.count()
            column = getattr(Usuario, sortname)
            usuarios = usuarios.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
            rows = [{'id'  : u.id,
                    'cell': [u.id,
                            u.name,
                            u.get_rol(fid),
                            ]} for u in usuarios]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @expose('json')
    def agregar_usuarios(self,**kw):
        idsyroles    =    kw['idsyroles[]']
        f_id    =   int(idsyroles.pop())
        current_user=request.identity['user']
        current_user_id =current_user.id
        reload=False
        cantidad    =    len(idsyroles)

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
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            r=DBSession.query(Rol).filter(Rol.rol_name=='Desarrolladores').first()
            u.roles.append(r)
            p.usuarios.append(u)
            DBSession.flush()
        conn.close()
        return dict(cantidad=cantidad, reload=reload)
    
    @expose('json')
    def quitar_usuarios(self,**kw):
        ids    =    kw['ids[]']
        f_id    =   int(ids.pop())
        f=DBSession.query(Fase).filter_by(id=f_id).first()
        p=f.proyecto

        current_user=request.identity['user']
        current_user_id=current_user.id
        reload=False
        
        fuera_del_proyecto=0
        for id in ids:
            u_id = int(id)
            if u_id == current_user_id:
                reload=True
                
            u=DBSession.query(Usuario).filter_by(id=u_id).first()
            f.usuarios.remove(u)
            fases_del_usuario=DBSession.query(Fase).filter(Fase.usuarios.any(id = u_id))
            fases_del_proyecto=fases_del_usuario.filter_by(proyecto_id=p.id)
            r=DBSession.query(Rol).filter(Rol.rol_name==u'Desarrolladores').first()
            
            if len(u.fases)==0:
                r.usuarios.remove(u)
            if fases_del_proyecto.count()==0:
                fuera_del_proyecto=fuera_del_proyecto+1
                p.usuarios.remove(u)
        DBSession.flush()
        return dict(quitados=len(ids),fuera_del_proyecto=fuera_del_proyecto,reload=reload)