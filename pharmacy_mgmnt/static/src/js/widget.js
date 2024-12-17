openerp.pharmacy_mgmnt = function (instance) {
    var _t = instance.web._t;
    var _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.form.widgets.add('float_no_default', 'instance.pharmacy_mgmnt.FieldFloatNoDefault');

    instance.pharmacy_mgmnt.FieldFloatNoDefault = instance.web.form.FieldFloat.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.node.attrs.digits = [16, 2];
        },
        render_value: function () {
            this._super.apply(this, arguments);
            var value = this.get('value');
            if (parseFloat(value) % 1 === 0) {
                value = parseFloat(value).toFixed(0);
            } else {
                value = parseFloat(value).toFixed(2);
            }
            if (value === "0") {
                this.$el.find('input').val("");
            } else {
                this.$el.find('input').val(value);
            }
        },
    });
   instance.web.FormView.include({
        load_form: function(data) {
            this._super(data);
            var self = this;


            function performActions(isBulkData) {
                var validateButton = document.querySelector('.cus_validate');
                if (validateButton) {
                    var invoiceLine = $('tr[data-id]');
                    console.log(invoiceLine.length);


                    var delays = isBulkData ? { delete: 1000, validate: 2000, pay: 3000 } : { delete: 500, validate: 1000, pay: 1500 };

                    if (invoiceLine.length > 0) {
                        var recordDelete = document.querySelector('.record_delete');
                        var payButton = document.querySelector('.password_class');

                        function clickElement(element, delay) {
                            return new Promise(function(resolve, reject) {
                                if (element) {
                                    setTimeout(function() {
                                        element.click();
                                        resolve();
                                    }, delay);
                                } else {
                                    resolve();
                                }
                            });
                        }

                        clickElement(recordDelete, delays.delete)
                            .then(function() {
                                return clickElement(validateButton, delays.validate);
                            })
                            .then(function() {
                                return clickElement(payButton, delays.pay);
                            })
                            .catch(function(error) {
                                console.error("Error during actions:", error);
                            });
                    } else {
                        self.do_warn('Warning', 'No invoice line');
                    }
                } else {
                    console.log("validateButton not found");
                }
            }

            // Determine if the data is bulk
            function isBulkData() {
                var invoiceLineCount = $('tr[data-id]').length;
                return invoiceLineCount > 10; // Define the threshold for bulk data
            }

            // Flag to prevent multiple event bindings
            var isHandlingSave = false;

           this.$buttons.find('.oe_form_button_save').click(function() {
                if (!isHandlingSave) {
                    isHandlingSave = true;


                    var packingInvoice = self.datarecord ? self.datarecord.packing_invoice : false;

                    if (!packingInvoice) {
                        console.log("Packing invoice is false, performing actions");
                        setTimeout(function() {
                            performActions(isBulkData());
                            isHandlingSave = false;
                        }, 100);
                    } else {
                         var printButton = document.querySelector('.css_print');
                         var passwordButton = document.querySelector('.password_class');
                         if(passwordButton){
                            passwordButton.click();
                            console.log("password_value button clicked");
                         }else{
                              console.warn("password_value button not found");
                         }
//                        if (printButton) {
//                            printButton.click();
//                            console.log("css_print button clicked");
//                        } else {
//                            console.warn("css_print button not found");
//                        }

                        console.log("Packing invoice is true, skipping actions");
                        isHandlingSave = false;
                    }
                }
           });

        }
   });



    instance.web.FormView.include({
        load_form: function() {
            this._super.apply(this, arguments);
            var self = this;
            var invoiceCancelButton = document.querySelector('.button_invoice_cancel');
            if (invoiceCancelButton) {
                invoiceCancelButton.addEventListener('click', function() {
                    var cancelButton = document.querySelector('.button_cancel_draft');
                    if (cancelButton) {
                        setTimeout(function() {
                            cancelButton.click();
                        }, 500);
                    }
                });
            }
        },
    });
    instance.web.FormView.include({
        load_form: function() {
            this._super.apply(this, arguments);
            var self = this;
            var invoiceCancelButton = document.querySelector('.oe_form_button_edit');
            if (invoiceCancelButton) {
                invoiceCancelButton.addEventListener('click', function() {
                    var cancelButton = document.querySelector('.button_invoice_cancel');
                    if (cancelButton) {
                        setTimeout(function() {
                            cancelButton.click();
                        }, 500);
                    }
                });
            }
        },
    });
     instance.web.FormView.include({
        load_form: function() {
            this._super.apply(this, arguments);


            var self = this;

            setTimeout(function() {
                var invoicePasswordSubmitButton = document.querySelector('.password_validate');
                if (invoicePasswordSubmitButton) {
                    console.log("Password validate button found!");

                    invoicePasswordSubmitButton.addEventListener('click', function() {
                        var passwordInput = document.querySelector('.password_value input');
                        if (!passwordInput) {
                            console.error("Password input field not found!");
                            return;
                        }

                        var password = passwordInput.value.trim();
                        console.log(password);
                        if (!password) {
                            console.error("Password is empty!");
                            return;
                        }

                        invoicePasswordSubmitButton.disabled = true;

                        $.ajax({
                            type: 'POST',
                            url: '/password/validate',
                            contentType: 'application/json',
                            data: JSON.stringify({ password: password }),

                            success: function(response) {
                                console.log("Password validation response:", response);

                                if (response.result.password_valid) {
                                    console.log("Password is valid!");

                                    var registerButton = document.querySelector('.invoice_pay_customer');
                                    var printButton = document.querySelector('.css_print');
                                    var packingInvoice = document.querySelector('.container[style="color:MediumSeaGreen; margin-left: 327px;"]');


                                    if (packingInvoice && packingInvoice.offsetParent !== null) {

                                        console.log("Packing slip exists and is visible. Clicking the print button...");
                                        if (printButton) {
                                            printButton.click();
                                        } else {
                                            console.error('Print button not found!');
                                        }
                                    } else {

                                        console.log("Packing slip not found or not visible. Clicking the register payment button...");
                                        if (registerButton) {
                                            setTimeout(function() {
                                                registerButton.click();
                                            }, 200);
                                        } else {
                                            console.log('Register button not found!');
                                        }
                                    }

                                } else {
//                                    alert(response.error_message || "Incorrect Password!");
                                }
                            },

                            error: function(xhr, status, error) {
                                console.error("Error validating password:", xhr.responseText || error);
                                alert("Error while validating password. Please try again.");
                            },
                            complete: function() {
                                invoicePasswordSubmitButton.disabled = false;
                            }
                        });
                    });
                } else {
                    console.log('Password validate button not found!');
                }
            }, 200);
        },
    });

    instance.web.FormView.include({
        load_form: function() {
            this._super.apply(this, arguments);

            setTimeout(function() {
                var invoicePasswordSubmitButton = document.querySelector('.payment_password_validate');
                if (invoicePasswordSubmitButton) {
                    console.log("Password validate button found!");

                    invoicePasswordSubmitButton.addEventListener('click', function() {
                        var passwordInput = document.querySelector('.password_value input');
                        if (!passwordInput) {
                            console.error("Password input field not found!");
                            return;
                        }

                       var password = passwordInput.value.trim();
                       console.log(password);
                        if (!password) {
                            console.error("Password is empty!");
                            return;
                        }
                        invoicePasswordSubmitButton.disabled = true;
                        $.ajax({
                            type: 'POST',
                            url: '/payment/password/validate',
                            contentType: 'application/json',
                            data: JSON.stringify({ password: password }),

                            success: function(response) {
                                console.log("Password validation response:", response);

                                if (response.result.password_valid) {
                                    console.log("Password is valid!");
                                    var registerButton = document.querySelector('.payment_button');
                                    if (registerButton) {
                                        console.log("Clicking the register button...");
                                        setTimeout(function() {
                                            registerButton.click();
                                        }, 200);
                                    } else {
                                        console.error('Register button not found!');
                                    }
                                } else {
//                                    alert(response.error_message || "Incorrect Password!");
                                }
                            },
                            error: function(xhr, status, error) {
                                console.error("Error validating password:", xhr.responseText || error);
                                alert("Error while validating password. Please try again.");
                            },
                            complete: function() {
                                invoicePasswordSubmitButton.disabled = false;
                            }
                        });
                    });
                } else {
                    console.error('Password validate button not found!');
                }
            }, 200);
        },
    });

};


