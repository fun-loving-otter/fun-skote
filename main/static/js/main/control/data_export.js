$(() => {
    $('#export-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var form = $(this);

        Swal.fire({
            title: "Loading",
            allowOutsideClick: false,
            didOpen: function () {
                Swal.showLoading();
                makeExportRequest();
            }
        })

        function makeExportRequest() {
            // Get form data as an object
            var formData = form.serializeArray();
            var formUrl = form.prop('action');

            // Send AJAX request
            $.ajax({
                type: "POST",
                url: formUrl,
                headers: {
                  'X-CSRFToken': CSRF
                },
                data: formData,
                dataType: "json", // Set the expected data type of the response
                success: handleExportSuccess,
                error: handleExportError,
                complete: function () {
                    Swal.hideLoading();
                }
            });
        }

        function handleExportSuccess(response) {
            var progressUrl = response.progress_url;

            Swal.fire({
              title: "Export in progress",
              html: "<div class='progress-wrapper'>" +
                      "<div id='progress-bar' class='progress-bar' style='background-color: #68a9ef; width: 0%;'>&nbsp;</div>" +
                    "</div>" +
                    "<div id='progress-bar-message'>Waiting for progress to start...</div>",
              showConfirmButton: false,
              allowOutsideClick: false,
              didOpen: function () {
                CeleryProgressBar.initProgressBar(progressUrl, {
                  onResult: handleExportTaskResult
                });
              }
            });
        }

        function handleExportError(xhr) {
            Swal.fire({
                icon: "error",
                title: "AJAX request finished with error",
                text: xhr.responseText,
                confirmButtonColor: "#556ee6",
            });
        }

        function handleExportTaskResult(resultElement, result) {
            Swal.close();
            window.location.replace(result);
        }
    })
})
