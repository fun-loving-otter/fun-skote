var table;


$(document).ready(function() {
    table = $('#data-table').DataTable({
        serverSide: true,
        ajax: TABLE_API_URL,
        rowId: "id",
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        columnDefs: [ {
            orderable: false,
            className: 'select-checkbox',
            targets:   0,
            defaultContent: '',
            data: null
        }],
        columns: TABLE_COLUMNS,
    });
});




function AddToList(url) {
    let selected_rows = table.rows({ selected: true });
    let ids = selected_rows.ids().toArray();

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

    selected_rows.deselect();
}



