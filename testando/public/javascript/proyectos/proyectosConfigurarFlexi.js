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
			{name: 'Detalle Completo', bclass: 'viewAll', onpress : doCommandFases},
			{separator: true},		
			{name: 'Fases', bclass: 'viewPhases', onpress : doCommandFases},
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
		if (com == 'Detalle Completo')
			{detalle_completo(grid)}
		else if (com == 'Fases')
			{ver_fases(grid)}
		else if (com == 'Iniciar')
			{iniciar(grid)}
	}
	else
	{msg_falta_seleccion()}	
}

function detalle_completo(grid){
	$('.trSelected', grid).each(function()
	{
		id = get_id(this) 
		estado=get_estado()
		nombre=get_nombre()
		window.location = "/configurar/detalle_completo/?pid="+id
	});	
}

function ver_fases(grid){
		$('.trSelected', grid).each(function()
		{	
			id = get_id(this) 
			estado=get_estado()
			nombre=get_nombre()
			window.location = "/configurar/vista_de_fases/?pid="+id
		});	
}

function iniciar(grid){
	$('.trSelected', grid).each(function()
	{
		estado=get_estado()
		if (estado !=="Iniciado")
		{			
			id = get_id(this) 
			fases=get_si_no('fases')
			if (fases != "no")
			{
				usuarios=get_si_no('usuarios')
				if(usuarios != "no")
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

function iniciarP(id){
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

function get_si_no(objeto){
	result='no'
	if (objeto == 'usuarios'){
			result=$('.trSelected').find('td[abbr="usuarios"]').text();
	}
	else if (objeto == 'fases'){
		result=$('.trSelected').find('td[abbr="fases"]').text();
	}
	return result
}


function get_id(tr){
	var id = $(tr).attr('id');
	id = id.substring(id.lastIndexOf('row')+3);
	return id;
}

function get_nombre(){
	nombre=$('.trSelected').find('td[abbr="name"]').text();
	return nombre
}

function get_estado(grid){
	estado=$('.trSelected').find('td[abbr="estado"]').text();
	return estado
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