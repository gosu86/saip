from tg             import expose,redirect, validate,flash,tmpl_context,config
from tg.decorators  import override_template
from tg.decorators  import without_trailing_slash
from decorators import registered_validate, register_validators, catch_errors
from tgext.crud     import CrudRestController
from repoze.what.predicates import All,not_anonymous,has_any_permission
from tg.decorators  import without_trailing_slash

from testando.model             import DBSession
from testando.model.auth        import Rol
from testando.widgets.rol_w		import rol_new_form,rol_edit_filler,rol_edit_form

from formencode		import validators

import logging
errors=()
__all__ = ['RolesController']
log = logging.getLogger(__name__)
class RolesController(CrudRestController):
	allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!'),
					 has_any_permission('AdministrarTodo',
										'AdministrarRoles',
										msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarRoles" acceder a esta seccion!'))	
	model 		= 	Rol
	new_form 	= 	rol_new_form
	edit_filler	=	rol_edit_filler
	edit_form 	=	rol_edit_form

	@expose('testando.templates.administrar.roles.index')
	def get_all(self):
		return dict(page="Administrar")
	
	@validate(validators={"page":validators.Int(), "rp":validators.Int()})
	@expose('json')
	def fetch(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
		offset = (int(page)-1) * int(rp)
		if (query):
			d = {qtype:query}
			roles = DBSession.query(Rol).filter_by(**d)
		else:
			roles = DBSession.query(Rol)
			
		total = roles.count()
		column = getattr(Rol, sortname)
		roles = roles.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
		rows = [{'id'  : rol.id,
				'cell': [rol.id,
						 rol.name,
						(', </br>'.join([p.permiso_name for p in rol.permisos]))
						]} for rol in roles
				]
		result = dict(page=page, total=total, rows=rows)
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
			rol = DBSession.query(Rol).filter_by(**d).first()
			nombre=rol.name
			DBSession.delete(rol)
			DBSession.flush()
			msg="El rol se ha eliminado."

		return dict(msg=msg,nombre=nombre)
	
	
	@expose('testando.templates.administrar.roles.edit')
	def edit(self, *args, **kw):
		tmpl_context.widget = self.edit_form
		pks = self.provider.get_primary_fields(self.model)
		kw = {}
	 	for i, pk in  enumerate(pks):
	 		kw[pk] = args[i]
	 	value = self.edit_filler.get_value(kw)
	 	value['_method'] = 'PUT'
	 	referer='/administrar/roles/'
	 	return dict(value=value, model=self.model.__name__, pk_count=len(pks),referer=referer,title_nav='Lista de Roles')

	@without_trailing_slash
	@expose('testando.templates.administrar.roles.new')
	def new(self, *args, **kw):
		tmpl_context.widget = self.new_form
		referer='/administrar/roles/'
		return dict(value=kw, model=self.model.__name__,referer=referer,title_nav='Lista de Roles')


	@catch_errors(errors, error_handler=new)
	@expose()
	@registered_validate(error_handler=new)
	def post(self, *args, **kw):
		self.provider.create(self.model, params=kw)
		raise redirect('./')
