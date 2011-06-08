$(function(){
	$("#faseNoIniVerTiposDeItemFlexi").flexigrid(
	{	
		url: '/configurar/tiposDeItem_asignados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Importar', bclass: 'import', onpress : doCommandTipoDeItem},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Tipos De Item de la fase: "+$('#fNombre').val() + " (No iniciada)",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});


function doCommandTipoDeItem(com, grid)
{
	if (com == 'Crear')
	{window.location = "/configurar/tiposDeItem/new/?fase_id="+$('input#fid').val();}
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
			var nombre = $('.trSelected',"#tiposDeItemAdministrarFlexi").find('td[abbr="name"]').children().text()	
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				if(confirm('Seguro que desea BORRAR el tipo de item: "' + nombre + '" ?'))
				{deleteTDI(id)}
			});
		}
		else
		{    	  jQuery.noticeAdd(
		    	  {
		              text: "Debe seleccionar una fila para borrar!",
		              stay: false,
		              stayTime: 5000,
		              type: 'notice'
		    	  });
		}
	}
	else if (com == 'Ver')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			var nombre = $('.trSelected',"#tiposDeItemAdministrarFlexi").find('td[abbr="name"]').children().text()	
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				window.location = location+'get_one/?id='+id
			});
		}
		else
		{    	  jQuery.noticeAdd(
		    	  {
		              text: "Debe seleccionar una fila para ver!",
		              stay: false,
		              stayTime: 5000,
		              type: 'notice'
		    	  });
		}
	}
}

function deleteTDI(id)
{
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
    	  $("#tiposDeItemAdministrarFlexi").flexReload();
      },
    });
}
