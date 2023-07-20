var table;
var filters = {};


$(document).ready(function() {
    table = $('#data-table').DataTable({
        dom: 'rtip',
        serverSide: true,
        processing: true,
        lengthChange: false,
        pageLength: 25,
        pagingType: "simple",
        ajax: {
            url: TABLE_API_URL,
            type: "POST",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", CSRF);
                showLoadingAlert();
            },
            data: function(d) {
                d.filters = JSON.stringify(filters);
            },
            complete: function() {
                hideLoadingAlert();
            }
        },
        rowId: "id",
        select: {
            style: 'multi',
            selector: 'td:first-child'
        },
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            targets: 0,
            defaultContent: '',
            data: null
        }],
        columns: TABLE_COLUMNS
    });

    $('#applyFilter').on('click', function() {
        $('input[data-filter="text-filter"]').each(function() {
            var columnSelector = '#' + $(this).data('column');
            var searchValue = $(this).val();
            table.column(columnSelector).search(searchValue);
        });

        $('input[data-filter="date-filter"]').each(function() {
            var rangeValue = $(this).data('range');
            var filterName = $(this).data('field') + '_' + rangeValue;
            filters[filterName] = $(this).val();
        })

        $('input[data-filter="range-filter"]:checked').each(function() {
            var columnSelector = '#' + $(this).data('column');
            var searchValue = $(this).data('range');
            table.column(columnSelector).search(searchValue);
        })

        $('[data-filter="select-filter"]').each(function() {
            var $select = $(this);
            var columnSelector = '#' + $select.data('column');
            var selectedOptions = $select.val();

            if (selectedOptions) {
                var searchValue = selectedOptions.join('|');
                table.column(columnSelector).search(searchValue, true, false);
            } else {
                table.column(columnSelector).search('');
            }
        });

        table.draw();
    });

    $('input[data-filter="date-filter"]').dtDateTime();

    $('[data-filter="select-filter"]').each(function() {
        var fieldName = $(this).data('field');
        $(this).select2({
            multiple: true,
            data: SELECT_OPTIONS[fieldName],
            dropdownAutoWidth: true,
            theme: 'bootstrap-5'
        })
    });
});


function showLoadingAlert() {
    Swal.fire({
        title: 'Loading',
        text: 'Please wait...',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        showCancelButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}


function hideLoadingAlert() {
    Swal.close();
}


function AddToList(url, ids) {
    // Construct the request body
    let data = {
        data: ids,
    };

    // Send the PATCH request with CSRF token in headers
    fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF,
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                toastr.success('Successfully added to list.');
            } else {
                toastr.error('Failed to add to list.');
            }
        })
        .catch(error => {
            toastr.error('An error occurred while making the request.');
        });
}


function AddSelectedToList(url) {
    let selected_rows = table.rows({ selected: true });
    let ids = selected_rows.ids().toArray();
    AddToList(url, ids);
    selected_rows.deselect();
}
