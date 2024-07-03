$(document).ready(function(){
    var isHandlingFocus = false;

    $(document).on('keydown', ".oe_form_required", function (event) {
        var $this = $(this);
        var value = event.target.value;

        if ((event.which === 13 || event.which === 9) && !isHandlingFocus && value === "") {
            event.preventDefault();
            isHandlingFocus = true;
            $this.focus();
            isHandlingFocus = false;
        } else {
            isHandlingFocus = false;
            $this.prop('selectionStart', $this.val().length);
        }
    });
    $(document).on('focus', '.oe_form_field_many2one', function(event) {
        var inputValue = $(this).find('input').val().trim();
        if (!$(this).data('clicked') && inputValue === '') {
            $(this).data('clicked', true);
            $(this).find('.oe_m2o_drop_down_button').click();
        }
    });

//    $(document).on('focus', '.oe_form_field_many2one', function(event) {
//        if (!$(this).data('clicked')) {
//            $(this).data('clicked', true);
//            $(this).find('.oe_m2o_drop_down_button').click();
//        }
//    });


    $(document).on('blur', '.oe_form_field_many2one', function(event) {
        $(this).data('clicked', false);
    });


var clickedStates = {};
$(document).on('focus', '.oe_form_field_many2one', function(event) {
    var tableRow = $(this).closest('tr');
    var label = tableRow.find('label');
    if (label.text().trim() === "Customer") {
        var $ul = $("ul.ui-autocomplete:eq(0)");
        var $firstItem = $ul.find("li:first");
        if ($firstItem.length && !$firstItem.data('clicked')) {
            $firstItem.trigger("click");
            $firstItem.data('clicked', true);
            $firstItem.off('click');
    }


//        if ($ul.find("li").length === 2) {
//            if (!clickedStates.customer) {
//                $ul.find("li:first").click();
//                clickedStates.customer = true;
//            }
//        }
    }

});

$(document).on('focus', '.oe_form_field_many2one', function(event) {
    var tableRow = $(this).closest('tr');
    var label = tableRow.find('label');
        if (label.text().trim() === "To") {
            var $ul = $("ul.ui-autocomplete:eq(1)");
            var $firstItem = $ul.find("li:first");
            if ($firstItem.length && !$firstItem.data('clicked')) {
                $firstItem.trigger("click");
                $firstItem.data('clicked', true);
                $firstItem.off('click');
        }
    }
});

$(document).on('focus', '.oe_form_field_many2one[data-fieldname="product_id"]', function(event) {
    var $productField = $(this);
    var $ul = $productField.closest('tr').find("ul.ui-autocomplete:eq(21)");
    var $firstItem = $ul.find("li:first");
    if ($firstItem.length && !$firstItem.data('clicked')) {
        $firstItem.trigger("click");
        $firstItem.data('clicked', true);
        $firstItem.off('click');
    }
});
$(document).on('focus', '.oe_form_field_many2one[data-fieldname="medicine_rack"]', function(event) {
    var $productField = $(this);

    var $ul = $productField.closest('tr').find("ul.ui-autocomplete:eq(20)");
    var $firstItem = $ul.find("li:first");

    if ($firstItem.length && !$firstItem.data('clicked')) {
        // Trigger a click event on the first item of the autocomplete dropdown
        $firstItem.trigger("click");

        // Remove the click event listener after it's been triggered once
        $firstItem.data('clicked', true);
        $firstItem.off('click');
    }
});



});
 $(document).ready(function() {
    $(document).on('click', 'div.modal.in div.modal-header h3:contains("Payment History")', function() {
    });

   $(document).on('click', 'div.modal.in table tbody tr', function(event) {
        var jsonData = {};

        $.ajax({
            type: 'POST',
            url: '/pharmacy_mgmnt/payment_history',
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: function (response) {
//                alert('Payment successful!');
                console.log(response);
            },
            error: function (xhr, status, error) {

                alert('Error payment history: ' + error);
            }
        });
//        alert('Element in the first row of the modal body clicked!');
    });
});





