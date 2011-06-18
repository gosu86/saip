$(function(){
	$("#fasesAprobarDesarrollarItemsFlexi").flexigrid(
	{	
		url: '/desarrollar/items_creados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 150, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 150, sortable : true, align: 'left'},
			{display: 'Campos Extras', name : 'camposExtras', width : 150, sortable : true, align: 'left'},			
		],
		
		buttons : [          
			{separator: true},
			{name: 'Editar', bclass: 'edit_item', onpress : doCommandItem},
			{separator: true},
			{separator: true},
			{separator: true},
			{name: 'Borrar', bclass: 'delete_item', onpress : doCommandItem},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},			
			{name: 'Aprobar', bclass: 'approve', onpress : doCommandItem},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Desarrollo y Aprobacion de Items",
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
			
				$('.trSelected', grid).each(function()
				{
					id = get_id(this) 
					jQuery.noticeAdd({
			              text: "Aprobar: "+id,
			              stay: false,
			              stayTime: 2500,
			              type: "notice"
			    	  });
				});
			}
			else if (com == "Editar")
			{
				if ($('.trSelected', grid).length > 1)
				{
					msg_toManySelected()
				}
				else
				{
					$('.trSelected', grid).each(function()
							{
								id = get_id(this) 
								window.location = '/desarrollar/items/'+id+'/edit/';
							});			
				}
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

function msg_toManySelected(){
	jQuery.noticeAdd({
        text: "Ha seleccionado más de un item!",
        stay: false,
        stayTime: 2500,
        type: "error"
	  });
	jQuery.noticeAdd({
        text: "Solo puede editar un item a la vez.",
        stay: false,
        stayTime: 3000,
        type: "notice"
	  });	
}