$(function(){
	$("#fasesAprobarItemsFlexi").flexigrid(
	{	
		url: '/desarrollar/items_creados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 50, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 80, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 80, sortable : true, align: 'left'},
			{display: 'Tipo De Item', name : 'tipoDeItem', width : 150, sortable : true, align: 'left'},
			{display: 'Linea Base', name : 'lineaBase', width : 150, sortable : true, align: 'left'},		
		],
		
		buttons : [
			{separator: true},
			{name: 'Aprobar', bclass: 'approve', onpress : doCommandItem},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name'},
			{display: 'Codigo', name : 'codigo', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Aprobacion de Items",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: false
	});
	$('div.DeFase .flexigrid').addClass('hideBody');	
});


function doCommandItem(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
			if (com == 'Aprobar')
			{
				obtener_ids(grid)
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

function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar almenos un item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}

function obtener_ids(grid){
		ids=''
		$('.trSelected', grid).each(function()
		{
			id = get_id(this) 
			ids=ids+(id+',')
		});
		aprobar(ids)
	}
	
function aprobar(ids){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/desarrollar/aprobar',
    	      data: {ids:ids},
    	      success: function(data)
    	      { 

				  jQuery.noticeAdd(
				    	  {
				              text: data.msg,
				              stay: false,
				              stayTime: 2500,
				              type: data.type
				    	  });
					if (data.error != 0){
						  jQuery.noticeAdd(
						    	  {
						              text: data.error,
						              stay: false,
						              stayTime: 2500,
						              type: 'error'
						    	  });
						  jQuery.noticeAdd(
						    	  {
						              text: 'Solo items "terminados", pueden ser aprobados... ',
						              stay: false,
						              stayTime: 2500,
						              type: 'notice'
						    	  });										    	  
					}
				  $('#fasesAprobarItemsFlexi').flexReload();
    	    	 
    	      },
    	    });	
}