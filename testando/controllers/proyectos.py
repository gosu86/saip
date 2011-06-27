from tg             import expose,redirect, validate,tmpl_context
from tg.decorators  import without_trailing_slash

from tgext.crud     import CrudRestController

from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model             	import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.auth        	import Usuario
from testando.model.auth        	import Rol
from testando.model.fase        	import Fase
from testando.widgets.proyecto_w 	import proyecto_new_form,proyecto_edit_filler,proyecto_edit_form
from testando.widgets.myWidgets 	import hideMe
from decorators import registered_validate, catch_errors
from formencode		import validators
errors = ()
try:
	from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
	errors =  (IntegrityError, DatabaseError, ProgrammingError)
except ImportError:
	pass
import logging
__all__ = ['ProyectosController']
log = logging.getLogger(__name__)
class ProyectosController(CrudRestController):
	log.debug('<-- In to ProyectosController -->')
	allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha logueado!'),
					 has_any_permission('AdministrarTodo',
										'AdministrarProyectos',
										msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarProyectos" acceder a esta seccion!'))	
	model		=	Proyecto
	new_form 	=	proyecto_new_form
	edit_filler	=	proyecto_edit_filler
	edit_form 	=	proyecto_edit_form

	@expose('testando.templates.administrar.proyectos.index')
	def get_all(self):
		return dict(page="Administar")

	@without_trailing_slash
	@expose('testando.templates.administrar.proyectos.new')
	def new(self, *args, **kw):
		"""Display a page to show a new record."""
		tmpl_context.widget = self.new_form
		referer='/administrar/proyectos/'
		return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Proyectos')
	
	@catch_errors(errors, error_handler=new)
	@expose()
	@registered_validate(error_handler=new)
	def post(self, *args, **kw):
		p=self.provider.create(self.model, params=kw)
		r=DBSession.query(Rol).filter(Rol.rol_name=='Configuradores').first()
		p.lider.roles.append(r)
		DBSession.flush()
		raise redirect('./')		
	
	@expose('testando.templates.administrar.proyectos.edit')
	def edit(self, *args, **kw):
		"""Display a page to edit the record."""
		tmpl_context.widget = self.edit_form
		pks = self.provider.get_primary_fields(self.model)
		kw = {}
		for i, pk in  enumerate(pks):
			kw[pk] = args[i]
		value = self.edit_filler.get_value(kw)
		value['_method'] = 'PUT'
		referer='/administrar/proyectos/'
		return dict(value=value, model=self.model.__name__, pk_count=len(pks),referer=referer,title_nav='Lista de Proyectos')	
	
	@expose()
	def put(self, *args, **kw):
		"""update"""
		id=kw['name']
		log.debug('id: %s' %id )
		log.debug('ARGS: %s' %str(args))
		pks = self.provider.get_primary_fields(self.model)
		for i, pk in enumerate(pks):
			if pk not in kw and i < len(args):
				kw[pk] = args[i]
		d={'id':kw[pk]}
		p=DBSession.query(Proyecto).filter_by(**d).first()
		log.debug('proyecto.name: %s' %p.name )
		p.name=kw['name']
		p.empresa=kw['empresa']
		p.estado=kw['estado']
		p.descripcion=kw['descripcion']
		p.lider_id=int(kw['lider'])
		DBSession.flush()
		redirect('../' * len(pks))
		
	@validate(validators={"id":validators.Int()})
	@expose('json')
	def post_delete(self,**kw):
		id = kw['id']
		log.debug("Inside post_fetch: id == %s" % (id))
		if (id != None):
			d = {'id':id}
			proyecto = DBSession.query(Proyecto).filter_by(**d).first()
			nombre=proyecto.name
			if (proyecto.estado != 'Iniciado'):
				DBSession.delete(proyecto)
				DBSession.flush()
				msg="El proyecto se ha eliminado con exito!."
				type="succes"
			else:
				msg="El proyecto esta Iniciado! No se puede eliminar."
				type="error"
		return dict(msg=msg,nombre=nombre,type=type)			
				
	@expose()
	def get_one(self, *args, **kw):
		redirect('../')
			