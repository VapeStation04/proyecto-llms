/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async loaded(data) {
        await super.loaded(...arguments);

        const posConfigId = this.config.id;

        const domain = [["pos_config_ids", "in", [posConfigId]]];

        this.vape_channels = await this.orm.searchRead(
            "vape.channel",
            domain,
            ["name"]
        );

        this.vape_shipping_types = await this.orm.searchRead(
            "vape.shipping.type",
            domain,
            ["name"]
        );
    },
});