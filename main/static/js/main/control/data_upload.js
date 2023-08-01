Dropzone.autoDiscover = false;

$(() => {
    // Hide the form and disable the 'Create Upload' button by default
    var formSubmitButton = $('#create-upload-form-submit');
    formSubmitButton.prop('disabled', true);

    var activeFiles = 0; // Keep track of the active files
    var tmpFileNames = []; // Store the temporary file names

    // Configuring Dropzone
    new Dropzone('#data-upload-files', {
        headers: {
            'X-CSRFToken': CSRF
        },
        paramName: 'file', // The name that will be used to transfer the file
        maxFilesize: 1024, // MB
        parallelUploads: 2,
        chunking: true,
        forceChunking: true,
        chunkSize: 2000000, // Chunk size in bytes (2MB)
        retryChunks: true, 
        retryChunksLimit: 3,
        dictDefaultMessage: "Drop files here to upload, or click to select files",
        init: function() {
            this.on("addedfile", function(file) {
                activeFiles++;
            });
            this.on("success", function(file, response) {
                // Handle the response returned by the server
                var data = JSON.parse(file.xhr.response)
                tmpFileNames.push(data.tmp_file_name);
            });
            this.on("complete", function(file) {
                activeFiles--;

                if (activeFiles === 0) {
                    // Enable the 'Create Upload' button when all files are uploaded
                    formSubmitButton.prop('disabled', false);

                    // Set the value of the '#id_files' input
                    $('#id_files').val(tmpFileNames.join(','));
                }
            });
            this.on("error", function(file, response) {
                toastr.error(response);
            });
        }
    });
})
