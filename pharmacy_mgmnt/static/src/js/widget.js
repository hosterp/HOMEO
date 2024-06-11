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
            this.$buttons.find('.oe_form_button_save').click(function() {
                var validateButton = document.querySelector('.cus_validate');
                var payButton = document.querySelector('.invoice_pay_customer');

                if (validateButton) {
                    validateButton.click();
                }

                if (payButton) {
                    setTimeout(function() {
                        payButton.click();
                    }, 1000);
                }
            });
        },
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
};


