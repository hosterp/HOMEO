$(document).on("shown.bs.modal", function () {
setTimeout(function(){
$('.tree_class table').DataTable();
  $('input[type="search"]').focus();
  resetFieldValue();
//$('419').DataTable();
}, 500)
});
function resetFieldValue() {
    var field = $('td[data-field="quantity_selected"]');
    if (field.length > 0) {
        field.text('0');
        console.log('Resetting field value...');
    } else {
        console.error('Field not found.');
    }
}

