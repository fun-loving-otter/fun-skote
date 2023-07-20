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
            theme: 'bootstrap-5',
            selectionCssClass: "select2--small",
            dropdownCssClass: "select2--small",
        })
    });

    // Set event listeners for date filter buttons
    $('#fundingPeriod7').click(function() {
        setFundingPeriod(7);
    });

    $('#fundingPeriod14').click(function() {
        setFundingPeriod(14);
    });

    $('#fundingPeriod30').click(function() {
        setFundingPeriod(30);
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


// Function to set the funding period filters and redraw the table
function setFundingPeriod(days) {
    // Get the current date
    var currentDate = new Date();

    // Calculate the start date
    var startDate = new Date();
    startDate.setDate(currentDate.getDate() - days);

    // Format the start and end dates as strings
    var startDateString = moment(startDate).format('YYYY-MM-DD');
    var endDateString = moment(currentDate).format('YYYY-MM-DD');

    // Set the filter values
    filters['last_funding_date_after'] = startDateString;
    filters['last_funding_date_before'] = endDateString;

    // Redraw the table
    table.draw();
}
