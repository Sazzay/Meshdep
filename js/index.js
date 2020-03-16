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

	$("#regForm").submit(function(event) {
		$.post("api/register", function(data) {
			console.log("Successfully submitted registration.")
		})
	})

	$("#logInForm").submit(function() {
		$.post("api/login", function(data) {
			console.log("Successfully submitted login.")
		});
	})

	$("#regSubButton").click(function() {
		if ($('#regInputPassword').val() == $('#regInputConfPassword').val()) {
			$("#regInputConfPassword")[0].setCustomValidity("")
			$("#regForm").submit();
		} else {
			$("#regInputConfPassword")[0].setCustomValidity("Passwords do not match.")
		}
	})
});