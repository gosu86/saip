$(function(){
	$('#navegador').flexigrid(
	{	
	
		buttons : [
			{separator: true},
			{name: 'Atras', bclass: 'import', onpress : doCommandTipoDeItem},
			{separator: true},
			{name: 'Desarrollar', bclass: 'add', onpress : doCommandTipoDeItem},			
		],
		height: '0px',

	});
});	
function doCommandTipoDeItem(com, grid)
{

}