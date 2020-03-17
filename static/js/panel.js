$(function() {
	$("#uploadFileButton").hover(function() {
        $(this).animate({opacity: 0.7}, 500);
    }, function() {
        $(this).animate({opacity: 1.0}, 500);
    });

    $('#uploadFileButton').on('click', function() {
    	$('#uploadFileField').trigger('click');
	});

	$('#uploadFileField').change(function() {
		field = $("#uploadFileField").val()

	})

	$('#uploadFileField').fileupload({
		formData: {
			filename: "test"
		},
		dataType: "json",
		method: "POST",
		url: "/api/upload",
		limitConcurrentUploads: 1,
		maxNumberOfFiles: 1,
		sequentialUploads: true,
		add: function(e, data) {
			data.submit()
		},
		progress: function(e, data) {
			let progress = parseInt(data.loaded / data.total * 100, 10)

			console.log(progress)
		}
	})
})