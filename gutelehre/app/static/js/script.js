$(document).ready(function() {

	$(function(){
	    $('#bewerten textarea').keyup(function(){
	      // var count = $(this).val().length;
	      // var needed = 300 - count;

	      // if (count < 300) {
	      // 	var str = "Nur noch " + needed + " Zeichen benötigt."
	      	
	      // 	if (count > 100 && count < 200) {
	      // 		str += "Schon über 100 Zeichen."
	      // 	} else {
		     //  	if (count >= 200) {
		     //  		str += "Fast geschafft. Weiter so!"
		     //  	}
		     //  }
		     //  $('#count').html(str);
	      // } else {
	      // 	var str = "Du hast " + count + " Zeichen geschrieben. Das reicht, aber du kannst sehr gerne noch mehr schreiben."
	      // 	if (count > 400) {
	      // 		str += " Desto ausführlicher, deto besser. Keep going!"

	      // 		if (count > 500) {
	      // 			str += " Premium!";

	      // 			if (count > 600) {
      	// 				str += " Super!";

	      // 				if (count > 800) {
		     //  				str += " Geil!";
	 
	     	// 	 				if (count > 1000) {
	      // 						str += " Oh yeaaaah!";

	      // 							if (count > 1500) {
	      // 								str += " Wow. Krass, du bist echt cool!";

	      // 								if (count > 2000) {
	      // 									str += " Dein Engagement ist eizigartig. Das war die letzte Motivation. Danke, für deinen Text";
	      // 								}
	      // 							}
	      // 						}
	      // 					}
	      // 				}
	      // 			}
	      // 		}
	      // 	$('#count').html(str);
	      // }
	    });

		$('#bewerten select').val('WS13')
		$('#bewerten input').one('focus', function(){
			if (this.value.length < 100) // only deleting if dummy text in teaxtarea
    		this.value = '';
		});

	});


	$('#star').raty({ path: '/static/lib/img' });
	$('#star').click(function(e) {  
	    $('#rating').val($('#star').raty('score'));     
	});
});

function toggleForm(){
   if (document.getElementById('add_new_course').style.visibility == "visible" ) {
   	document.getElementById('add_new_course').style.visibility = "hidden";
   } else {
   	document.getElementById('add_new_course').style.visibility = "visible";
   }
}

