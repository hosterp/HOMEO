
//JS16AK11HI2022L
openerp.Key_shortcuts = function (jQuery) {
//    $(document).bind('keydown', 'f2', function assets() {
////        window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&menu_id=441&action=395';
//        window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&action=395';
//    setTimeout(function(){
//    $('button.oe_button.oe_form_button_create').click();
//}, 4000)
//    });

$(document).ready(function () {
  $(document).on('focus', '.qty_class', function (e) {
        var target = e.target;
        setTimeout(function () {
            var keyPressEvent = $.Event('keypress');
            keyPressEvent.which = 13;
            keyPressEvent.keyCode = 13;
            $(target).trigger(keyPressEvent);
        }, 100);
    });

});
//    HARSHA'S CODE
$.shortcut = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null
        if(e.keyCode != 49 && (e.keyCode == key.charCodeAt(0) || e.keyCode == key)) {
            callback.apply(this, args);
            return false;
        }
    });
};

$.shortcut('113', function() {
    window.location.assign("/web#view_type=form&model=account.invoice&action=400");
        $('.oe_list_add').trigger('click');
        $('.oe_form_button_create').trigger('click');
//    $('.oe_form_button_create').each(function() {
//        if($(this).parents('div:hidden').length == 0){
//            $(this).trigger('click');
//        }
//    });
//
//	$('.oe_list_add').each(function() {
//            if($(this).parents('div:hidden').length == 0){
//                $(this).trigger('click');
//            }
//        });
});
$.shortcut('117', function() {
      window.location.assign("/web#view_type=form&model=account.invoice&action=408");
        $('.oe_list_add').trigger('click');
        $('.oe_form_button_create').trigger('click');
});
$.shortcut('116', function() {
      window.location.assign("/web#view_type=form&model=account.invoice&action=409");
        $('.oe_list_add').trigger('click');
        $('.oe_form_button_create').trigger('click');
});
$.shortcut('114', function() {
	$('.css_hiworth').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
			 resetFieldValue();
		}
	});
});


$.shortcut('107', function() {
	$('.btn_txt').first().each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
	$('.oe_required:even').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
			// $(this).focus();
		}
	});
});
$.shortcut('16', function() {
	$('.oe_required:even').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
			// $(this).focus();
		}
	});
});

//$.shortcut('16', function() {
//	$('.oe_required').odd().each(function() {
//		if($(this).parents('div:hidden').length == 0){
//		    $(this).trigger('click');
////			$(this).focus();
//		}
//	});
//});
$.shortcut('123', function() {
//     $('.cus_validate').each(function() {
//        if($(this).parents('div:hidden').length == 0){
//			$(this).trigger('click');
//        }
//    });
//    $('.supplier_validate').each(function() {
//        if($(this).parents('div:hidden').length == 0){
//            $(this).trigger('click');
//        }
//    });

    $('.oe_form_button_save').each(function() {
        if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
        }
    });

//    if (confirm("if you want to save?")) {
//        $('.oe_form_button_save').each(function() {
//            if($(this).parents('div:hidden').length == 0){
//                    $(this).trigger('click');
//
//            }
//        });
//        txt = "You pressed OK!";
//    } else {
//      txt = "You pressed Cancel!";
//    }

});

$.shortcut('121', function() {
//	$('.oe_form_button_save').each(function() {
//		if($(this).parents('div:hidden').length == 0){
//                $(this).trigger('click');
//		}
//	});
	    setTimeout(function() {
            $('.css_print').each(function() {
                if($(this).parents('div:hidden').length == 0){
                    $(this).trigger('click');

                }
            });
        }, 3000)
});

$.shortcut('123', function() {
	$('.oe_form_button_save').each(function() {
	    console.log("working f12")
		if($(this).parents('div:hidden').length == 0){
                $(this).trigger('click');
		}
	});

//ashik new stock
$(document).ready(function() {
    $('input[name="quantity_selected"]').keydown(function(event) {
        console.log("Key pressed: " + event.key);
        if (event.key === "Enter") {
            console.log("Enter key pressed in quantity_selected field");
            event.preventDefault();    // Prevent the default Enter key behavior
            event.stopPropagation();   // Stop the event from bubbling up
            return false;              // Ensure that no further action is taken
        }
    });
});

//end
//	    setTimeout(function() {
//            $('.css_print').each(function() {
//                if($(this).parents('div:hidden').length == 0){
//                    $(this).trigger('click');
//
//                }
//            });
//        }, 3000)
});

$(document).ready(function(){
    $(document).on('blur', "input[type=text],textarea", function () {
        $(this).val(function (_, val) {
            return val.toUpperCase();
        });
    });
    $(document).on('click' , '.field_boolean', function(){
        var q_bal = $(this).parent('span[data-fieldname="select"]').siblings('span.oe_form_field[data-fieldname="residual"]').children('span.oe_form_char_content').text();
        var amount = $('.payment_total_calculation').children('span.oe_form_field_float').children('span.oe_form_char_content').text();
        var add_balance = parseFloat(q_bal);
        var balance = parseFloat(amount);
        var isChecked = $(this).prop('checked');
        if (isChecked === true) {
            var total = balance + add_balance
            $('.oe_form_char_content:eq(1)').text(total);
            console.log('The checkbox is checked.');
        } else {
            var total = balance - add_balance
            $('.oe_form_char_content:eq(1)').text(total);
            console.log('The checkbox is not checked.');
        }
    });

});
//$(document).ready(function(){
//    $(document).on('click','span.oe_form_char_content',function(){
//        var nearestparent = $(this).parent('span.oe_form_field').closest('span.oe_form_field[data-fieldname="test"]');
//        if (!$(nearestparent).hasClass("testidddd")){
//            $(nearestparent).addClass('testidddd');
//        }
//        var idspan = nearestparent.children('span.oe_form_char_content');
//        var testid = idspan.text();
//        var id = parseInt(testid);
//        window.location.assign("/web#id="+id+"&view_type=form&model=account.invoice&action=400");
//    });
//});
//class="oe_list oe_view oe_list_editable oe_editing"


$(document).ready(function() {
    $(document).on('keydown', 'input[type="text"][placeholder="Select customer"]', function(event) {
        if (event.keyCode === 13) {
            $(".open_customer").trigger('click');
        }
    });
    $(document).on('keydown','input[type="text"][placeholder="select supplier"]', function(event) {
        if (event.keyCode === 13) {
            var inputValue = $(this).val().trim();
            if (inputValue !== "") {
                $(".supplier_invo").trigger('click');
            } else {
                $(this).next('input').focus();
            }
        }
    });

    $(document).on('keydown', 'input[type="text"][placeholder="Select Hold Bill"]', function(event) {
        if (event.keyCode === 13) {
            $(".Hold_Bill").trigger('click');
        }
    });
    $(document).on('keydown', 'input[type="text"][placeholder="Select Packing slip"]', function(event) {
        if (event.keyCode === 13) {
            $(".open_pack").trigger('click');
        }
    });
    $(document).on('keydown', 'input[type="text"][placeholder="Select customer_invoice"]', function(event) {
        if (event.keyCode === 13) {
            $(".pack_customer").trigger('click');
        }
    });
});





//console.log('f3');
     quantity=$('[id^="DataTables_Table_"] tbody td[data-field="quantity_selected"]')
//    ROBIN'S CODE
    $( document ).ready(function() {
//         $(window).on("hashchange", function() {
//            var urlHash = window.location.hash;
//            if (urlHash.includes('model=partner.payment') && urlHash.includes('menu_id=346')) {
//    //            alert('ready');
//                $(document).on("change", function() {
//                    $(".oe_form_button_save").trigger('click');
//                });
//            }
//            else {
//
//                $(document).off("change");
//            }
//        });



    //For adding class to html tag
    var newClass = window.location.href;
    newClass = newClass.substring(newClass.indexOf('&action=') + 1).replace('=', '-num');
    $('html').addClass(newClass);
    // For adding tr to supplier table


//VINCODES
  $(document).on('keyup', '.dataTables_filter input[type="search"]', function (event) {
  if (event.keyCode === 13) {
     var quantityField = $('[id^="DataTables_Table_"] tbody tr:first-child td[data-field="quantity_selected"]');
     quantityField.click();
       if (quantityField.closest('tr').next('tr').length >= 0) {
        quantityField.click();
//        alert('click');
        }
        else{
               $('.close').click();
        }
    }

     let lastKeyPressTime = 0;
//    const doubleClickInterval = 500; // Time interval to consider as a double click (in milliseconds)
//     $(document).on('keyup', quantity, function (event) {
//        if (event.keyCode === 32 && !$(':focus').is('.dataTables_filter input[type="search"]')) {
//            $('.close').click();
//    }
//});

//new ashik
//$(document).on('keydown', quantity, function (event) {
//    if (event.keyCode === 32 && !$(':focus').is('.dataTables_filter input[type="search"]')) {
//        // Close the current dialog or modal
//        $('.close').click();
//
//        // Add a delay before triggering the click and setting focus
//        setTimeout(function() {
//            // Trigger the click on the add row button
//            $('.oe_form_field_one2many_list_row_add a').trigger('click');
//
//            // Set focus to the product_id field after the row is added
//            $('.oe_form_field_many2one[data-fieldname="product_id"]').focus();
//
//            console.log('clicked...............');
//        }, 1000); // 200ms delay
//    }
//});

//var addRowTriggered = false;
//
//$(document).on('keydown', function (event) {
//  if (event.keyCode === 32 && !$(document.activeElement).hasClass('dataTables_filter') && !addRowTriggered) {
//    // Close any open dialogs/modals
//    $('.modal').modal('hide');
//
//    // Set the flag to true to prevent multiple triggers
//    addRowTriggered = true;
//
//    // Add a delay before triggering the click and setting focus
//    setTimeout(function() {
//      // Trigger the click on the add row button
//      $('.oe_form_field_one2many_list_row_add a')[0].click();
//
//      // Set focus back to the product_id field after a short delay
//      setTimeout(function() {
//        $('#product_id_field').focus();
//      }, 100); // 100ms delay
//
//      console.log('clicked...............');
//
//      // Reset the flag after the timeout
//      setTimeout(function() {
//        addRowTriggered = false;
//      }, 500); // 500ms delay
//    }, 1000); // 200ms delay
//  }
//});


//    quantity = $('[id^="DataTables_Table_"] tbody td[data-field="quantity_selected"]');
//    $(document).on('keyup', quantity, function (event) {
//        if (event.keyCode === 32)  {
//            $('.close').click();
////            const currentKeyPressTime = new Date().getTime();
////            const timeSinceLastKeyPress = currentKeyPressTime - lastKeyPressTime;
////            lastKeyPressTime = currentKeyPressTime;
////             if (timeSinceLastKeyPress < doubleClickInterval) {
////                    $('.close').click();
////                }
//            }
//
//    });

    var quantitySelectedField = '[id^="DataTables_Table_"] tbody td[data-field="quantity_selected"]';

//    $(document).on('keyup', quantitySelectedField, function (event) {
//        if (event.keyCode === 32) {
//            $(this).trigger('change');
////            $('.close').click(); //
//        }
//    });




//     quantity=$('[id^="DataTables_Table_"] tbody td[data-field="quantity_selected"]')
//     $(document).on('keyup',quantity,function (event) {
//        if (event.keyCode.dbclick()=== 13) {
//            $('.close').click();
//        }
//     });
  });

 $(document).on('keyup', '.css_hiworth', function (event) {
    if (event.keyCode === 13) {
        $('.oe_form_field_one2many_list_row_add a').trigger('click');
    }
  });
  $(document).on('keyup', '.doctor', function (event) {
    if (event.keyCode === 13) {
        $('.oe_form_field_one2many_list_row_add a').trigger('click');
    }
  });
  $(document).on('keyup', '.next_line', function (event) {
    if (event.keyCode === 13) {
        $('.oe_form_field_one2many_list_row_add a').trigger('click');
    }
  });
 $(document).on('keyup', '.hiworth', function (event) {
    if (event.keyCode === 13) {
        var firstRow = document.querySelector('tr[data-id^="one2many_v_id_"]');
        if (firstRow) {
            var productOfField = firstRow.querySelector('td[data-field="product_of"]');
            if (productOfField) {
                productOfField.click();
            }
        } else {
           $('.oe_form_field_one2many_list_row_add a').trigger('click');
           setTimeout(function() {
                var productOfInput = $('span[data-fieldname="product_of"] input');
                productOfInput.val('');
            }, 100)

        }
    }
});


  $(document).on('keydown', '.rack input[type="text"]', function() {
     if (event.keyCode === 13) {
    // Trigger the click event on .oe_form_field_one2many_list_row_add a
    $('.oe_form_field_one2many_list_row_add a').trigger('click');
    }
 });

 $(document).on('keyup', '.hsn', function (event) {
    if (event.keyCode === 13) {
        $('.oe_form_field_one2many_list_row_add a').trigger('click');
    }
  });



    });
    $("button.oe_button.oe_list_add").on('click', function() {
        $('.oe_notebook_page.ui-tabs-panel.ui-widget-content .abhi_custom .oe_form_field .oe_view_manager_wrapper .oe_view_manager_body .oe_view_manager_view_list table.oe_list_content > tbody:last-child').append('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
    });

//    $( "oe_button oe_form_button_create" ).click(function() {
    $("button.oe_button.oe_form_button_create").on('click', function() {
//    alert( "Handler for .click() called." );
      $('.oe_notebook_page.ui-tabs-panel.ui-widget-content .abhi_custom .oe_form_field .oe_view_manager_wrapper .oe_view_manager_body .oe_view_manager_view_list table.oe_list_content > tbody:last-child').append('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');

    });

//END


};

//jQuery(function($) {
//
//  $(window).load(function() {
//
//    var $gal = $(".oe_notebook_page"),
//      galW = $gal.outerWidth(true),
//      galSW = $gal[0].scrollWidth,
//      wDiff = (galSW / galW) - 1, // widths difference ratio
//      mPadd = 60, // Mousemove Padding
//      damp = 20, // Mousemove response softness
//      mX = 0, // Real mouse position
//      mX2 = 0, // Modified mouse position
//      posX = 0,
//      mmAA = galW - (mPadd * 2), // The mousemove available area
//      mmAAr = (galW / mmAA); // get available mousemove fidderence ratio
//
//    $gal.mousemove(function(e) {
//      mX = e.pageX - $(this).offset().left;
//      mX2 = Math.min(Math.max(0, mX - mPadd), mmAA) * mmAAr;
//    });
//
//    setInterval(function() {
//      posX += (mX2 - posX) / damp; // zeno's paradox equation "catching delay"
//      $gal.scrollLeft(posX * wDiff);
//    }, 10);
//
//  });
//
//});

//new ashik
//$(document).on('keydown', quantity, function (event) {
//    if (event.keyCode === 32 && !$(':focus').is('.dataTables_filter input[type="search"]')) {
//        // Close the current dialog or modal
//        $('.close').click();
//
//        // Add a delay before triggering the click and setting focus
//        setTimeout(function() {
//            // Trigger the click on the add row button
//            $('.oe_form_field_one2many_list_row_add a').trigger('click');
//
//            // Set focus to the product_id field after the row is added
//            $('.oe_form_field_many2one[data-fieldname="product_id"]').focus();
//
//            console.log('clicked...............');
//        }, 1000); // 200ms delay
//    }
//});


// working code
//var addRowTriggered = false;
//
//$(document).on('keydown', function (event) {
//  if (event.keyCode === 32 && !$(document.activeElement).hasClass('dataTables_filter') && !addRowTriggered) {
//    // Close any open dialogs/modals
//    $('.modal').modal('hide');
//
//    // Set the flag to true to prevent multiple triggers
//    addRowTriggered = true;
//
//    // Add a delay before triggering the click and setting focus
//    setTimeout(function() {
//      // Trigger the click on the add row button
//      $('.oe_form_field_one2many_list_row_add a')[0].click();
//
//      // Set focus back to the product_id field after a short delay
//      setTimeout(function() {
//        $('#product_id_field').focus();
//      }, 100); // 100ms delay
//
//      console.log('clicked...............');
//
//      // Reset the flag after the timeout
//      setTimeout(function() {
//        addRowTriggered = false;
//      }, 500); // 500ms delay
//    }, 1000); // 200ms delay
//  }
//});
// end here

//  old space
//var addRowTriggered = false;
//
//$(document).on('keydown', function (event) {
//  if (event.keyCode === 32 && !$(':focus').is('.dataTables_filter input[type="search"]') && !addRowTriggered) {
//    // Close any open dialogs/modals
//    $('.modal').modal('hide');
//
//    // Set the flag to true to prevent multiple triggers
//    addRowTriggered = true;
//
//    console.log('Spacebar pressed, initiating row check and addition.');
//
//    // Add a delay before triggering the click and setting focus
//    setTimeout(function() {
//      // Find all rows in the one2many list
//      var rows = $('.oe_form_field_one2many_list .oe_form_field_one2many_list_row');
//      console.log('All rows found:', rows);
//
//      // Get the last row and the previous row
//      var lastRow = rows.last();
//      var previousRow = lastRow.prev();
//      console.log('Last row found:', lastRow);
//      console.log('Previous row found:', previousRow);
//
//      // Check if previousRow exists and has a product_id field
//      if (previousRow.length) {
//        var previousProductField = previousRow.find('.oe_form_field #product_id_field');
//        console.log('Previous product_id field value:', previousProductField.val());
//
//        // Check if the product_id field in the previous row is empty
//        if (previousProductField.val() === '') {
//          console.log('Previous product_id field is empty. Focusing on it.');
//          previousProductField.focus();
//        } else {
//          // Trigger the click on the add row button
//          console.log('Previous product_id field is not empty. Adding a new row.');
//          $('.oe_form_field_one2many_list_row_add a').first().click();
//
//          // Set focus back to the product_id field of the new row after a short delay
//          setTimeout(function() {
//            var newProductField = $('.oe_form_field_one2many_list .oe_form_field_one2many_list_row').last().find('#product_id_field');
//            newProductField.focus();
//            console.log('Focused on the new product_id field.');
//          }, 100); // 100ms delay
//        }
//      } else {
//        // If no previous row, add a new row and set focus
//        console.log('No previous row found. Adding a new row.');
//        $('.oe_form_field_one2many_list_row_add a').first().click();
//
//        // Set focus back to the product_id field of the new row after a short delay
//        setTimeout(function() {
//          var newProductField = $('.oe_form_field_one2many_list .oe_form_field_one2many_list_row').last().find('#product_id_field');
//          newProductField.focus();
//          console.log('Focused on the new product_id field.');
//        }, 100); // 100ms delay
//      }
//
//      // Reset the flag after the timeout
//      setTimeout(function() {
//        addRowTriggered = false;
//        console.log('Add row triggered flag reset.');
//      }, 500); // 500ms delay
//    }, 1000); // 1000ms delay
//  }
//});



//prevent qty field to be edited starts here
$(document).ready(function() {
    // Function to disable all buttons
    function disableButtons() {
        $('button').each(function() {
            $(this).data('enabled', !$(this).is(':disabled')); // Save current state
            $(this).prop('disabled', true); // Disable button
        });
    }

    // Function to restore buttons to their previous state
    function restoreButtons() {
        $('button').each(function() {
            if ($(this).data('enabled') !== undefined) {
                $(this).prop('disabled', !$(this).data('enabled')); // Restore previous state
            }
        });
    }

    // When focusing on qty field
    $('.qty_class input').on('focus', function() {
        disableButtons(); // Disable all buttons
    });

    // When leaving the qty field
    $('.qty_class input').on('blur', function() {
        restoreButtons(); // Restore all buttons
    });

    // Handle keydown events
    $(document).on('keydown', function(e) {
        if ($('.qty_class input').is(':focus') && e.key === 'Enter') {
            restoreButtons(); // Restore buttons if Enter key is pressed
        } else if ($('.qty_class input').is(':focus')) {
            e.preventDefault(); // Prevent all other keys
        }
    });
});
//prevent qty field to be edited ends here








// sapcebar to exit search wizard

var addRowTriggered = false;

$(document).on('keydown', function (event) {
  if (event.keyCode === 32 && !$(':focus').is('.dataTables_filter input[type="search"]') && !addRowTriggered) {
    // Check if the specific modal is open
    var modalTitle = $('.modal .modal-title').text().trim();
    if (modalTitle !== "Search Stock In Tree") {
      return; // Exit if the modal title doesn't match
    }
     var target = event.target;
     var keyPressEvent = $.Event('keypress');
            keyPressEvent.which = 13;
            keyPressEvent.keyCode = 13;
            $(target).trigger(keyPressEvent);


        setTimeout(function() {
            $('.modal').modal('hide');
            console.log('Modal is now closed');
        }, 300);
    addRowTriggered = true;

    console.log('Spacebar pressed, initiating row check and addition.');

    // Add a delay before triggering the click and setting focus
    setTimeout(function() {
      // Find all rows in the one2many list containing product_id field
      var rows = $('.openerp .oe_list .oe_form_container .oe_form .oe_form_container.oe_form_nosheet span.oe_form_field.required_class input');
      console.log('All rows found:', rows);

      // Get the last row and the previous row
      var lastRow = rows.first();
      console.log('Last row found:', lastRow);

      // Check if previousRow exists and has a product_id field
      if (lastRow.length) {
        var previousProductField = lastRow;
        console.log('Previous product_id field value:', previousProductField.val());

        // Check if the product_id field in the previous row is empty
        if (previousProductField.val() === '') {
          var quantityField = $('[id^="DataTables_Table_"] tbody tr:first-child td[data-field="quantity_selected"]');
          var t = $('.oe_list_content tbody td[data-field="product_id"]');
          console.log('Previous product_id field is empty. Focusing on it.');
          t.click();
        } else {
          // Trigger the click on the add row button
          console.log('Previous product_id field is not empty. Adding a new row.');
          $('.oe_form_field_one2many_list_row_add a').first().click();

          // Set focus back to the product_id field of the new row after a short delay
          setTimeout(function() {
            var newProductField = $('tr:has(td:has(input[name="product_id"]))').last().find('input[name="product_id"]');
            newProductField.focus();
            console.log('Focused on the new product_id field.');
          }, 100); // 100ms delay
        }
      } else {
        // If no previous row, add a new row and set focus
        console.log('No previous row found. Adding a new row.');
        $('.oe_form_field_one2many_list_row_add a').first().click();

        // Set focus back to the product_id field of the new row after a short delay
        setTimeout(function() {
          var newProductField = $('tr:has(td:has(input[name="product_id"]))').last().find('input[name="product_id"]');
          newProductField.focus();
          console.log('Focused on the new product_id field.');
        }, 100); // 100ms delay
      }

      // Reset the flag after the timeout
      setTimeout(function() {
        addRowTriggered = false;
        console.log('Add row triggered flag reset.');
      }, 500); // 500ms delay
    }, 1000); // 1000ms delay
  }
});

//ends here
