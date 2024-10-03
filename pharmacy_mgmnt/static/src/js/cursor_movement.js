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

  $(document).on('focus', '.oe_form_field_many2one, .phone_customer input', function (event) {
        var $productField = $(this);
        var tableRow = $productField.closest('tr');
        var label = tableRow.find('label').text().trim();

        if (label === "Customer") {
            $productField.find('input').addClass('css_customer');

        } else if (label === "Phone No") {
            $productField.addClass('css_phone');
        }

    });
var clickedStates = {};



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

//$(document).on('focus', '.oe_form_field_many2one[data-fieldname="product_id"]', function(event) {
//    var $productField = $(this);
//    var $ul = $productField.closest('tr').find("ul.ui-autocomplete:eq(21)");
//    var $firstItem = $ul.find("li:first");
//    if ($firstItem.length && !$firstItem.data('clicked')) {
//        $firstItem.trigger("click");
//        $firstItem.data('clicked', true);
//        $firstItem.off('click');
//        $productField.find('input').select();
//    }
//});
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
            var printbutton = $('.custom_print');
            if(printbutton.length){
                printbutton.focus();
            }
            if(firstButton.length) {
//                console.log("First button found, triggering click...");
                firstButton.focus();
                firstButton.on('click', function() {
                      firstButton.focus();
//                    console.log("First button was clicked, triggering the second button...");
                    var secondButton = $('.css_print');
                    if(secondButton.length) {
//                        console.log("Second button found, triggering click...");
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

var currentlyFocusedField = null;


$(document).on('focus', 'input, textarea, select', function () {
    currentlyFocusedField = $(this);
    console.log("Currently focused field:", currentlyFocusedField);
});


$(document).on('shown.bs.modal', function (event) {
    var modal = $(event.target);
    var modalTitle = modal.find('.modal-title').text().trim();
    var modalBody = modal.find('.modal-body').text().trim();

    var titlesToCheck = ["Hiworth Warning", "Warning", "Hiworth Client Error", "Hiworth"];

    if (titlesToCheck.includes(modalTitle) || modalBody.includes("Odoo Server Error")) {
          $(document).on('keydown', function (event) {
                if (event.keyCode === 13) {
                    modal.find('.close').click();
                }
                });
    }
});


$(document).on('hidden.bs.modal', function () {
    console.log("Modal is now hidden");
    if (currentlyFocusedField) {
        setTimeout(function () {
            currentlyFocusedField.focus();
            console.log("Focusing on field:", currentlyFocusedField);
        }, 100);
    }
});


//    $(document).on('shown.bs.modal', function (event) {
//        var modal = $(event.target);
//        var modalTitle = modal.find('.modal-title').text().trim();
//        var modalBody = modal.find('.modal-body').text().trim(); // Get the text content of the modal body
//
//        var titlesToCheck = ["Hiworth Warning", "Warning","Hiworth Client Error","Hiworth"];
//        if (titlesToCheck.includes(modalTitle) || modalBody.includes("Odoo Server Error")) {
//            $(document).on('keydown', function (event) {
//                if (event.keyCode === 13) {
//                    modal.find('.close').click();
//                }
//            });
//        }
//    });
});
$(document).ready(function() {
    $(document).on('focus', '.oe_form_field_many2one', debounce(function(event) {
        checkAndHandleConditions($(this));
    }, 200));
});

function checkAndHandleConditions($this) {
    var inputValue = $this.find('input').val().trim();
    var dropdownButton = $this.find('.oe_m2o_drop_down_button');


//    console.log('Input Value:', inputValue);
//    console.log('Dropdown Button Visible:', dropdownButton.is(':visible'));


    if (inputValue === '') {
        if (!$this.data('clicked')) {
            $this.data('clicked', true);
            setTimeout(() => {
                console.log('Attempting to click dropdown button...');
                dropdownButton.click();

                // Wait for dropdown to appear
                setTimeout(() => {
                    var $ulAfterClick = $("ul.ui-autocomplete");
//                    console.log('Dropdown List Visible After Click:', $ulAfterClick.is(':visible'));

                    if (!$ulAfterClick.is(':visible')) {
//                        console.log('Dropdown not visible after clicking. There might be an issue.');
                    }
                }, 500);
            }, 100);
        }
    } else {
        if (dropdownButton.is(':visible')) {
//            console.log('Input Value Present - Attempting to hide dropdown...');
            setTimeout(() => {
                dropdownButton.hide();
                $this.find('input').select();

                setTimeout(() => {
                    var $ulAfterHide = $("ul.ui-autocomplete");
//                    console.log('Dropdown List Visible After Hide:', $ulAfterHide.is(':visible'));

                    if ($ulAfterHide.is(':visible')) {
//                        console.log('Dropdown still visible after hiding. There might be an issue.');
                    }
                }, 500);
            }, 100);
        } else {
//            console.log('Dropdown already hidden or never shown');
        }
    }
}


function debounce(func, wait) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
    }


$(document).on('keydown', '.required_class.grp', function(event) {
            if (event.which === 13 || event.which === 9) {
                event.preventDefault();

                console.log('Keydown event detected:', event.which);


                var $currentInput = $(this).find('input');


                console.log('Current input:', $currentInput);


               var $inputField = $('.oe_form_field.oe_form_field_float.required_class.qty input');
//                    .nextAll('.oe_form_field')
//                    .find('input')
//                    .first();


                console.log('Next input:', $inputField);

                if ($inputField.length) {
                    setTimeout(function() {
                        $inputField.focus();
                        console.log('Focused on next input field.');
                    }, 100);
                } else {
                    console.warn('Next input element not found.');
                }
            }
        });



$(document).ready(function () {
     $(document).on('mousedown', '.save_as_holding_invoice', function (event) {
//        console.log('clicked.................');
        $('.oe_form_button_save').trigger('click');
     });



    $(document).on('keydown', '.css_customer', function (event) {
        if (event.which === 13) { // Enter key
            var $productField = $(this);
            var tableRow = $productField.closest('tr');
            var label = tableRow.find('label').text().trim();

            if (label === "Customer") {
                // Remove the autocomplete-handled flag on every keydown to ensure it runs each time
                $productField.data('autocomplete-handled', false);

                if (!$productField.data('autocomplete-handled')) {
                    $productField.data('autocomplete-handled', true);

                    var $input = $productField.find('input');
                    console.log('Input field:', $input);

                    // Ensure the input field is found
                    if ($input.length === 0) {
                        console.log("Input field not found.");
                    }

                    var inputValue = $input.val() ? $input.val().trim() : "";
                    console.log('Detected input value:', inputValue);

                    // Ensure autocomplete is opened
                    if (!$input.data('autocomplete-opened')) {
                        $input.data('autocomplete-opened', true);

                        $input.one('autocompleteopen', function () {
                            setTimeout(function () {
                                $input.select();
                            }, 200);
                        });
                    }

                    setTimeout(function () {
                        var $ul = $("ul.ui-autocomplete");
                        var $items = $ul.find('li');
                        console.log('Dropdown items:', $items);

                        // Look for "Create" option matching the input value
                        var $createItem = $items.filter(function () {
                            var text = $(this).text().trim();
                            return text.startsWith('Create "') && text.endsWith('"') && text.includes(inputValue);
                        }).first();

                        if ($createItem.length > 0) {
                            console.log('Clicking Create item:', $createItem.text());
                            $createItem[0].click();
                        } else {
                            // Optionally handle other cases
                            var $highlightedItem = $items.filter('.ui-state-highlight').first();
                            if ($highlightedItem.length > 0) {
                                console.log('Clicking highlighted item:', $highlightedItem.text());
                                $highlightedItem[0].click();
                            } else {
                                console.log('No matching items found.');
                            }
                        }

                        // Optionally focus on another element after selecting
                        setTimeout(function () {
                            $('.css_phone').focus();
                        }, 200);
                    }, 100);
                }
            }
        }
    });
$(document).on('keydown', '.oe_form_field_many2one[data-fieldname="product_id"]', function (event) {
    if (event.which === 13) { // Enter key
        var $productField = $(this);
        var $input = $productField.find('input');

        console.log('Input field:', $input);


        if ($input.length === 0) {
            console.log("Input field not found.");
            return;
        }

        var inputValue = $input.val() ? $input.val().trim() : "";
        console.log('Detected input value:', inputValue);

        setTimeout(function () {
            var $ul = $("ul.ui-autocomplete");
            var $items = $ul.find('li');
            console.log('Dropdown items:', $items);


            var $createItem = $items.filter(function () {
                var text = $(this).text().trim();
                return text.startsWith('Create "') && text.endsWith('"') && text.includes(inputValue);
            }).first();

            if ($createItem.length > 0) {
                console.log('Clicking Create item:', $createItem.text());
                $createItem[0].click();
            } else {

                var $highlightedItem = $items.filter('.ui-state-highlight').first();
                if ($highlightedItem.length > 0) {
                    console.log('Clicking highlighted item:', $highlightedItem.text());
                    $highlightedItem[0].click();
                } else {
                    console.log('No matching items found.');
                }
            }


            setTimeout(function () {
                $('.potency').focus();
            }, 200);
        }, 100);
    }
});
$(document).on('keydown', '.potency', function (event) {
    if (event.which === 13) {
        event.preventDefault();
        $('span.custom_batch input').focus();
    }
});



    // Handle item click in the autocomplete list
    $(document).on('click', 'ul.ui-autocomplete li', function () {
        var selectedItemText = $(this).text().trim();
        console.log('Item clicked:', selectedItemText);
    });

    // Reset the autocomplete-handled flag when the input value changes
    $(document).on('input', '.css_customer input', function () {
        $(this).closest('.css_customer').data('autocomplete-handled', false);
    });
});










