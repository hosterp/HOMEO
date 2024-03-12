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
    $(document).on('keydown', '.oe_form_field_many2one', function(event) {
        var $currentField = $(this);
        var $createLabelElement = $('.oe_view_manager_body').find('li.ui-menu-item:first a:contains("Create")');
        if ($createLabelElement.length > 0 && event.which === $.ui.keyCode.ENTER) {
            $createLabelElement.click();
        }
    });

});