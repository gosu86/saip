from sprox.formbase import EditableForm
from sprox.formbase import AddRecordForm
from sprox.fillerbase    import EditFormFiller

from tw.forms import TextField

from testando.model.auth import Permiso
from testando.model import DBSession
        

class PermisoNewForm(AddRecordForm):
    __model__ = Permiso
    
    __omit_fields__ = ['roles']
    __field_order__ = ['permiso_name','descripcion']
    __field_attrs__ = {'descripcion':{'rows':'2'}}
             
    permiso_name    =   TextField('permiso_name',label_text='Nombre ')
#============================================================

class PermisoEditFiller(EditFormFiller):
    __model__ = Permiso  
#============================================================
  
class PermisoEditForm(EditableForm):
    __model__ = Permiso
    
    __omit_fields__ = ['roles']
    __field_order__ = ['permiso_name','descripcion']
    __field_attrs__ = {'descripcion':{'rows':'2'}}
    
    permiso_name    =   TextField('permiso_name',label_text='Nombre ')
#============================================================
    
permiso_new_form    =   PermisoNewForm(DBSession)

permiso_edit_filler =   PermisoEditFiller(DBSession)   
permiso_edit_form   =   PermisoEditForm(DBSession)