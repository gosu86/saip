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
			{display: 'Fases', name : 'fases', width : 40, sortable : false, align: 'center'},
			{display: 'Usuarios', name : 'usuarios', width : 40, sortable : false, align: 'center'}
		],

		buttons : [
			{separator: true},         	
			{name: 'Fases', bclass: 'phases', onpress : doCommandProyecto},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},
			{separator: true},	
			{name: 'Iniciar', bclass: 'start', onpress : doCommandProyecto},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado'},
			{display: 'Empresa', name : 'empresa'}
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

function doCommandProyecto(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
		if (com == 'Fases')
		{ver_fases(grid)}
		else if (com == 'Iniciar')
		{iniciar_proyecto(grid)}
	}
	else
	{notify("Debe seleccionar un proyecto!",null,timeL)}	
}
function ver_fases(grid)
{window.location = "/configurar/vista_de_fases/?pid="+get_ids(grid)[0]}

function iniciar_proyecto(grid){
	var id = get_ids(grid)[0]
    $.ajax({
    	type: 'POST',
    	dataType: "json",
    	url: "/configurar/proyectos/iniciar_proyecto",
    	data: {id:id,iniciable:false},
    	success: function(data){
    		if (data.iniciable)
    		{iniciar(id)}
    		else{
    			if (data.ya_iniciado)
    			{notify("El proyecto seleccionado ya se encuentra iniciado",null,timeL)}
    			else
    			{
    				notify("El proyecto no se puede iniciar.","error",timeL)
		    		if (data.sin_fases)
		    		{notify("El proyecto seleccionado no posee fases",null,timeL)}
		    		if (data.sin_usuarios)
		    		{notify("El proyecto seleccionado no posee fases",null,timeL)}
    			}
    		}
   	    	  
    	},
	});
}

function iniciar(id){
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/proyectos/iniciar_proyecto",
      data: {id:id},
      success: function(data)
      {   	  
    	  $("#proyectosConfigurarFlexi").flexReload();
    	  notify("El proyecto fue iniciado con exito","succes")
      },
    });
}