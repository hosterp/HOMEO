//$(document).on("shown.bs.modal", function (e) {
//    var $modal = $(e.target);
//    var modalTitle = $modal.find('.modal-title').text().trim();
//
//    if (modalTitle === "Search Stock In Tree") {
//        resetFieldValue();
//
//      var timeoutValue = data.length * 10; // adjust the multiplier as needed
//        setTimeout(function(){
//            // Initialize DataTable
//            $('.tree_class table').DataTable();
//
//
//            $('input[type="search"]').focus();
//        }, timeoutValue);
//    }
//});
function initializeDataTable(maxAttempts = 50) {
    var attempts = 0;
    var interval = 100;

    function attemptInitialization() {
        if ($('.tree_class table').length && $('.tree_class table tbody tr').length > 0) {

            if (!$.fn.DataTable.isDataTable('.tree_class table')) {
                $('.tree_class table').DataTable({
                    "drawCallback": function(settings) {

                        $('input[type="search"]').focus();
                    }
                });
            } else {

                $('input[type="search"]').focus();
            }
            console.log("DataTable initialized successfully");
        } else if (attempts < maxAttempts) {

            attempts++;
            setTimeout(attemptInitialization, interval);
        } else {
            console.warn("Failed to initialize DataTable after " + maxAttempts + " attempts");
        }
    }


    attemptInitialization();
}

$(document).on("shown.bs.modal", function (e) {
    var $modal = $(e.target);
    var modalTitle = $modal.find('.modal-title').text().trim();

    if (modalTitle === "Search Stock In Tree") {
        resetFieldValue();

        // Call the initialization function
        initializeDataTable();

        // Set up a listener for dynamic content loading, if applicable
        $modal.on('DOMNodeInserted', function(e) {
            if ($(e.target).hasClass('tree_class') || $(e.target).find('.tree_class').length > 0) {
                initializeDataTable();
            }
        });
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