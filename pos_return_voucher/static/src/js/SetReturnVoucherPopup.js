odoo.define("pos_edit_order_line.SetReturnVoucherPopup", function (require) {
    "use strict";

    const {useState, useRef} = owl.hooks;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const framework = require("web.framework");

    class SetReturnVoucherPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({
                id: false,
                name: "",
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
                name: this.state.name,
                amount: this.state.amount,
            };
        }
        async searchReturnVoucher(event) {
            const inputName = event.target.value;
            if (inputName.length > 0) {
                const {
                    id,
                    name,
                    amount,
                    max_validity_date,
                } = await this._getReturnVoucher(inputName);
                this.state.id = id || false;
                this.state.name = name || "";
                this.state.amount = amount || 0.0;
                this.state.max_validity_date = max_validity_date || false;
            }
        }
        async _getReturnVoucher(name) {
            let voucherData = {};
            framework.blockUI();

            const data = await this.rpc({
                model: "pos.return.voucher",
                method: "search_read",
                args: [
                    [
                        ["name", "=", name],
                        ["state", "=", "active"],
                    ],
                    ["id", "name", "amount", "max_validity_date"],
                ],
            });
            framework.unblockUI();

            if (data.length > 0) {
                voucherData = data[0];
            } else {
                this.showPopup("ErrorPopup", {
                    title: this.env._t("Error"),
                    body: this.env._t("Return voucher not found."),
                });
            }

            return voucherData;
        }

        async confirm() {
            this.props.resolve(this.getPayload());
            this.trigger("close-popup");
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
