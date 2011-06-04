$(function()
{
	$("#permisosAdministrarFlexi").flexigrid(
	{
		url: location+'fetch/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'permiso_name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},
			{display: 'Roles al que pertenece', name : 'roles', width : 150, sortable : false, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandPermiso},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandPermiso},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandPermiso},
			{separator: true}
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Permisos",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		resizable: false,
		height: 'auto',
		singleSelect: true
	});
});

function deletePER(id) {
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
    	              stayTime: 3000,
    	              type: data.type
    	    	  });    	  
    	  $("#permisosAdministrarFlexi").flexReload();
      },
    });
}


function doCommandPermiso(com, grid)
{
	if (com == 'Crear')
	{window.location = location+"new/";}
	else if (com == 'Editar')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				window.location = location+id+"/edit/"
			});
		}
		else
		{alert("Debe seleccionar una fila para editar!");}
	}
	else if (com == 'Borrar') 
	{
		if ($('.trSelected', grid).length > 0)
		{
			var nombre = $('.trSelected',"#permisosAdministrarFlexi").find('td[abbr="permiso_name"]').children().text()	
			$('.trSelected', grid).each(function() {
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				if(confirm('Seguro que desea BORRAR el permiso: "' + nombre + '" ?'))
				{deletePER(id)}
			});
		}
		else
		{
			jQuery.noticeAdd(
			    	  {
			              text: "Debe seleccionar una fila para borrar!",
			              stay: false,
			              stayTime: 5000,
			              type: "notice"
			    	  });			
		}
	}
}