/* Copyright 2023 Aures Tic - Jose Zambudio
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("pos_return_vocher.models", function (require) {
    "use strict";

    const models = require("point_of_sale.models");
    models.load_fields("pos.payment.method", ["return_voucher"]);

    const superOrder = models.Order.prototype;
    const superPaymentline = models.Paymentline.prototype;

    models.Paymentline = models.Paymentline.extend({
        initialize: function (attr, options) {
            superPaymentline.initialize.call(this, attr, options);
            this.emittedReturnVoucherId = null;
            this.redeemedReturnVoucherId = null;
        },
        export_as_JSON: function () {
            const json = superPaymentline.export_as_JSON.call(this);
            json.emitted_return_voucher_id = this.emittedReturnVoucherId;
            json.redeemed_return_voucher_id = this.redeemedReturnVoucherId;
            return json;
        },
        init_from_JSON: function (json) {
            superPaymentline.init_from_JSON.apply(this, arguments);
            this.emittedReturnVoucherId = json.emitted_return_voucher_id;
            this.redeemedReturnVoucherId = json.redeemed_return_voucher_id;
        },
        set_redeemed_return_voucher: function (id) {
            this.redeemedReturnVoucherId = id;
        },
        export_for_printing: function () {
            const json = superPaymentline.export_for_printing.call(this);
            json.return_voucher =
                this.payment_method.return_voucher && this.get_amount() < 0;
            return json;
        },
    });

    models.Order = models.Order.extend({
        export_for_printing: function () {
            const json = superOrder.export_for_printing.call(this);
            json.return_voucher = json.paymentlines.some(
                (payment) => payment.return_voucher
            );
            return json;
        },
    });

    return models;
});
