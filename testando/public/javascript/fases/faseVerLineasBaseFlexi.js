$(function()
{
	$("#faseVerLineasBaseFlexi").flexigrid(
	{
		url: '/configurar/lineas_base/?fid='+$('input#faseId').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Fecha de creacion', name : 'fecha_creacion', width : 150, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{separator: true},{separator: true},{separator: true},
			{name: 'Abrir Linea Base', bclass: 'open', onpress : doCommandLineaBase},
			{separator: true},	
		],
		searchitems : [
		   			{display: 'Estado', name : 'estado'},
		   		],		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Lineas Base de la fase: "+$('input#faseNombre').val(),
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		showToggleBtn: true,
		width:'auto',
		height: 'auto',
		singleSelect: true,
	});
	
	$('#faseVerItemsAprobadosFlexi').flexigrid(
			{
				url: '/configurar/items_aprobados/?fid='+$('input#faseId').val(),
				dataType: 'json',
				
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 50, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 80, sortable : true, align: 'left'},
			{display: 'Tipo de Item', name : 'tipoitem', width : 150, sortable : true, align: 'left'},			
		],
				
				buttons : [
					{separator: true},
					{name: 'Aplicar Linea Base', bclass: 'baseline', onpress : doCommandLineaBase},
					{separator: true},
				],
				
				searchitems : [
					{display: 'Nombre', name : 'name', isdefault: true}
				],
				
				sortname: "id",
				sortorder: "asc",
				usepager: true,
				nowrap: false,
				title: "Items aprobados de la fase: "+$('input#faseNombre').val(),
				useRp: true,
				rp: 5,
				showTableToggleBtn: true,
				showToggleBtn: true,
				height: 'auto',
				singleSelect: false,
			});
	
});

function doCommandLineaBase(com, grid) {

	if ($('.trSelected', grid).length > 0)
	{	
		if (com=='Aplicar Linea Base')
		{
			obtener_ids(grid)
		}
		else if (com=='Ver Items')
		{
			
		}
		else if (com=='Abrir Linea Base')
		{
			id=get_id($('.trSelected', grid))
			abrir_linea_base(id)
		}
	}
	else
	{msg_falta_seleccion(com)}


} 

function get_id(tr){
	var id = $(tr).attr('id');
	id = id.substring(id.lastIndexOf('row')+3);
	return id;
}

function abrir_linea_base(id)
{
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/abrir_linea_base',
    	      data: {id:id},
    	      success: function(data)
    	      { 
				  jQuery.noticeAdd(
				    	  {
				              text: data.msg,
				              stay: false,
				              stayTime: 2500,
				              type: data.type
				    	  });
					  $("#faseVerLineasBaseFlexi").flexReload();
    	    	 
    	      },
    	    });		
}


function obtener_ids(grid){
		ids=''
		$('.trSelected', grid).each(function()
		{
			id = get_id(this) 
			ids=ids+(id+',')
		});
		aplicar_linea_base(ids)
	}

function aplicar_linea_base(ids)
{
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/aplicar_linea_base',
    	      data: {ids:ids},
    	      success: function(data)
    	      { 
					$('#faseVerItemsAprobadosFlexi').flexReload();
				  jQuery.noticeAdd(
				    	  {
				              text: data.msg,
				              stay: false,
				              stayTime: 2500,
				              type: data.type
				    	  });
					  $("#faseVerLineasBaseFlexi").flexReload();
    	    	 
    	      },
    	    });		
}	
function msg_falta_seleccion(com){
	if (com=='Aplicar Linea Base'){
		seleccionar=' un Item'
	}
	else{
		
		seleccionar=' una Linea Base'
	}
	jQuery.noticeAdd({
	              text: "Debe seleccionar almenos"+seleccionar+"!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}	
