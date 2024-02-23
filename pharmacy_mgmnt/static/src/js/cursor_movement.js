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
});