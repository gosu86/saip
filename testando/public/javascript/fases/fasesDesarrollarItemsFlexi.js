$(function(){
	$("#fasesDesarrollarItemsFlexi").flexigrid(
	{	
		url: '/desarrollar/fases/items_creados/?fid='+$('input#fid').val(),
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
			{name: 'Editar', bclass: 'edit_item', onpress : doCommandItem},
			{separator: true},{separator: true},{separator: true},
			{name: 'Adjuntos', bclass: 'attachment', onpress : doCommandItem},
			{separator: true},{separator: true},{separator: true},
			{separator: true},{separator: true},{separator: true},	
			{name: 'Dar por terminado', bclass: 'finish', onpress : doCommandItem},
			{separator: true},{separator: true},{separator: true},
			{separator: true},{separator: true},{separator: true},			
			{name: 'Borrar', bclass: 'delete_item', onpress : doCommandItem},
			{separator: true},{separator: true},{separator: true},
			{separator: true},{separator: true},{separator: true},
			{name: 'Historial', bclass: 'items', onpress : doCommandItem},			
			{separator: true},
			{name: 'Calculo de Impacto', bclass: 'calculo', onpress : doCommandItem},
			{separator: true},	
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Codigo', name : 'codigo', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Desarrollo de Items",
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
	if (com=='Historial'){
		window.location = "/desarrollar/items/vista_de_historial/?iid="+get_id($('.trSelected', grid))
	}
	
	if ($('.trSelected', grid).length > 0)
	{	
			if (com == 'Dar por terminado')
			{
				obtener_ids(grid,'terminar');
			}		
			else if (com == 'Editar')
			{
				if ($('.trSelected', grid).length > 1)
				{
					msg_toManySelected('editar')
				}
				else
				{
					$('.trSelected', grid).each(function()
					{
						id = get_id(this) 
						lb = $('tr.trSelected td:last').children().text()
						
						if (lb == 'Activa')
						{
							alert(lb)
							set_comprometida(id)
						}
						else if (lb == 'Comprometida')
						{
							msg_comprometida()
						}
						else{
								window.location = '/desarrollar/items/'+id+'/edit/';
							}
					});			
				}
			}
			else if (com == 'Adjuntos')
			{
				if ($('.trSelected', grid).length > 1)
				{
					msg_toManySelected('ver adjuntos de')
				}
				else
				{
					id = get_id($('.trSelected', grid)) 
					window.location = '/desarrollar/items/impacto/?itemid='+id+'&fid='+$('input#fid').val();
				}
			}
			else if (com == 'Calculo de Impacto')
			{
				if ($('.trSelected', grid).length > 1)
				{
					msg_toManySelected('Calcular el Impacto de')
				}
				else{
					$('.trSelected', grid).each(function()
					{
						id = get_id(this)
							window.location = '/desarrollar/items/impacto/?itemid='+id;		
					});					
				}			

			}
			else if (com == 'Borrar')
			{
				if ($('.trSelected', grid).length > 1)
				{
					msg_toManySelected('borrar')
				}
				else
				{
					id = get_id($('.trSelected', grid)) 
					borrar(id)
				}
			}
	}
	else
	{msg_falta_seleccion()}

}

function obtener_ids(grid,tipo){
		ids=''
		$('.trSelected', grid).each(function()
		{
			id = get_id(this) 
			ids=ids+(id+',')
		});
		if (tipo=='terminar'){
			terminar(ids)
		}
		
	}

function borrar(id){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/desarrollar/eliminar_item',
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
				  $('#fasesDesarrollarItemsFlexi').flexReload();
    	    	 
    	      },
    	    });	
}

function terminar(ids){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/desarrollar/terminar',
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
					}
				  $('#fasesDesarrollarItemsFlexi').flexReload();
    	    	 
    	      },
    	    });	
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
function msg_toManySelected(que){
	jQuery.noticeAdd({
        text: "Ha seleccionado más de un item!",
        stay: false,
        stayTime: 2500,
        type: "error"
	  });
	jQuery.noticeAdd({
        text: "Solo puede "+que+" un item a la vez.",
        stay: false,
        stayTime: 3000,
        type: "notice"
	  });	
}