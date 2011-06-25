from tg             import expose,redirect, validate,flash,tmpl_context,config
from tg.decorators  import override_template
from tg.decorators  import without_trailing_slash
from decorators import registered_validate, register_validators, catch_errors
from tgext.crud     import CrudRestController
from sqlalchemy.sql import and_, or_, not_
from testando.model             import DBSession
from testando.model.fase        import Fase
from testando.model.auth        import Rol
from testando.model.campoextra  import CampoExtra
from testando.model.tipoitem        import TipoItem
from testando.model.proyecto        import Proyecto
from testando.widgets.fase_w    import fase_new_form,fase_edit_filler,fase_edit_form
from testando.widgets.myWidgets import hideMe
from formencode     import validators

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
    log.debug('<-- In to FasesController -->')
    model       =   Fase
    new_form    =   fase_new_form
    edit_filler =   fase_edit_filler    
    edit_form   =   fase_edit_form
    
    template=''
    page=''

    @expose()
    def get_all(self,proyecto_Id=''):
        tmpl_context.proyectoId = hideMe()
        override_template(self.get_all,self.template)    
        return dict(page=self.page, proyectoId=proyecto_Id)
    
    @without_trailing_slash
    @expose('testando.templates.administrar.fases.new')
    def new(self, *args, **kw):
        kw['orden']=len(DBSession.query(Proyecto).filter_by(id=int(kw['proyecto_id'])).first().fases)+1
        #proyecto_id se recibe en kw, y este se le asigna a value y en el template se le llena
        """Display a page to show a new record."""
        tmpl_context.widget = self.new_form
        referer='/configurar/vista_de_fases/?pid='+str(kw['proyecto_id'])
        return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Fases')
    
    @catch_errors(errors, error_handler=new)
    @expose()
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        self.provider.create(self.model, params=kw)
        raise redirect('/configurar/vista_de_fases/?pid='+kw['proyecto_id'])    

    @expose('testando.templates.administrar.fases.edit')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        #tmpl_context.widget = self.edit_form
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        log.debug('__________%s' %value)
        referer='/configurar/vista_de_fases/?pid='+str(value['proyecto_id'])
        return dict(value=value, model=self.model.__name__, pk_count=len(pks),referer=referer,title_nav='Lista de Fases')


    @expose()
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
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
        id = kw['id']
        if (id != None):
            d = {'id':id}
            fase = DBSession.query(Fase).filter_by(**d).first()
            p=fase.proyecto
            nombre=fase.name
            if (fase.estado == 'Inicial'):
                r=DBSession.query(Rol).filter(Rol.rol_name=='Desarrolladores').first()
                for u in fase.usuarios:
                    if (len(u.fases)-1)==0:
                        log.debug('remover')
                        u.roles.remove(r) 
                    c=0    
                    for f in u.fases:
                        if f.proyecto_id==p.id:
                            c=c+1
                    if (c-1)==0:
                        p.usuarios.remove(u)
                                    
                DBSession.delete(fase)
                DBSession.flush()
                msg="la fase "+nombre+" se ha eliminado con exito!."
                type="succes"
            else:
                msg="La fase NO se puede eliminar, ya se ha iniciado."
                type="error"
        return dict(msg=msg,nombre=nombre,type=type)
       
    @expose()
    def get_one(self, *args, **kw):
        redirect('../')
        
    @expose('json')
    def importar_TiposDeItem(self,**kw):
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
        