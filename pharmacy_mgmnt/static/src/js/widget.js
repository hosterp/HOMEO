openerp.pharmacy_mgmnt = function (instance) {
    var _t = instance.web._t;
    var _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.form.widgets.add('float_no_default', 'instance.pharmacy_mgmnt.FieldFloatNoDefault');

    instance.pharmacy_mgmnt.FieldFloatNoDefault = instance.web.form.FieldFloat.extend({
        init: function () {
            this._super.apply(this, arguments);

            // Set precision to 2 decimal places directly on the field
            this.node.attrs.digits = [16, 2];
        },
        render_value: function () {
            this._super.apply(this, arguments);
            var value = this.get('value');

            // Check if the decimal part is ".00" before rounding
            if (parseFloat(value) % 1 === 0) {
                value = parseFloat(value).toFixed(0);
            } else {
                value = parseFloat(value).toFixed(2);
            }

            if (value === "0") {
                this.$el.find('input').val(""); // Use this.$el to find the input element
            } else {
                this.$el.find('input').val(value);
            }
        },
    });
};
