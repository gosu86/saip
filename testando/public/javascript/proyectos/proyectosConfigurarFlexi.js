$(function()
{
	$("#proyectosConfigurarFlexi").flexigrid(
	{
		url: '/configurar/lista_de_proyectos/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Empresa', name : 'empresa', width : 150, sortable : false, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'center'},
			{display: 'Fases', name : 'fases', width : 40, sortable : true, align: 'center'},
			{display: 'Usuarios', name : 'usuarios', width : 40, sortable : true, align: 'center'}
		],

		buttons : [
			{separator: true},         
			{name: 'Ver Detalle Completo', bclass: 'viewAll', onpress : doCommandFases},
			{separator: true},
			{name: 'Asignar Usuarios', bclass: 'addUsers', onpress : doCommandFases},
			{separator: true},			
			{name: 'Ver Usuarios', bclass: 'viewUsers', onpress : doCommandFases},
			{separator: true},
			{name: 'Asignar Fases', bclass: 'addPhases', onpress : doCommandFases},
			{separator: true},			
			{name: 'Ver Fases', bclass: 'viewPhases', onpress : doCommandFases},
			{separator: true},
			{name: 'Iniciar', bclass: 'start', onpress : doCommandFases},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Seleccion de Proyectos",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});
function doCommandFases(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
		if (com == 'Asignar Fases')
			{asignar_fases(grid)}
		else if (com == 'Ver Fases')
			{ver_fases(grid)}
		else if (com == 'Iniciar')
			{iniciar(grid)}
	}
	else
	{msg_falta_seleccion()}	
}

function asignar_fases(grid){
	estado=$('.trSelected', grid).find('td[abbr="estado"]').text()
	if (estado != "Iniciado")
	{
		$('.trSelected', grid).each(function()
		{
			var id = $(this).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			window.location = "/configurar/asignacion_de_fases/"+id
		});	
	}
	else
	{	
		msg_proyecto_ya_iniciado()
		msg_no_asignar()
	}
}

function ver_fases(grid){
	fases=$('.trSelected',grid).find('td[abbr="fases"]').text()
	if (fases == "si")
	{
		$('.trSelected', grid).each(function()
		{
			var id = $(this).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			window.location = "/configurar/vista_de_fases/"+id
		});	
	}
	else
	{msg_no_posee_fases();}
}

function iniciar(grid){
	$('.trSelected', grid).each(function()
	{
		estado=$('.trSelected',grid).find('td[abbr="estado"]').text()
		if (estado !=="Iniciado")
		{			
			var id = $(this).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			fases=$('.trSelected',grid).find('td[abbr="fases"]').text()
			if (fases == "si")
			{
				usuarios=$('.trSelected',grid).find('td[abbr="usuarios"]').text()
				if(usuarios == "si")
				{iniciarP(id)}
				else
				{				
					msg_no_posee_usuarios();
					msg_no_iniciar()
				}
		
			}
			else
			{
				msg_no_posee_fases();
				msg_no_iniciar()
			}
		}
		else
		{msg_proyecto_ya_iniciado()}
	});
}

function iniciarP(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/iniciar_proyecto",
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
    	  
    	  $("#proyectosConfigurarFlexi").flexReload();
    	  
      },
    });
}

function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar un proyecto!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}

function msg_no_posee_fases(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto seleccionado no posee fases",
	              stay: false,
	              stayTime: 2000,
	              type: "notice"
	    	  });	
}

function msg_no_posee_usuarios(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto seleccionado no posee usuarios",
	              stay: false,
	              stayTime: 2000,
	              type: "notice"
	    	  });	
}

function msg_proyecto_ya_iniciado(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto seleccionado ya se encuentra iniciado",
	              stay: false,
	              stayTime: 2000,
	              type: "notice"
	    	  });	
}

function msg_no_iniciar(){
	jQuery.noticeAdd(
	    	  {
	              text: "El proyecto no se puede iniciar.",
	              stay: false,
	              stayTime: 3000,
	              type: "error"
	    	  });	
}
function msg_no_asignar(){
	jQuery.noticeAdd(
	    	  {
	              text: "No se pueden asignar fases.",
	              stay: false,
	              stayTime: 3000,
	              type: "error"
	    	  });	
}