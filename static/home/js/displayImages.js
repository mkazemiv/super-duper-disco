var folder = "videos/"; 

$.ajax({
  url : folder,
  success: function (data) {
    $(data).find("a").attr("href", function (i, val) {
      if( val.match(/\.(mp4)$/) ) {
        $("body").append( "<video src='"+ folder + val +"' controls></video>" );  
      }
    });
  }
});