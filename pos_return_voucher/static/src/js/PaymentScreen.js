/* Copyright 2023 Aures Tic - Jose Zambudio
   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("pos_return_voucher.ReturnVoucherScreen", function (require) {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    const ReturnVoucherScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async addNewPaymentLine({detail: paymentMethod}) {
                const prevPaymentLines = this.currentOrder.paymentlines.clone();
                let res = false;
                if (paymentMethod.return_voucher && this.currentOrder.get_due() > 0) {
                    console.log("Mostramos los vales? buscador de vales en un popup?");
                    const {id, amount} = await this.showPopup("SetReturnVoucherPopup", {
                        title: this.env._t("Set return voucher"),
                    });
                    res = super.addNewPaymentLine(...arguments);
                    const newPaymentline = this.currentOrder.paymentlines.filter(
                        (item) => {
                            return !prevPaymentLines.find(item);
                        }
                    );
                    if (
                        newPaymentline.length === 1 &&
                        id &&
                        amount < newPaymentline[0].amount
                    ) {
                        newPaymentline[0].set_amount(amount);
                        newPaymentline[0].setReturnVoucherId(id);
                    }
                } else {
                    res = super.addNewPaymentLine(...arguments);
                }
                return res;
            }
        };

    Registries.Component.extend(PaymentScreen, ReturnVoucherScreen);

    return ReturnVoucherScreen;
});
