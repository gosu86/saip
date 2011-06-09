$(function()
{
	$("#proyectosAdministrarFlexi").flexigrid(
	{
		url: location+'lista_de_proyectos/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Lider', name : 'lider', width : 150, sortable : false, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Fases', name : 'fases', width : 150, sortable : false, align: 'left'}
		],
		
		buttons : [
			{separator: true},         
			{name: 'Crear', bclass: 'add', onpress : doCommandProyecto},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandProyecto},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandProyecto},
			{separator: true}
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Proyectos",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});

function doCommandProyecto(com, grid)
{
	if (com == 'Crear') 
	{window.location = location+"new/";}
	else{
		if ($('.trSelected', grid).length > 0){
			if (com == 'Editar')
			{editar(grid)}
			else if (com == 'Borrar') 
			{borrar(grid)}
		}
		else
		{msg_falta_seleccion()}
	}
}

function deleteP(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: location+"/post_delete",
      data: {id:id},
      success: function(data)
      {
    	  jQuery.noticeAdd(
    	  {
              text: data.msg,
              stay: false,
              stayTime: 5000,
              type: data.type
    	  });
    	  
    	  $("#proyectosAdministrarFlexi").flexReload();
    	  
      },
    });
}

function editar(grid)
{
	$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				window.location = location+id+"/edit/"
			});
}

function borrar(grid)
{
		var nombre = $('.trSelected',"#proyectosAdministrarFlexi").find('td[abbr="name"]').children().text()
		var estado = $('.trSelected',"#proyectosAdministrarFlexi").find('td[abbr="estado"]').children().text()
		if (estado !== "Iniciado")
		{
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				if(confirm('Seguro que desea BORRAR el proyecto: "' + nombre + '" ?'))
				{deleteP(id)}
			});
		}
		else
		{
			msg_proyecto_ya_iniciado();
			msg_no_borrar();
		}

}
function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar un proyecto!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}

function msg_proyecto_ya_iniciado(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto seleccionado se encuentra iniciado",
	              stay: false,
	              stayTime: 2000,
	              type: "notice"
	    	  });	
}

function msg_no_borrar(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto no se puede borrar.",
	              stay: false,
	              stayTime: 3000,
	              type: "error"
	    	  });	
}