/** @odoo-module **/
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { onWillStart, useState } from "@odoo/owl"; 
import { CustomGridPopup } from "@vape_pos_order_fields/app/components/custom_grid_popup";

patch(PaymentScreen.prototype, {
    
    setup() {
        super.setup(...arguments);
        
        this.vapeState = useState({ renderTrigger: 0 });
        
        onWillStart(async () => {
            if (!this.pos.vape_channels) {
                const domain = [["pos_config_ids", "in", [this.pos.config.id]]];
                this.pos.vape_channels = await this.env.services.orm.searchRead(
                    "vape.channel",
                    domain,
                    ["name", "color", "icon", "custom_icon"]
                );
            }
            if (!this.pos.vape_shipping_types) {
                const domain = [["pos_config_ids", "in", [this.pos.config.id]]];
                this.pos.vape_shipping_types = await this.env.services.orm.searchRead(
                    "vape.shipping.type", 
                    domain, 
                    ["name"]
                );
            }
        });
    },

    openCustomPaymentPopup() {
        this.dialog.add(CustomGridPopup, {
            title: "Método de pago",
            list: this.payment_methods_from_config.map(m => ({ id: m.id, label: m.name, item: m })),
            getPayload: (selected) => {
                if (selected) this.addNewPaymentLine(selected);
            },
        });
    },

    async openChannelPopup() {
        this.dialog.add(CustomGridPopup, {
            title: "Seleccionar Canal de Venta",
            list: this.pos.vape_channels.map(c => ({ id: c.id, label: c.name, item: c, isChannel: true })),
            getPayload: (selected) => {
                if (selected) {
                    const channelId = selected.id || selected.item?.id || selected;
                    this.currentOrder.vs_channel_id = channelId;
                    
                    this.vapeState.renderTrigger++;
                }
            },
        });
    },

    async openShippingPopup() {
        this.dialog.add(CustomGridPopup, {
            title: "Seleccionar Tipo de Envío",
            list: this.pos.vape_shipping_types.map(s => ({ id: s.id, label: s.name, item: s })),
            getPayload: (selected) => {
                if (selected) {
                    const shippingId = selected.id || selected.item?.id || selected;
                    this.currentOrder.vs_shipping_type_id = shippingId;
                    
                    this.vapeState.renderTrigger++;
                }
            },
        });
    },
});