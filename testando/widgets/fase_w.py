from sprox.dojo.formbase    import DojoEditableForm,DojoAddRecordForm
from sprox.fillerbase       import EditFormFiller

from testando.model         import DBSession
from testando.model.fase    import Fase

from tw.forms import TextField,TextArea, HiddenField
from tw.forms.validators import Int, NotEmpty, DateConverter
from formencode import validators
from formencode.compound import All
from myWidgets import SingleSelectEstadosFases

class FaseNewForm(DojoAddRecordForm):
    __model__       = Fase
    __omit_fields__ = ['estado','fecha_creacion', 'tipos_item','usuarios','items']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'30'}}
    orden   =   TextField('orden',validator=All(
                                                validators.Int(messages={'integer': 'Orden debe ser un numero entero.'}),
                                                validators.NotEmpty(messages={'empty': 'Orden no puede estar vacio.'})))
    name    =   TextField('name',label_text='Nombre')
    proyecto = HiddenField('proyecto_id')
    descripcion = TextArea

class FaseEditFiller(EditFormFiller):
    __model__ = Fase
   
class FaseEditForm(DojoEditableForm):
    __model__       = Fase
    __omit_fields__ = ['estado','fecha_creacion', 'tipos_item','usuarios','items']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'30'}}
    proyecto = HiddenField
    name = TextField
    estado = SingleSelectEstadosFases
    
fase_new_form = FaseNewForm(DBSession)
fase_edit_filler=FaseEditFiller(DBSession)    
fase_edit_form=FaseEditForm(DBSession)