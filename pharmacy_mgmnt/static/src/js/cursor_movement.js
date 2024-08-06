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
//                console.log("First button found, triggering click...");
                firstButton.on('click', function() {
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

$(document).ready(function () {
    $(document).on('keypress', '.css_customer', function (event) {
        if (event.which === 13) {
            var $productField = $(this);
            var tableRow = $productField.closest('tr');
            var label = tableRow.find('label').text().trim();

            if (label === "Customer" && !$productField.data('autocomplete-handled')) {
                $productField.data('autocomplete-handled', true);

                var $input = $productField.find('input');

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
                               var $firstItem = $ul.find('li:eq(-2)');
                    // var $firstItem = $ul.find('a.ui-corner-all:contains("Create")');
                    if ($firstItem.length > 0) {
                        $firstItem[0].click();
                         setTimeout(function () {
                            $('.css_phone').focus();
                        }, 200);
                        // $firstItem.data('clicked', true);
                    }
                }, 100);
            }
        }
    });
});
//$(document).ready(function() {
//    // Function to save the value of a specific field to local storage
//    function saveFieldValue(fieldName) {
//        var $fieldContainer = $('.oe_form_field_many2one[data-fieldname="' + fieldName + '"]');
//        if ($fieldContainer.length === 0) {
//            console.error('Field container not found for field:', fieldName);
//            return;
//        }
//        var $inputField = $fieldContainer.find('.ui-autocomplete-input');
//        var value = $inputField.val().trim();
//        localStorage.setItem('field_value_' + fieldName, value);
//        console.log('Saved value for field ' + fieldName + ':', value);
//    }
//
//    // Function to load and set the value of a specific field from local storage
//    function loadFieldValue(fieldName) {
//        var value = localStorage.getItem('field_value_' + fieldName);
//        if (value !== null) {
//            var $fieldContainer = $('.oe_form_field_many2one[data-fieldname="' + fieldName + '"]');
//            if ($fieldContainer.length === 0) {
//                console.error('Field container not found for field:', fieldName);
//                return;
//            }
//            var $inputField = $fieldContainer.find('.ui-autocomplete-input');
//            $inputField.val(value);
//            console.log('Loaded value for field ' + fieldName + ':', value);
//        } else {
//            console.log('No value found in local storage for field ' + fieldName + '.');
//        }
//    }
//
//    // Function to copy values from the previous line if fields match
//    function copyGroupValueIfFieldsMatch() {
//        var $lines = $('tr[data-id]'); // Ensure this matches your HTML structure
//        $lines.each(function(index) {
//            if (index > 0) {
//                var $currentLine = $(this);
//                var $previousLine = $lines.eq(index - 1);
//
//                // Retrieve and trim field values
//                var currentProduct = $currentLine.find('[data-fieldname="product_id"]').val().trim();
//                var previousProduct = $previousLine.find('[data-fieldname="product_id"]').val().trim();
//
//                var currentPotency = $currentLine.find('[data-fieldname="medicine_name_subcat"]').val().trim();
//                var previousPotency = $previousLine.find('[data-fieldname="medicine_name_subcat"]').val().trim();
//
//                var currentPacking = $currentLine.find('[data-fieldname="medicine_name_packing"]').val().trim();
//                var previousPacking = $previousLine.find('[data-fieldname="medicine_name_packing"]').val().trim();
//
//                var currentCompany = $currentLine.find('[data-fieldname="company_id"]').val().trim();
//                var previousCompany = $previousLine.find('[data-fieldname="company_id"]').val().trim();
//
//                // Debug information
//                console.log('Comparing values at index', index);
//                console.log('Current Product:', currentProduct, 'Previous Product:', previousProduct);
//                console.log('Current Potency:', currentPotency, 'Previous Potency:', previousPotency);
//                console.log('Current Packing:', currentPacking, 'Previous Packing:', previousPacking);
//                console.log('Current Company:', currentCompany, 'Previous Company:', previousCompany);
//
//                // Copy group value if all fields match
//                if (currentProduct === previousProduct && currentPotency === previousPotency && currentPacking === previousPacking && currentCompany === previousCompany) {
//                    var groupValue = $previousLine.find('[data-fieldname="medicine_grp"]').val().trim();
//                    $currentLine.find('[data-fieldname="medicine_grp"]').val(groupValue);
//                    console.log('Copied group value to line at index', index);
//                } else {
//                    console.log('Values do not match for line at index', index);
//                }
//            }
//        });
//    }
//
//    // Event handler to save the field value when it gains focus
//    $(document).on('focus', '.oe_form_field_many2one[data-fieldname]', function(event) {
//        var fieldName = $(this).data('fieldname');
//        saveFieldValue(fieldName);
//    });
//
//    // Event handler to save the field value and copy group value when it changes
//    $(document).on('change', '.oe_form_field_many2one[data-fieldname] .ui-autocomplete-input', function(event) {
//        var fieldName = $(this).closest('.oe_form_field_many2one').data('fieldname');
//        saveFieldValue(fieldName);
//        copyGroupValueIfFieldsMatch(); // Call this function when the field changes
//    });
//
//    // Function to load all field values from local storage
//    function loadAllFieldValues() {
//        $('.oe_form_field_many2one[data-fieldname]').each(function() {
//            var fieldName = $(this).data('fieldname');
//            loadFieldValue(fieldName);
//        });
//    }
//
//    // Load all field values when the document is ready
//    loadAllFieldValues();
//});
