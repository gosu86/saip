$(function()
{
	$("#faseVerUsuariosFlexi").flexigrid(
	{
		url: '/configurar/fases/usuarios_asignados/?fid='+$('input#faseId').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Permiso', name : 'rol', width : 350, sortable : true, align: 'center'},
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
			{name: 'Cambiar Permisos', bclass: 'switch_rol', onpress : doCommandUsuarios},
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
					{display: 'Permiso', name : 'rol', width : 350, sortable : true, align: 'center'},
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
	{$('div.DeSistema .flexigrid').toggleClass('hideBody');}	
	else if ($('.trSelected', grid).length > 0)
	{
		if (com == 'Agregar a la Fase')
		{obtener_ids(grid,'agregar');}
		else if (com == 'Quitar de la Fase')
		{obtener_ids(grid,'quitar');}		
		else if (com == 'Cambiar Permisos')
		{obtener_ids(grid,'cambiar');}
	}
	else
	{notify("Debe seleccionar al menos un usuario!");}
} 

function obtener_ids(grid,tipo){
		ids=get_ids(grid)	
		faseId=$('input#faseId').val();
		if(tipo=='quitar')
		{ids.push(faseId);quitar_usuarios(ids)}		
		else{
			idsyroles=[]
			for(i=0;i<ids.length;i++){
				rol=$('select#'+ids[i]).val()
				idsyroles.push(ids[i]+','+rol)
			}			
			idsyroles.push(faseId);
			if (tipo=='agregar')
			{agregar_usuarios(idsyroles)}
			else if (tipo=='cambiar')
			{cambiar_roles(idsyroles)}
		}
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
    	  if (data.reload)
    	  {location.reload(true);}
    	  else
    	  {	  $("#faseVerUsuariosFlexi").flexReload();
    		  notify(data.cantidad+" usuarios agregados con exito.","succes");
        	  $('#usuariosListaFlexi').flexReload();
    	  } 
      },
    });
}
function quitar_usuarios(ids) {
    $.ajax({
      type: 'POST',
      dataType: "json",
      url: '/configurar/fases/quitar_usuarios',
      data: {ids:ids},
      success: function(data)
      { 
    	  if (data.reload)
    	  {location.reload(true);}
    	  else
    	  {    	  
	    	  $("#faseVerUsuariosFlexi").flexReload();
	    	  notify(data.quitados +" usuarios quitados con exito.","succes")
	    	  if (data.fuera_del_proyecto >0){
	    		  notify(data.fuera_del_proyecto + " usuarios ya no forman parte del proyecto")
	    	  }
	    	  $('#usuariosListaFlexi').flexReload();
    	  }
      },
    });
}
function cambiar_roles(idsyroles){
    $.ajax({
	  type: 'POST',
	  dataType: "json",
	  url: '/configurar/cambiar_roles',
	  data: {idsyroles:idsyroles},
	  success: function(data)
	  { 
		  $("#faseVerUsuariosFlexi").flexReload();
		  notify(data.cantidad+" permisos cambiados con exito.","succes")
		  $('#usuariosListaFlexi').flexReload();
	  },
	});	
}