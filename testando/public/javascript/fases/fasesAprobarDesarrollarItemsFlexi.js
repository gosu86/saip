$(function(){
	$("#fasesAprobarDesarrollarItemsFlexi").flexigrid(
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
			{separator: true},{separator: true},{separator: true},			
			{name: 'Aprobar', bclass: 'approve', onpress : doCommandItem},
			{separator: true},{separator: true},{separator: true},
			{separator: true},{separator: true},{separator: true},
			{name: 'Historial de Items', bclass: 'items', onpress : doCommandItem},				
			{separator: true},
			{name: 'Calculo de Impacto', bclass: 'calculo', onpress : doCommandItem},
			{separator: true},	
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name'},
			{display: 'Codigo', name : 'codigo', isdefault: true}
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
	if (com=='Historial de Items'){
		window.location = "/configurar/vista_de_items/?fid="+$('input#fid').val()
	}	
	if ($('.trSelected', grid).length > 0)
	{	
			if (com == 'Aprobar')
			{
				obtener_ids(grid,'aprobar');
			}
			else if (com == 'Dar por terminado')
			{
				obtener_ids(grid,'terminar');
			}			
			else if (com == "Editar")
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
				else{
					$('.trSelected', grid).each(function()
					{
						id = get_id(this)
							window.location = '/desarrollar/items/index/?itemid='+id+'&fid='+$('input#fid').val();		
					});					
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
		if (tipo=='aprobar'){
			aprobar(ids)	
		}
		else if (tipo=='terminar'){
			terminar(ids)
		}
		
	}
function set_comprometida(id)
{
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/desarrollar/comprometer',
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
				  jQuery.noticeAdd(
				    	  {
				              text: 'Su linea base ha pasado al estado "Comprometida"',
				              stay: false,
				              stayTime: 2500,
				              type: data.type
				    	  });				    	  
				  $('#fasesAprobarDesarrollarItemsFlexi').flexReload();
    	    	 
    	      },
    	    });	
	
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
				  $('#fasesAprobarDesarrollarItemsFlexi').flexReload();
    	    	 
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
				  $('#fasesAprobarDesarrollarItemsFlexi').flexReload();
    	    	 
    	      },
    	    });	
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
				  $('#fasesAprobarDesarrollarItemsFlexi').flexReload();
    	    	 
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
function msg_comprometida(){
	jQuery.noticeAdd({
        text: "El item posee un linea base comprometida, No se puede editar.",
        stay: false,
        stayTime: 3000,
        type: "notice"
	  });	
}