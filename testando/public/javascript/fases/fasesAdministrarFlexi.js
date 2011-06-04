$(function()
{
	$("#fasesAdministrarFlexi").flexigrid(
	{
		url: location+'lista_de_fases/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 150, sortable : true, align: 'left'}
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
		title: "Lista de Fases",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});
function deleteF(id) {
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
    	  
    	  $("#fasesAdministrarFlexi").flexReload();
      },
    });
}


function doCommandProyecto(com, grid) {
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
				window.location = location+id+"/edit/"}
			);
		}
		else
		{alert("Debe seleccionar una fila para editar!");}
	}
	else if (com == 'Borrar') 
	{
		if ($('.trSelected', grid).length > 0)
		{
			var nombre = $('.trSelected',"#fasesAdministrarFlexi").find('td[abbr="name"]').children().text()	
			$('.trSelected', grid).each(function() {
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				if(confirm('Seguro que desea BORRAR la fase: "' + nombre + '" ?'))
				{deleteF(id)}
			});
		}
		else
		{			jQuery.noticeAdd(
		    	  {
		              text: "Debe seleccionar una fila para borrar!",
		              stay: false,
		              stayTime: 5000,
		              type: "notice"
		    	  });
		}
	}
}