$(document).ready(function(){
    var isHandlingFocus = false;

    $(document).on('keydown', ".oe_form_required, .required_class", function (event) {
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
//$(document).on('keydown', '#oe-field-input-2', function(event) {
//    if (event.key === 'Enter') {
//        var $ul = $("ul.ui-autocomplete:eq(0)");
//        var $selectedItem = $ul.find("li.ui-state-focus");
//        if ($selectedItem) {
//            $selectedItem.trigger("click");
//            $('#oe-field-input-6').focus();
//        }
//    }
//});
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
$(document).on('focus', '.oe_form_field_many2one[data-fieldname="rack"]', function(event) {
    var $productField = $(this);
    var $ul = $productField.closest('tr').find("ul.ui-autocomplete:eq(3)");
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
    function addNewTabBehavior($element) {
        var href = $element.attr('href');
        $element.on('click', function(e) {
            e.preventDefault();
            var newWindow = window.open(href, '_blank');
              if (newWindow) {
                newWindow.addEventListener('beforeunload', function(event) {
                    event.returnValue = "Are you sure you want to leave this page?";
                });
            }
        });
    }

    $('.oe_menu_leaf').each(function() {
        var $mainMenuItem = $(this);
        var menuId = $mainMenuItem.data('menu');
        var $submenu = $('[data-parent-menu-id="' + menuId + '"]');

        if ($submenu.length > 0) {
            $submenu.find('a').each(function() {
                addNewTabBehavior($(this));
            });
        } else {
            addNewTabBehavior($mainMenuItem);
        }
    });

    $('.oe_menu_leaf').next('ul').find('a').each(function() {
        addNewTabBehavior($(this));
    });

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
$(document).ready(function() {
   $(document).on("shown.bs.modal", function () {
        setTimeout(function(){
            var firstButton = $('.modal-footer .custom_register_payment');
            if(firstButton.length) {
                console.log("First button found, triggering click...");
                firstButton.on('click', function() {
                    console.log("First button was clicked, triggering the second button...");
                    var secondButton = $('.css_print');
                    if(secondButton.length) {
                        console.log("Second button found, triggering click...");
                        secondButton.trigger('click');
                    } else {
                        console.log("Second button not found");
                    }
                });
            } else {
                console.log("First button not found");
            }
        }, 500);
    });
});
