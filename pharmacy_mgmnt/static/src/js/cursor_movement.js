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
//   $(document).on('focus', '.oe_form_field_many2one', function(event) {
//        var $this = $(this);
//        var inputValue = $(this).find('input').val().trim();
//        if (!$(this).data('clicked') && inputValue === '') {
//            $(this).data('clicked', true);
//            $(this).find('.oe_m2o_drop_down_button').click();
//            console.log('visible');
//        } else if (inputValue!== '') {
//            console.log('hide');
//            $(this).find('.oe_m2o_drop_down_button').hide();
//        }
//    });

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
//$(document).on('focus', '.oe_form_field_many2one', function(event) {
//    var $productField = $(this);
//    var tableRow = $(this).closest('tr');
//    var label = tableRow.find('label');
//    if (label.text().trim() === "Customer") {
//       $productField.find('input').one('autocompleteopen', function() {
//            setTimeout(function() {
//                $productField.find('input').select();
//            }, 100); // Increase timeout value
//        });
//        var $ul = $("ul.ui-autocomplete");
//        var $firstItem = $ul.find("li:first");
//        if ($firstItem.length && !$firstItem.data('clicked')) {
//            $firstItem.trigger("click");
//            $firstItem.data('clicked', true);
//            $firstItem.off('click');
//        }
//    }
//});
        $(document).on('focus', '.oe_form_field_many2one', function(event) {
            var $productField = $(this);
            var tableRow = $(this).closest('tr');
            var label = tableRow.find('label');

            if (label.text().trim() === "Customer") {
                // Ensure that the input field is fully rendered
                setTimeout(function() {
                    var $input = $productField.find('input');

                    // Ensure that the input field is visible and focusable
                    if ($input.is(':visible') && $input.is(':focus')) {
                        // Select input value
                        $input.select();
                        console.log('Input value selected');
                    } else {
                        console.log('Input field is not visible or not focused');
                    }
                }, 100); // Increase the timeout value if needed

                var $ul = $("ul.ui-autocomplete");
                var $firstItem = $ul.find("li:first");
                if ($firstItem.length && !$firstItem.data('clicked')) {
                    $firstItem.trigger("click");
                    $firstItem.data('clicked', true);
                    $firstItem.off('click');
                }
            }
        });


//        if ($ul.find("li").length === 2) {
//            if (!clickedStates.customer) {
//                $ul.find("li:first").click();
//                clickedStates.customer = true;
//            }
//        }


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
        $productField.find('input').select();
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
        $firstItem.trigger("click");
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
          e.stopPropagation();

          window.open(href, '_blank');
          return false;
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
    var shouldWarn = true;

    window.addEventListener('beforeunload', function (e) {
        if (shouldWarn) {
            var confirmationMessage = 'You have unsaved changes or are leaving the page.';
            e.preventDefault();
            e.returnValue = confirmationMessage;
            return confirmationMessage;
        }
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
            var firstButton = $('.custom_register_payment');
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
//   $(document).on('shown.bs.modal', function (event) {
//        var modal = $(event.target);
//        var modalTitle = modal.find('.modal-title').text().trim();
//
//        if (modalTitle === "Hiworth Warning"||modalTitle === "Warning"||modalTitle === "Hiworth") {
//            $(document).on('keydown', function (event) {
//                if (event.keyCode === 13) {
//                    modal.find('.close').click();
//                }
//            });
//        }
//   });
    $(document).on('shown.bs.modal', function (event) {
        var modal = $(event.target);
        var modalTitle = modal.find('.modal-title').text().trim();
        var modalBody = modal.find('.modal-body').text().trim(); // Get the text content of the modal body

        var titlesToCheck = ["Hiworth Warning", "Warning","Hiworth Client Error","Hiworth"];


        if (titlesToCheck.includes(modalTitle) || modalBody.includes("Odoo Server Error")) {
            $(document).on('keydown', function (event) {
                if (event.keyCode === 13) {
                    modal.find('.close').click();
                }
            });
        }
    });
});
$(document).ready(function() {
    checkAndHandleConditions();
});

function checkAndHandleConditions() {
    // Check the condition and perform actions
    $('.oe_form_field_many2one').each(function() {
        var $this = $(this);
        var inputValue = $this.find('input').val().trim();
        var dropdownButton = $this.find('.oe_m2o_drop_down_button');
        var isDropdownVisible = dropdownButton.is(':visible');

        if (inputValue === '') {
            if (!$(this).data('clicked')) {
                $(this).data('clicked', true);
                setTimeout(() => {
                    dropdownButton.click();
                    console.log('Dropdown button clicked');
                }, 100); // Adjust delay as needed
            }
        } else {
            if (isDropdownVisible) {
                setTimeout(() => {
                    dropdownButton.hide();
                    console.log('Dropdown hidden');
                }, 100); // Adjust delay as needed
            } else {
                console.log('Dropdown already hidden');
            }
        }
    });
}
