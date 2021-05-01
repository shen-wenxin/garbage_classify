var pg=document.getElementById('pg');

setInterval(function(e){

   if(pg.value!=100) pg.value++;     

   else pg.value=0;

},100);