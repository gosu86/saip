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
		"""Muestra la pagina index.html de proyectos, en la cual se muestra la lista de proyectos existentes en el sistema."""
		return dict(page="Administar")

	@without_trailing_slash
	@expose('testando.templates.administrar.proyectos.new')
	def new(self, *args, **kw):
		"""Muestra la pagina new.html con el from para la creacion de un nuevo proyecto."""
		tmpl_context.widget = self.new_form
		referer='/administrar/proyectos/'
		return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Proyectos')
	
	@catch_errors(errors, error_handler=new)
	@expose()
	@registered_validate(error_handler=new)
	def post(self, *args, **kw):
		""" Guarda un proyecto nuevo en la base de datos."""
		p=self.provider.create(self.model, params=kw)
		r=DBSession.query(Rol).filter(Rol.rol_name=='Configuradores').first()
		p.lider.roles.append(r)
		DBSession.flush()
		raise redirect('/administrar/proyectos/')		
	
	@expose('testando.templates.administrar.proyectos.edit')
	def edit(self, *args, **kw):
		"""Muestra la pagina edit.html con el form para la edicion de un proyecto seleccionado."""
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
		"""Actualiza en la BD los cambios realizados a un proyecto."""
		pks = self.provider.get_primary_fields(self.model)
		for i, pk in enumerate(pks):
			if pk not in kw and i < len(args):
				kw[pk] = args[i]
		d={'id':kw[pk]}
		p=DBSession.query(Proyecto).filter_by(**d).first()
		
		p.name=kw['name']
		p.empresa=kw['empresa']
		p.estado=kw['estado']
		p.descripcion=kw['descripcion']
		p.lider_id=int(kw['lider'])
		DBSession.flush()
		redirect('/administrar/proyectos/')
		
	@validate(validators={"id":validators.Int()})
	@expose('json')
	def post_delete(self,**kw):
		"""Elimina un proyecto (cambia su estado a eliminado)."""
		id = kw['id']
		if (id != None):
			d = {'id':id}
			proyecto = DBSession.query(Proyecto).filter_by(**d).first()
			nombre=proyecto.name
			if (proyecto.estado != 'Iniciado'):
				proyecto.estado='Eliminado'
				DBSession.flush()
				msg="El proyecto se ha eliminado con exito!."
				type="succes"
			else:
				msg="El proyecto esta Iniciado! No se puede eliminar."
				type="error"
		return dict(msg=msg,nombre=nombre,type=type)

	@validate(validators={"id":validators.Int()})
	@expose('json')
	def iniciar_proyecto(self,**kw):
		"""
		Inicia un proyecto seleccionado.
		@param id: id del proyecto. 
		"""
		id = kw['id']
		if (id != None):
			d = {'id':id}
			proyecto = DBSession.query(Proyecto).filter_by(**d).first()
			nombre=proyecto.name
			if (proyecto.estado != 'Iniciado'):
				f=proyecto.fases[0]
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
	
	@validate(validators={"page":validators.Int(), "rp":validators.Int()})
	@expose('json')	
	def fases_asignadas(self,pid=None, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
		"""
		Devuelve la lista de fases asignadas a un proyecto.
		@param proyecto_id: id del proyecto.
		"""
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
				
			total	   =   fases.count()
			column	  =   getattr(Fase, sortname)
			fases	   =   fases.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
			
			rows = [{'id'  : fase.id,
					'cell': [fase.id,
							fase.name,
							fase.descripcion,
							fase.estado,
							fase.orden,
							fase.tiene_usuarios(),
							fase.tiene_tiposDeItem(),
							fase.tiene_items()]} for fase in fases]
			result = dict(page=page, total=total, rows=rows)
		except:
			result = dict() 
		return result