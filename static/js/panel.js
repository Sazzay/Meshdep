$(function() {
	$("#uploadFile").hover(function() {
        $(this).animate({opacity: 0.7}, 500);
    }, function() {
        $(this).animate({opacity: 1.0}, 500);
    });
})