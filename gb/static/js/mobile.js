$(document).ready(function() {

  if (navigator.userAgent.match(/Android/i)) {
	$('#tit').text('android');
    window.scrollTo(0,0); // reset in case prev not scrolled  
    var nPageH = $(document).height();
    var nViewH = window.outerHeight;
    if (nViewH > nPageH) {
		nViewH = nViewH / window.devicePixelRatio;
		$('BODY').css('height',nViewH + 'px');
    }
    window.scrollTo(0,1);
  }

});