odoo.define("pos_edit_order_line.SetReturnVoucherPopup", function (require) {
    "use strict";

    const {useState, useRef} = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const framework = require("web.framework");
    const time = require("web.time");

    class SetReturnVoucherPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({
                id: false,
                pos_reference: "",
                amount: 0.0,
                max_validity_date: false,
            });
            this.inputRef = useRef("inputName");
        }
        mounted() {
            this.inputRef.el.focus();
        }
        getPayload() {
            return {
                id: this.state.id,
                pos_reference: this.state.pos_reference,
                amount: this.state.amount,
            };
        }
        async searchReturnVoucher(event) {
            const inputPosReference = event.target.value;
            if (inputPosReference.length > 0) {
                const {
                    id,
                    pos_reference,
                    amount,
                    max_validity_date,
                } = await this._getReturnVoucher(inputPosReference);
                this.state.id = id || false;
                this.state.pos_reference = pos_reference || "";
                this.state.amount = amount || 0.0;
                this.state.max_validity_date = max_validity_date || false;
            }
        }
        async _getReturnVoucher(pos_reference) {
            let voucherData = {};
            framework.blockUI();

            const data = await this.rpc({
                model: "pos.return.voucher",
                method: "search_read",
                args: [
                    [["order_id.pos_reference", "=", pos_reference]],
                    ["id", "pos_reference", "amount", "max_validity_date", "state"],
                ],
            });
            framework.unblockUI();

            try {
                if (data.length === 0)
                    throw Error(this.env._t("Return voucher not found."));
                voucherData = data[0];
                if (voucherData.state === "done")
                    throw Error(
                        this.env._t("The return voucher has already been used.")
                    );
                else if (voucherData.state === "expired")
                    throw Error(
                        this.env._t(
                            `The return voucher expired on ${this.datetime_to_str(
                                voucherData.max_validity_date
                            )}`
                        )
                    );
            } catch (error) {
                this.showPopup("ErrorPopup", {
                    title: this.env._t("Error"),
                    body: error.message,
                });
            }

            return voucherData;
        }
        async confirm() {
            this.props.resolve(this.getPayload());
            this.trigger("close-popup");
        }
        datetime_to_str(date) {
            return time.datetime_to_str(new Date(date));
        }
    }
    SetReturnVoucherPopup.template = "SetReturnVoucherPopup";
    SetReturnVoucherPopup.defaultProps = {
        confirmText: "Select return voucher",
        cancelText: "Cancel",
    };

    Registries.Component.add(SetReturnVoucherPopup);

    return SetReturnVoucherPopup;
});
