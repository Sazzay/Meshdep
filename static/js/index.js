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

	$("#loginSubButton").click(function() {
		username = $("#loginInputEmail").val()
		password = $("#loginInputPassword").val()

		$.ajax({
			async: false,
			type: 'POST',
			url: '/api/login',
			contentType: "application/json",
			data: JSON.stringify({'user': username, 'pass': password}),
			success: function(result) {
				if (result == "AUTH") {
					window.location.href = '/'
				}
				if (result == "NAUTH") {
					alert("Invalid username or password")
				}
			}
		})
	})

	$("#regSubButton").click(function() {
		if ($('#regInputPassword').val() == $('#regInputConfPassword').val()) {
			$("#regInputConfPassword")[0].setCustomValidity("")
			
			username = $("#regInputEmail").val()
			password = $("#regInputPassword").val()

			$.ajax({
				async: true,
				type: 'POST',
				url: '/api/register',
				contentType: "application/json",
				data: JSON.stringify({'user': username, 'pass': password}),
				success: function(result) {
					alert(JSON.parse(result))
				}
			})
		} else {
			$("#regInputConfPassword")[0].setCustomValidity("Passwords do not match.")
		}
	})
});