$(function()
{
	$("#proyectoVerFasesFlexi").flexigrid(
	{
		url: '/configurar/proyectos/fases_asignadas/?pid='+$('input#pid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},			
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 50, sortable : true, align: 'left'},
			{display: 'Usuarios', name : 'usuarios', width : 50, sortable : false, align: 'left'},
			{display: 'Tipos de Items', name : 'tiposdeitem', width : 80, sortable : false, align: 'left'},
			{display: 'Items', name : 'items', width : 50, sortable : false, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandFases},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandFases},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandFases},
			{separator: true},
			{separator: true},		           
			{separator: true},			
			{separator: true},
			{separator: true},		           
			{separator: true},
			{name: 'Usuarios', bclass: 'users', onpress : doCommandFases},
			{separator: true},
			{name: 'Tipos de Items', bclass: 'itemtypes', onpress : doCommandFases},	
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Fases del proyecto: "+$('#proyectoNombre').val() + " (No iniciado)",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		showToggleBtn: true,
		height: 'auto',
		singleSelect: true,
	});
});

function doCommandFases(com, grid) {
	if (com == 'Crear')
	{window.location = "/configurar/fases/new/?proyecto_id="+$('input#pid').val();}
	else if ($('.trSelected', grid).length > 0)
	{	id=get_ids(grid)[0]
		if (com == 'Editar')
		{window.location = '/configurar/fases/'+id+"/edit/";}
		else if (com == 'Borrar') 
		{
			if(confirm('Seguro que desea BORRAR la fase?'))
			{deleteF(id);}
		}
		else if (com == 'Usuarios')
		{window.location = "/configurar/vista_de_usuarios/?fid="+id}		
		else if (com == 'Tipos de Items')
		{window.location = "/configurar/vista_de_tiposDeItem/?fid="+id}
	}
	else
	{notify("Debe seleccionar una Fase!")}
} 

function deleteF(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/fases/post_delete",
      data: {id:id},
      success: function(data)
      {
    	  if(data.borrada){notify("Fase borrada con exito!","succes")}
    	  else{notify("La fase no se puede borrar, La fase esta iniciada")}    	  
    	  $("#proyectoVerFasesFlexi").flexReload();
      },
    });
}