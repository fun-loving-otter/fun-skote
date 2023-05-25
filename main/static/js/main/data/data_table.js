$(document).ready(function() {
  $('#data-table').DataTable({
    serverSide: true,
    ajax: TABLE_API_URL,
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
