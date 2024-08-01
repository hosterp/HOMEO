$(document).on("shown.bs.modal", function (e) {
    var $modal = $(e.target);
    var modalTitle = $modal.find('.modal-title').text().trim();

    if (modalTitle === "Search Stock In Tree") {
        resetFieldValue();

        setTimeout(function(){
            // Initialize DataTable
            $('.tree_class table').DataTable();

            // Focus the search input
            $('input[type="search"]').focus();
        }, 500);
    }
});

//libiya.....................
function resetFieldValue() {
     $.ajax({
            type: 'POST',
            url: '/pharmacy_mgmnt/reset_quantity',
            success: function (response) {
//                alert('Reset successful!');
                console.log(response);
            },
            error: function (xhr, status, error) {
//                alert('Error resetting quantity: ' + error);
            }
     });
    var field = $('td[data-field="quantity_selected"]');
    if (field.length > 0) {
        field.text('0');
//        console.log('Resetting field value...');
    } else {
        console.error('Field not found.');
    }
}

//libiya.........................................