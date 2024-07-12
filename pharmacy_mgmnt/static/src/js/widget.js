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

        // Define a function to perform the actions
        function performActions() {
            var validateButton = document.querySelector('.cus_validate');
            if (validateButton) {
                var invoiceLine = self.datarecord.invoice_line;
                console.log(invoiceLine);
                if (invoiceLine && invoiceLine.length > 0) {
                    var recordDelete = document.querySelector('.record_delete');
                    var payButton = document.querySelector('.invoice_pay_customer');

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

                    clickElement(recordDelete, 200)
                        .then(function() {
                            return clickElement(validateButton, 1000);
                        })
                        .then(function() {
                            return clickElement(payButton, 1000);
                        });
                } else {
                    self.do_warn('Warning', 'No invoice line');
                }
            } else {
                console.log("validateButton not found");
            }
        }

        // Attach the performActions function to the save button click event
        this.$buttons.find('.oe_form_button_save').click(function() {
             setTimeout(function() {
                 performActions();
            }, 100);
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
};


