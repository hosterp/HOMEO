$(document).ready(function(){
    var isHandlingFocus = false;

    $(document).on('keydown', ".oe_form_required", function (event) {
        var $this = $(this);
        var value = event.target.value;

        if ((event.which === 13 || event.which === 9) && !isHandlingFocus && value === "") {
            event.preventDefault();
            isHandlingFocus = true;
//            console.log("Required field is empty. Value:", value);
            $this.focus();
            isHandlingFocus = false;
        } else {
//            console.log("Field has value:", value);
            isHandlingFocus = false;
            $this.prop('selectionStart', $this.val().length);
        }
    });
//    $(document).on('keydown', '.oe_form_field_many2one', function(event) {
//        var $currentField = $(this);
//        var $createLabelElement = $('.oe_view_manager_body').find('li.ui-menu-item:first a:contains("Create")');
//        if ($createLabelElement.length > 0 && event.which === $.ui.keyCode.ENTER) {
//            $createLabelElement.click();
//        }
//    });
    $(document).on('focus', '.oe_form_field_many2one', function(event) {
        if (!$(this).data('clicked')) { // Check if the click event hasn't been triggered yet
            $(this).data('clicked', true); // Set the flag to indicate the click event has been triggered
            $(this).find('.oe_m2o_drop_down_button').click(); // Trigger click event on oe_m2o_drop_down_button
        }
    });

    $(document).on('blur', '.oe_form_field_many2one', function(event) {
        $(this).data('clicked', false); // Reset the flag when the field loses focus
    });


});