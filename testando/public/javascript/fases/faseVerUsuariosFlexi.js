$(function()
{
	$("#faseVerUsuariosFlexi").flexigrid(
	{
		url: '/configurar/fases/usuarios_asignados/?fid='+$('input#faseId').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Rol', name : 'rol', width : 350, sortable : true, align: 'center'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Agregar Usuarios', bclass: 'add_users', onpress : doCommandUsuarios},
			{separator: true},	
			{separator: true},
			{separator: true},
			{name: 'Quitar de la Fase', bclass: 'delete_users', onpress : doCommandUsuarios},
			{separator: true},	
			{separator: true},
			{separator: true},
			{name: 'Cambiar Rol', bclass: 'switch_rol', onpress : doCommandUsuarios},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Usuarios de la fase: "+$('input#faseNombre').val(),
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		showToggleBtn: true,
		width:'auto',
		height: 'auto',
		singleSelect: false,
	});
	
	$('#usuariosListaFlexi').flexigrid(
			{
				url: '/configurar/usuarios_del_sistema/?fid='+$('input#faseId').val(),
				dataType: 'json',
				
				colModel : [
					{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
					{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
					{display: 'Rol', name : 'rol', width : 350, sortable : true, align: 'center'},
				],
				
				buttons : [
					{separator: true},
					{name: 'Agregar a la Fase', bclass: 'add', onpress : doCommandUsuarios},
				],
				
				searchitems : [
					{display: 'Nombre', name : 'name', isdefault: true}
				],
				
				sortname: "id",
				sortorder: "asc",
				usepager: true,
				nowrap: false,
				title: "Usuarios del Sistema",
				useRp: true,
				rp: 5,
				showTableToggleBtn: true,
				showToggleBtn: true,
				height: 'auto',
				singleSelect: false,
			});
	$('div.DeSistema .flexigrid').addClass('hideBody');
	
});

function doCommandUsuarios(com, grid) {
	if (com == 'Agregar Usuarios')
	{
			$('div.DeSistema .flexigrid').toggleClass('hideBody');
	}	
	else if ($('.trSelected', grid).length > 0)
	{
		if (com == 'Agregar a la Fase')
		{
				obtener_ids(grid,'agregar');
		}
		else if (com == 'Quitar de la Fase')
		{
				obtener_ids(grid,'quitar');
		}		
		else if (com == 'Cambiar Rol')
		{
				obtener_ids(grid,'cambiar');
		}
	}
	else
	{msg_falta_seleccion();}
	


} 


function obtener_ids(grid,tipo){
		faseId=$('input#faseId').val();
		ids=''
		idsyroles=''
		ids=faseId+','
		idsyroles=faseId+';'
		$('.trSelected', grid).each(function()
		{
			id = get_id(this) 
			ids=ids+(id+',')
			rol=$('select#'+id).val()
			idsyroles=idsyroles+(id+','+rol+';')
		});
		if (tipo=='agregar')
		{agregar_usuarios(idsyroles)}
		else if(tipo=='quitar')
		{quitar_usuarios(ids)}
		else if (tipo=='cambiar')
		{cambiar_roles(idsyroles)}
}

function agregar_usuarios(idsyroles) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: '/configurar/fases/agregar_usuarios',
      data: {idsyroles:idsyroles},
      success: function(data)
      { 
    	  if (data.reload){
    		  location.reload(true);	  
    	  }
    	  else
    	  {
        	  $("#faseVerUsuariosFlexi").flexReload();
        	  jQuery.noticeAdd(
        	    	  {
        	              text: data.msg,
        	              stay: false,
        	              stayTime: 2500,
        	              type: data.type
        	    	  });
        		  
        	  $('#usuariosListaFlexi').flexReload();
    	  }
    	 
      },
    });
}
function quitar_usuarios(ids) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: '/configurar/fases/quitar_usuarios',
      data: {ids:ids},
      success: function(data)
      { 
    	  
    	  if (data.reload){
    		  location.reload(true);	  
    	  }
    	  else
    	  {    	  
	    	  $("#faseVerUsuariosFlexi").flexReload();
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: data.msg,
	    	              stay: false,
	    	              stayTime: 2500,
	    	              type: data.type
	    	    	  });
	    	  if (data.msg_p.length > 1)
	    	  {
	        	  jQuery.noticeAdd(
	        	    	  {
	        	              text: data.msg_p,
	        	              stay: false,
	        	              stayTime: 4500,
	        	              type: 'notice'
	        	    	  });    		  
	    	  }    	  
	    	  $('#usuariosListaFlexi').flexReload();
    	  }
    	 
      },
    });
}
function cambiar_roles(idsyroles){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/cambiar_roles',
    	      data: {idsyroles:idsyroles},
    	      success: function(data)
    	      { 
    	    	  $("#faseVerUsuariosFlexi").flexReload();
    	    	  jQuery.noticeAdd(
    	    	    	  {
    	    	              text: data.msg,
    	    	              stay: false,
    	    	              stayTime: 2500,
    	    	              type: data.type
    	    	    	  });
    	    		  
    	    	  $('#usuariosListaFlexi').flexReload();
    	    	 
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
	              text: "Debe seleccionar al menos un usuario!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}