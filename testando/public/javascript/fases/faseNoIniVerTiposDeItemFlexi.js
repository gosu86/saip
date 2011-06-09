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
			{display: 'Campos Extras', name : 'camposExtras', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Ver Tipos de Item del sistema', bclass: 'import', onpress : doCommandTipoDeItem},
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
	$('#tiposDeItemListaFlexi').flexigrid(
			{
				url: '/configurar/tiposDeItem_del_sistema/?fid='+$('input#fid').val(),
				dataType: 'json',
				
				colModel : [
							{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
							{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
							{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
							{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
							{display: 'Campos Extras', name : 'camposExtras', width : 150, sortable : true, align: 'left'},
				],
				
				buttons : [
					{separator: true},
					{name: 'Importar a la fase', bclass: 'add', onpress : doCommandTipoDeItem},
				],
				
				searchitems : [
					{display: 'Nombre', name : 'name', isdefault: true}
				],
				
				sortname: "id",
				sortorder: "asc",
				usepager: true,
				nowrap: false,
				title: "Tipos de Items del Sistema",
				useRp: true,
				rp: 5,
				showTableToggleBtn: true,
				showToggleBtn: true,
				height: 'auto',
				singleSelect: false,
			});
	$('div.DeSistema .flexigrid').addClass('hideBody');	
});


function doCommandTipoDeItem(com, grid)
{
	if (com == 'Crear')
	{window.location = "/configurar/tiposDeItem/new/?fase_id="+$('input#fid').val();}
	else if (com=='Ver Tipos de Item del sistema')
	{
		$('div.DeSistema .flexigrid').toggleClass('hideBody');
	}
	else if ($('.trSelected', grid).length > 0)
	{	
		if (com == 'Editar')
		{
		
			$('.trSelected', grid).each(function()
			{
				id = get_id(this) 
				window.location = '/configurar/tiposDeItem/'+id+"/edit/";
			});
		
		}
		else if (com == 'Borrar') 
		{
			$('.trSelected', grid).each(function()
			{
				id = get_id(this) 
				nombre=get_nombre()
				
				if(confirm('Seguro que desea BORRAR el tipo de item: "' + nombre + '" ?'))
					{deleteTDI(id)}
			});
		}
		else if (com == 'Importar a la fase')
		{
			obtener_ids(grid,'importar')		
		}
	}
	else
	{msg_falta_seleccion()}
}

function deleteTDI(id)
{
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/tiposDeItem/post_delete",
      data: {id:id},
      success: function(data)
      {	
    	  $('#tiposDeItemListaFlexi').flexReload();
    	  jQuery.noticeAdd(
    	    	  {
    	              text: data.msg,
    	              stay: false,
    	              stayTime: 5000,
    	              type: data.type
    	    	  });    	  
    	  $("#faseNoIniVerTiposDeItemFlexi").flexReload();
      },
    });
}
function get_id(tr){
	var id = $(tr).attr('id');
	id = id.substring(id.lastIndexOf('row')+3);
	return id;
}

function get_nombre(){
	nombre=$('.trSelected').find('td[abbr="name"]').text();
	return nombre
}

function obtener_ids(grid,tipo){
	faseId=$('input#fid').val();
	ids=faseId+','
	$('.trSelected', grid).each(function()
	{
		id = get_id(this) 
		ids=ids+(id+',')
	});
	if (tipo=='importar')
	{importar_tiposDeItem(ids)}
}
function importar_tiposDeItem(ids)
{
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: "/configurar/fases/importar_TiposDeItem",
    	      data: {ids:ids},
    	      success: function(data)
    	      {
    	    	  jQuery.noticeAdd(
    	    	    	  {
    	    	              text: data.msg,
    	    	              stay: false,
    	    	              stayTime: 5000,
    	    	              type: data.type
    	    	    	  });    	  
    	    	  $("#faseNoIniVerTiposDeItemFlexi").flexReload();
    	      },
    	    });
}

function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar una Fase!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}