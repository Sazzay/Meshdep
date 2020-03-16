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

	$("#regForm").submit(function() {
		username = $("#regInputEmail").val()
		password = $("#regInputPassword").val()

		$.ajax({
			type: 'POST',
			url: '/api/register',
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify({user: username, pass: password}),
			success: function(result) {
				alert("Test")
			}
		})
	})

	$("#loginSubButton").click(function() {
		username = $("#loginInputEmail").val()
		password = $("#loginInputPassword").val()

		$.ajax({
			type: 'POST',
			url: '/api/login',
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify({user: username, pass: password}),
			success: function(result) {
				alert(result)
			}
		})
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