/*
$('#container').waterfall({
    itemCls: 'item',
    colWidth: 230,
    gutterWidth: 5,
    gutterHeight: 5,
    checkImagesLoaded: false,
    isAnimated: true,
    animationOptions: {
    },
    path: function(page) {
        return 'static/data/data.json?page=' + page;
    }
});
*/
/*
$(function() {
$( "#slider-range" ).slider({
range: true,
min: 0,
max: 5000,
values: [ 0, 5000 ],
slide: function( event, ui ) {
$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
}
});
$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
" - $" + $( "#slider-range" ).slider( "values", 1 ) );
});
*/

jQuery(document).ready(function(){
  $('.filter h3').click(function() {

	  $(this).toggleClass("closed").next().toggle();
     
  })
 
  
});