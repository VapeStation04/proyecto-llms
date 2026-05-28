/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class CustomGridPopup extends Component {
    static template = "vape_pos_order_fields.CustomGridPopup";
    static components = { Dialog };

    static props = ["title", "list", "getPayload", "close"];

    selectItem(item) {
        if (this.props.getPayload) {
            this.props.getPayload(item);
        }
        this.props.close();
    }
}