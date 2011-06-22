from tg             import expose,redirect, validate,flash,tmpl_context,config
from tg.decorators  import override_template
from tg.decorators  import without_trailing_slash
from decorators import registered_validate, register_validators, catch_errors


from tgext.crud     import CrudRestController

from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model	            	import DBSession
from testando.model.auth        	import Permiso
from testando.widgets.permiso_w		import permiso_new_form,permiso_edit_filler,permiso_edit_form

from formencode		import validators

import logging
errors=()
__all__ = ['PermisosController']
log = logging.getLogger(__name__)
class PermisosController(CrudRestController):
	allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!'),
					 has_any_permission('AdministrarTodo',
										'AdministrarPermisos',
										msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarPermisos" acceder a esta seccion!'))	
	model 		= 	Permiso
	new_form	=	permiso_new_form
	edit_filler	=	permiso_edit_filler
	edit_form	= 	permiso_edit_form

	@expose('testando.templates.administrar.permisos.index')
	def get_all(self):
		return dict(page="Administrar")
	
	@validate(validators={"page":validators.Int(), "rp":validators.Int()})
	@expose('json')
	def fetch(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
		try:	
			offset = (int(page)-1) * int(rp)
			if (query):
				d = {qtype:query}
				permisos = DBSession.query(Permiso).filter_by(**d)
			else:
				permisos = DBSession.query(Permiso)
			
			total = permisos.count()
			column = getattr(Permiso, sortname)
			log.debug("column = %s" %column)
			permisos = permisos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
			
			rows = [{'id'  : permiso.id,
					'cell': [permiso.id,
							permiso.permiso_name,
							permiso.descripcion,
							(', </br> '.join([r.name for r in permiso.roles]))
							]} for permiso in permisos
					]
			result = dict(page=page, total=total, rows=rows)
		except:
			result = dict() 
		return result
	
	@expose()
	def get_one(self, *args, **kw):
		redirect('../')
	
	@validate(validators={"id":validators.Int()})
	@expose('json')
	def post_delete(self,**kw):
		id = kw['id']
		log.debug("Inside post_fetch: id == %s" % (id))
		if (id != None):
			d = {'id':id}
			permiso = DBSession.query(Permiso).filter_by(**d).first()
			nombre=permiso.permiso_name
			DBSession.delete(permiso)
			DBSession.flush()
			msg="El permiso se ha eliminado."
		return dict(msg=msg,nombre=nombre)
	
    
	@expose('testando.templates.administrar.permisos.edit')
	def edit(self, *args, **kw):
	 	"""Display a page to edit the record."""
	 	tmpl_context.widget = self.edit_form
	 	pks = self.provider.get_primary_fields(self.model)
	 	kw = {}
	 	for i, pk in  enumerate(pks):
	 		kw[pk] = args[i]
	 	value = self.edit_filler.get_value(kw)
	 	value['_method'] = 'PUT'
	 	referer='/administrar/permisos/'
	 	return dict(value=value, model=self.model.__name__, pk_count=len(pks),referer=referer,title_nav='Lista de Permisos')

	@without_trailing_slash
	@expose('testando.templates.administrar.permisos.new')
	def new(self, *args, **kw):
		"""Display a page to show a new record."""
		tmpl_context.widget = self.new_form
		referer='/administrar/permisos/'
		return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Permisos')

	@catch_errors(errors, error_handler=new)
	@expose()
	@registered_validate(error_handler=new)
	def post(self, *args, **kw):
		self.provider.create(self.model, params=kw)
		raise redirect('./')