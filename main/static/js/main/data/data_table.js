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
            },
            data: function(d) {
                d.filters = JSON.stringify(filters);
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
        columns: TABLE_COLUMNS,
        initComplete: function() {
            this.api()
                .columns()
                .every(function() {
                    var column = this;

                    var footer = $(column.footer());
                    var filterType = footer.data('filter-type');

                    if (filterType == 'char') {
                        var input = footer.children('input');
                        input.on('keyup change clear', function() {
                            if (column.search() !== this.value) {
                                column.search(this.value).draw();
                            }
                        });
                    } else if (filterType == 'dateRange') {
                        var fieldName = footer.data('field-name');

                        var startInput = footer.children('input[data-range="start"]');
                        var endInput = footer.children('input[data-range="end"]');

                        var startDate = startInput.dtDateTime();
                        var endDate = endInput.dtDateTime();

                        startInput.on('change', function () {
                            filters[`${fieldName}_after`] = startDate.val();
                            table.draw();
                        });
                        endInput.on('change', function () {
                            filters[`${fieldName}_before`] = endDate.val();
                            table.draw();
                        });
                    } else if (filterType == 'intRange') {
                        var fieldName = footer.data('field-name');

                        var startInput = footer.children('input[data-range="start"]');
                        var endInput = footer.children('input[data-range="end"]');

                        footer.children('input').on('keyup change clear', function () {
                            column.search(startInput.val() + '|' + endInput.val(), true, false).draw();
                        })



                        // var fieldName = footer.data('field-name');

                        // var startInput = footer.children('input[data-range="start"]');
                        // var endInput = footer.children('input[data-range="end"]');

                        // startInput.on('change', function () {
                        //     filters[`${fieldName}_min`] = startInput.val();
                        //     table.draw();
                        // });
                        // endInput.on('change', function () {
                        //     filters[`${fieldName}_max`] = endInput.val();
                        //     table.draw();
                        // });
                    }
                });
        },
    });
});




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
