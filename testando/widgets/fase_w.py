from sprox.dojo.formbase    import DojoEditableForm,DojoAddRecordForm
from sprox.formbase    import EditableForm,AddRecordForm
from sprox.fillerbase       import EditFormFiller

from testando.model         import DBSession
from testando.model.fase    import Fase

from tw.forms import TextField,TextArea, HiddenField
from tw.forms.validators import Int, NotEmpty, DateConverter
from formencode import validators
from formencode.compound import All
from myWidgets import SingleSelectEstadosFases

class FaseNewForm(AddRecordForm):
    __model__       = Fase
    __omit_fields__ = ['estado','fecha_creacion', 'tiposDeItem','usuarios','items']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'50'},'name':{'label':'Nombre:'},'orden':{'readonly':'true'}}
    
    orden       =   TextField('orden',size=5,disabled="",validator=All(
                                                validators.Int(messages={'integer': 'Orden debe ser un numero entero.'})))
    name        =   TextField
    proyecto    = HiddenField('proyecto_id')

    submit_text = "Guardar"
    
class FaseEditFiller(EditFormFiller):
    __model__ = Fase
   
class FaseEditForm(DojoEditableForm):
    __model__       = Fase
    __omit_fields__ = ['estado','fecha_creacion', 'tiposDeItem','usuarios','items']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'50'},'name':{'label':'Nombre:'}}
    
    orden       =   TextField('orden',size=5,disabled="true")
    proyecto = HiddenField
    name = TextField
    estado = SingleSelectEstadosFases
    
fase_new_form = FaseNewForm(DBSession)
fase_edit_filler=FaseEditFiller(DBSession)    
fase_edit_form=FaseEditForm(DBSession)