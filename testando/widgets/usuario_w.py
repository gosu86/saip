from sprox.dojo.formbase    import DojoEditableForm,DojoAddRecordForm
from sprox.fillerbase       import EditFormFiller

from testando.model         import DBSession
from testando.model.auth    import Usuario

from tw.forms import TextField,PasswordField
from myWidgets import SingleSelectEstadosUsuarios
from tw.forms.validators import Int, NotEmpty, DateConverter
from formencode.validators import Email,MinLength
     

class UsuarioNewForm(DojoAddRecordForm):
    __model__          =   Usuario
    __omit_fields__    =   ['id','fecha_creacion','roles','estado','proyectos','fases','mis_proyectos']
    __field_order__    =   ['name','apellido','email','usuario_name','_password','fecha_creacion']
    __field_attrs__    =   {'name':{'label':'Nombre:'}}
    __require_fields__ =   ['apellido','usuario_name','_password']
    
    password    =   PasswordField('_password',validator=MinLength(4))
    name        =   TextField('name',label_text='Nombre ', validator=NotEmpty)
    email       =   TextField('email', validator=Email(not_empty=True),attrs={'size':30})
    submit_text = 'Guardar'

class UsuarioEditFiller(EditFormFiller):
    __omit_fields__   = ['password']
    __model__ = Usuario
   
class UsuarioEditForm(DojoEditableForm):
    __model__       =   Usuario
    __omit_fields__ =   ['fecha_creacion','id','proyectos','fases','roles','mis_proyectos']
    __field_order__ =   ['name','apellido','email','usuario_name','_password','password','roles']
    __field_attrs__ =   {'roles':{'label_text':'Roles de Sistema:'}}
    
    estado          =   SingleSelectEstadosUsuarios
    email           =   TextField
    name            =   TextField('name',label_text='Nombre ')
    usuario_name    =   TextField('usuario_name',label_text='Nombre Usuario')
    
usuario_new_form    =   UsuarioNewForm(DBSession)
    
usuario_edit_filler =   UsuarioEditFiller(DBSession)   
usuario_edit_form   =   UsuarioEditForm(DBSession)
