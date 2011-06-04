from tg             import expose,redirect,validate
from tg.decorators  import override_template

from tgext.crud     import CrudRestController

from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model	            	import DBSession
from testando.model.auth        	import Permiso
from testando.widgets.permiso_w		import permiso_new_form,permiso_edit_filler,permiso_edit_form

from formencode		import validators

import logging

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
	
	template	=	''
	page		=	''

	@expose()
	def get_all(self):
		override_template(self.get_all,self.template)	
		return dict(page=self.page)
	
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
							(', '.join([r.name for r in permiso.roles]))
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