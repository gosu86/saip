from sprox.dojo.formbase import DojoEditableForm,DojoAddRecordForm
from sprox.fillerbase    import EditFormFiller

from tw.forms import TextField,MultipleSelectField

from testando.model import DBSession
from testando.model.auth import Rol      

class RolNewForm(DojoAddRecordForm):
    __model__       = Rol
    __omit_fields__ = ['fecha_creacion']
    __field_order__ = ['name','rol_name','permisos']
    
    name        = TextField('name',label_text='Nombre ')
    rol_name    = TextField('rol_name',label_text='Nombre Descriptivo')
#============================================================

class RolEditFiller(EditFormFiller):
    __model__ = Rol
#============================================================
   
class RolEditForm(DojoEditableForm):
    __model__       = Rol
    __field_order__ = ['name']
    __omit_fields__ = ['fecha_creacion']
    __field_order__ = ['name','rol_name','permisos']
    
    name        = TextField('name',label_text='Nombre ')
    
#============================================================

rol_new_form = RolNewForm(DBSession)
    
rol_edit_filler=RolEditFiller(DBSession)    
rol_edit_form=RolEditForm(DBSession)