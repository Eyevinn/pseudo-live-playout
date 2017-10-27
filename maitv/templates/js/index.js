$(document).ready(function(){

 console.log("Hello World!");

 $( "#play" ).click(function() {
  console.log("Play button clicked!");
  $('#videoplayer').play();
});

 var myVideos;
 var userId = 1;
 var userName= "anna";
/*
   $.ajax({
       url: 'http://localhost:8080/login?user=' + userName,
       success: function(data) {
           userId = int(data);
           console.log(userId);
       }
     });*/
   });