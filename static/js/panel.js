$(function() {
	// JQuery
	let files = []

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

	setInterval(function(){
		var fileIds = [];


    	$.ajax({
       		type: "GET",
       		url: "/api/fetch_files",
       		success: function(response){
        	 	files = JSON.parse(response)
       		}
   		});

		for (a of files) {
			if (!isIdValid(a[0])) {
				$("#fileContainerRow").append(
					"<div id=" + a[0] + " class='card mt-2 ml-1 mr-1' style='width: 200px; height: 250px; display: none;'>"+
						"<div class='card-body' style='padding-top: 10px; margin-left: 5px margin'>"+
							"<h5 class='card-title' style='font-size: 14px'>" + a[6] + "</h5>"+
	    					"<p style='font-size: 10px'><b>Stored on node</b> - " + a[2] + "</p>"+
	    					"<p style='font-size: 10px'><b>Last Modified</b> - " + a[3] + "</p>"+
	    					"<input id=delBtn" + a[0] + " class='logo-vsmall' type='image' style='max-width: 32px; max-height:32px; position: absolute; bottom: 5px; left: 10px' src='/static/img/meshdep-del.png' alt='Delete'>"+
	    					"<input id=addBtn" + a[0] + " class='logo-vsmall' type='image' style='max-width: 32px; max-height:32px; position: absolute; bottom: 5px; right: 10px' src='/static/img/meshdep-download.png' alt='Download'>"+
	  					"</div>"+
					"</div>")
				$("#" + a[0]).css('opacity', '0.0')
				$("#" + a[0]).css('display', 'block')
				$("#" + a[0]).animate({opacity: 1.0}, 1000);

				$("#delBtn" + a[0]).on('click', function() {
					console.log(this)
					let id = $(this).attr('id')

					// del button
				})

				$("#addBtn" + a[0]).on('click', function() {
					console.log(this)
					let id = $(this).attr('id')

					// add button
				})
			}

			fileIds.push(a[0])
		}

		divs = fetchAllDivIds("#fileContainerRow")

		for (d of divs) {
			if (!fileIds.includes(parseInt($(d).attr("id")))) {
				$(d).remove()
			}
		}
		// figure out method to delete
   		
	}, 1000 );


	// Raw JS
	function isIdValid(id) {
		if($("#" + id).length == 0) {
			return false
		} else {
			return true
		}
	}

	function fetchAllDivIds(parentDiv) {
		return $(parentDiv).children("div[id]")
	}
})