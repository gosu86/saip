$(function(){
	$("#fasesDesarrollarItemsFlexi").flexigrid(
	{	
		url: '/desarrollar/items_creados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 150, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
			{display: 'Tipo De Item', name : 'tipoDeItem', width : 150, sortable : true, align: 'left'},			
		],
		
		buttons : [	           
			{separator: true},
			{name: 'Editar', bclass: 'edit_item', onpress : doCommandItem},
			{separator: true},
			{separator: true},
			{separator: true},
			{name: 'Adjuntar', bclass: 'file', onpress : doCommandItem},
			{separator: true},
			{separator: true},
			{separator: true},			
			{name: 'Borrar', bclass: 'delete_item', onpress : doCommandItem},
			{separator: true},
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Desarrollo de Items",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
	$('div.DeFase .flexigrid').addClass('hideBody');	
});


function doCommandItem(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
			if (com == 'Editar')
			{
			
				$('.trSelected', grid).each(function()
				{
					id = get_id(this) 
					window.location = '/desarrollar/items/'+id+'/edit/';
				});
			}
			else if (com == 'Adjuntar')
			{
			
				$('.trSelected', grid).each(function()
				{
					id = get_id(this) 
					window.location = '/desarrollar/items/index/?itemid='+id;
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
	              text: "Debe seleccionar al menos un item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}