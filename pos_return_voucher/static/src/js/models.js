/* Copyright 2023 Aures Tic - Jose Zambudio
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("pos_return_vocher.models", function (require) {
    "use strict";

    const models = require("point_of_sale.models");
    models.load_fields("pos.payment.method", ["return_voucher"]);

    const superPaymentline = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        initialize: function (attr, options) {
            superPaymentline.initialize.call(this, attr, options);
            this.posReturnVoucherId = null;
        },
        export_as_JSON: function () {
            const json = superPaymentline.export_as_JSON.call(this);
            json.pos_return_voucher_id = this.posReturnVoucherId;
            return json;
        },
        init_from_JSON: function (json) {
            superPaymentline.init_from_JSON.apply(this, arguments);
            this.posReturnVoucherId = json.pos_return_voucher_id;
        },
        setReturnVoucherId: function (id) {
            this.posReturnVoucherId = id;
        },
    });

    return models;
});
