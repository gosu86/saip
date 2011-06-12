$(function(){
	$("#fasesDesarrollarTiposDeItemFlexi").flexigrid(
	{	
		url: '/desarrollar/tiposDeItem_asignados/?fid='+$('input#fid').val(),
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
			{name: 'Crear Item de este tipo', bclass: 'add', onpress : doCommandTipoDeItem},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Tipos De Item de la fase: "+$('#fNombre').val(),
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
	$('div.DeFase .flexigrid').addClass('hideBody');	
});


function doCommandTipoDeItem(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
			if (com == 'Crear Item de este tipo')
			{
			
				$('.trSelected', grid).each(function()
				{
					id = get_id(this) 
					window.location = '/desarrollar/items/new/?tdiid='+id;
				});
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
	              text: "Debe seleccionar un tipo de item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}