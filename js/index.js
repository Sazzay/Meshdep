$(function() {
	$("#regButton").click(function() {
		$("#logInForm").fadeOut(400, function() {
			$("#disclamerDiv").fadeIn(400)
		})
	})

	$("#disclamerAccept").click(function() {
		$("#disclamerDiv").fadeOut(400, function() {
			$("#regForm").fadeIn(400)
		})
	})

	$("#disclamerDecline").click(function() {
		window.location.replace("https://google.com")
	})

	$("#logInButton").click(function() {
		$("#regForm").fadeOut(400, function() {
			$("#logInForm").fadeIn(400)
		})
	})
});