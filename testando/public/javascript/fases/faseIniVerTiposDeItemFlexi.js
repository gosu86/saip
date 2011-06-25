$(function(){
	$("#faseNoIniVerTiposDeItemFlexi").flexigrid(
	{	
		url: '/configurar/tiposDeItem_asignados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
			{display: 'Campos Extras', name : 'camposExtras', width : 150, sortable : false, align: 'left'},			
		],
		
		buttons : [
			{separator: true},
			{name: 'Ver Tipos de Item del sistema', bclass: 'import', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Agregar Campos Extras', bclass: 'add', onpress : doCommandTipoDeItem},
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name'},
			{display: 'Codigo', name : 'codigo', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Tipos De Item de la fase: "+$('#fNombre').val() + " (Iniciada)",
		useRp: true,
		rp: 5,
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
							{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
							{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
							{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
							{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
							{display: 'Campos Extras', name : 'camposExtras', width : 150, sortable : true, align: 'left'},
							{display: 'Fase', name : 'faseName', width : 150, sortable : false, align: 'left'},
							{display: 'Proyecto', name : 'proyectoName', width : 150, sortable : false, align: 'left'},							
				],
				
				buttons : [
					{separator: true},
					{name: 'Importar a la fase', bclass: 'add', onpress : doCommandTipoDeItem},
				],
				
				searchitems : [
					{display: 'Nombre', name : 'name'},
					{display: 'Codigo', name : 'codigo', isdefault: true}
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
	if (com=='Ver Tipos de Item del sistema')
	{
		$('div.DeSistema .flexigrid').toggleClass('hideBody');
	}
	else if ($('.trSelected', grid).length > 0)
	{	
		if (com == 'Importar a la fase')
		{
			obtener_ids(grid,'importar')		
		}
		else if (com=='Agregar Campos Extras')
		{
			id = get_id($('.trSelected')) 
			agregar_campos_extras(id)
		}
	}
	else
	{msg_falta_seleccion()}
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
    	    	  $('#tiposDeItemListaFlexi').flexReload();
    	    	  if (data.msg.length > 1){
    	    	  jQuery.noticeAdd(
    	    	    	  {
    	    	              text: data.msg,
    	    	              stay: false,
    	    	              stayTime: 5000,
    	    	              type: data.type
    	    	    	  });
    	    	  }
    	    	  if (data.error.length > 1){
        	    	  jQuery.noticeAdd(
        	    	    	  {
        	    	              text: data.error,
        	    	              stay: false,
        	    	              stayTime: 5000,
        	    	              type: 'error'
        	    	    	  });    	    		  
    	    	  }
    	    	  $("#faseNoIniVerTiposDeItemFlexi").flexReload();
    	      },
    	    });
}

function agregar_campos_extras(tr)
{
	window.location = '/configurar/tiposDeItem/'+id+"/edit/?camposExtras=true";
}

function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar un tipo de item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}