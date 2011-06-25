from tw.forms import SingleSelectField
from tw.forms import InputField
class HiddenField(InputField):
    type = "hidden"
hideMe=HiddenField    

class SingleSelectEstadosProyectos(SingleSelectField):
    options         = ['Activo', 'Eliminado']

class SingleSelectEstadosFases(SingleSelectField):
    options         = ['Activa', 'Iniciada','Terminada', 'Eliminada']
    
class SingleSelectEstadosUsuarios(SingleSelectField):
    options         = ['Activo', 'Inactivo', 'Eliminado']    