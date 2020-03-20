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

	function notifOpInProgress() {
		new Noty({
    		type: 'warning',
    		container: '#notyContainer',
    		timeout: 6000,
		    text: "A file operation is already in progress, please wait until it's complete",
		    animation: {
		        open: 'animated bounceInLeft', // Animate.css class names
		        close: 'animated bounceOutLeft' // Animate.css class names
		    }
		}).show();
	}

	// JQuery
	let files = []
	let faded = false
	let operationInProgress = false


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
    	if (!operationInProgress) {
    		$('#uploadFileField').trigger('click');
    	} else {
    		notifOpInProgress()
    	}
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
			operationInProgress = true
			data.submit()

			if ($("#progressDiv").css("opacity") == 0.0) {
				$("#progressDiv").animate({opacity: 1.0}, 800)
			}

			new Noty({
	    		type: 'information',
	    		container: '#notyContainer',
	    		timeout: 4000,
			    text: 'Starting file upload... Please stand by.',
			    animation: {
			        open: 'animated bounceInLeft', // Animate.css class names
			        close: 'animated bounceOutLeft' // Animate.css class names
			    }
			}).show();
		},
		progress: function(e, data) {
			let progress = parseInt(data.loaded / data.total * 100, 10)

			$('#progressUlDl').css('width', progress+'%').attr('aria-valuenow', progress); 
			$('#progressUlDl').text(progress+'%')
		},
		done: function(e, data) {
			// fade out the progress bar and display message
			operationInProgress = false

			if ($("#progressDiv").css("opacity") > 0.0) {
				$("#progressDiv").animate({opacity: 0.0}, 800)
			}

			new Noty({
	    		type: 'success',
	    		container: '#notyContainer',
	    		timeout: 6000,
			    text: 'File upload was successful, it may take a minute for the file to show up.',
			    animation: {
			        open: 'animated bounceInLeft', // Animate.css class names
			        close: 'animated bounceOutLeft' // Animate.css class names
			    }
			}).show();
		},
		error: function(e, data) {
			operationInprogress = false

			if ($("#progressDiv").css("opacity") > 0.0) {
				$("#progressDiv").animate({opacity: 0.0}, 800)
			}

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
					"<div id=" + a[0] + " class='card mt-2 ml-1 mr-1 border-dark' style='width: 200px; height: 250px; display: none;'>"+
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
					if (!operationInProgress) {
						let file = fetchFileData($(this).attr('id').replace(/\D/g,''), files)
						operationInProgress = true

						$.ajax({ 
							type: 'POST',
							url: '/api/delete',
							contentType: "application/json; charset=utf-8",
							data: JSON.stringify({'fileName': file[6], 'node': file[2]}),
							success: function(response) {
								operationInProgress = false

								new Noty({
						    		type: 'success',
						    		container: '#notyContainer',
						    		timeout: 6000,
								    text: "Successfully deleted the file, it may take a few seconds for the file table to update.",
								    animation: {
								        open: 'animated bounceInLeft', // Animate.css class names
								        close: 'animated bounceOutLeft' // Animate.css class names
								    }
								}).show();
							},
							error: function(response) {
								operationInProgress = false

								new Noty({
						    		type: 'error',
						    		container: '#notyContainer',
						    		timeout: 6000,
								    text: "Something went wrong when trying to delete the file. Please try again later.",
								    animation: {
								        open: 'animated bounceInLeft', // Animate.css class names
								        close: 'animated bounceOutLeft' // Animate.css class names
								    }
								}).show();
							}
						})
					} else {
						notifOpInProgress();
					}
				})

				$("#addBtn" + a[0]).on('click', function() {
					new Noty({
			    		type: 'information',
			    		container: '#notyContainer',
			    		timeout: 8000,
					    text: 'Attempting to fetch the file from the server. This may take some time for large files.',
					    animation: {
					        open: 'animated bounceInLeft', // Animate.css class names
					        close: 'animated bounceOutLeft' // Animate.css class names
					    }
					}).show();

					if (!operationInProgress) {
						let file = fetchFileData($(this).attr('id').replace(/\D/g,''), files)
						operationInProgress = true

						$.fileDownload('/api/download', {
							httpMethod: 'POST',
							data: {'fileName': file[6], 'node': file[2], 'size': file[5]},
							successCallback: function(url) {
								operationInProgress = false

								new Noty({
						    		type: 'success',
						    		container: '#notyContainer',
						    		timeout: 6000,
								    text: "Server fetched the file, download starting!",
								    animation: {
								        open: 'animated bounceInLeft', // Animate.css class names
								        close: 'animated bounceOutLeft' // Animate.css class names
								    }
								}).show();
							},
							failCallback: function(html, url) {
								operationInProgress = false

								new Noty({
						    		type: 'error',
						    		container: '#notyContainer',
						    		timeout: 6000,
								    text: "Something went wrong when trying to download the file. Please try again later.",
								    animation: {
								        open: 'animated bounceInLeft', // Animate.css class names
								        close: 'animated bounceOutLeft' // Animate.css class names
								    }
								}).show();
							}
						})
					} else {
						notifOpInProgress();
					}
				})
			}

			fileIds.push(a[0])
		}

		divs = fetchAllDivIds("#fileContainerRow")

		for (d of divs) {
			if (!fileIds.includes(parseInt($(d).attr("id")))) {
	   			$(d).animate({opacity: 0.0}, 1000, function(d) {
	   				$(this).remove()
	   			})
			}
		}
		// figure out method to delete
   		
	}, 1000 );
})