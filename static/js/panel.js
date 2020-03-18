$(function() {
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

	function fetchFileData(id, fileInput) {
		for (a of fileInput) {
			if (parseInt(a[0]) == parseInt(id)) {
				return a
			}
		}

		return []
	}

	const sleep = (milliseconds) => {
  		return new Promise(resolve => setTimeout(resolve, milliseconds))
	}

	// JQuery
	let files = []
	let faded = false
	let fadedText = false

	// Initial fade in of loading
	$("#loadingDiv").animate({opacity: 1.0}, 800);

	sleep(1000).then(() => {
		$("#loadingDiv").animate({opacity: 0.0}, 800, function() {
			if (files.length == 0 && $("#noFilesDiv").css("opacity") == 0.0) {
				$("#noFilesDiv").animate({opacity: 1.0}, 800)
			}

			if (files.length > 0) {
				faded = true
			}
		})
	})

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

   		if (files.length != 0 && $("#noFilesDiv").css("opacity") == 1.0) {
   			$("#noFilesDiv").animate({opacity: 0.0}, 800, function() {
   				faded = true
   			});
   		}

		for (a of files) {
			if (!isIdValid(a[0]) && faded) {
				$("#fileContainerRow").append(
					"<div id=" + a[0] + " class='card mt-2 ml-1 mr-1' style='width: 200px; height: 250px; display: none;'>"+
						"<div class='card-body' style='padding-top: 10px; margin-left: 5px margin'>"+
							"<h5 class='card-title' style='font-size: 14px'>" + a[6] + "</h5>"+
	    					"<p style='font-size: 10px'><b>Stored on node: </b>" + a[2] + "</p>"+
	    					"<p style='font-size: 10px'><b>Last Modified: </b>" + a[3] + "</p>"+
	    					"<p style='font-size: 10px'><b>Filesize: </b> " + a[5] + "</p>"+
	    					"<input id=delBtn" + a[0] + " class='logo-vsmall' type='image' style='max-width: 32px; max-height:32px; position: absolute; bottom: 5px; left: 10px' src='/static/img/meshdep-del.png' alt='Delete'>"+
	    					"<input id=addBtn" + a[0] + " class='logo-vsmall' type='image' style='max-width: 32px; max-height:32px; position: absolute; bottom: 5px; right: 10px' src='/static/img/meshdep-download.png' alt='Download'>"+
	  					"</div>"+
					"</div>")
				$("#" + a[0]).css('opacity', '0.0')
				$("#" + a[0]).css('display', 'block')
				$("#" + a[0]).animate({opacity: 1.0}, 1000);

				$("#delBtn" + a[0]).on('click', function() {
					let file = fetchFileData($(this).attr('id').replace(/\D/g,''), files)

					$.ajax({ 
						type: 'POST',
						url: '/api/delete',
						contentType: "application/json; charset=utf-8",
						data: JSON.stringify({'fileName': file[6], 'node': file[2]})
					})

				})

				$("#addBtn" + a[0]).on('click', function() {
					let file = fetchFileData($(this).attr('id').replace(/\D/g,''), files)
					console.log(file)
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
})