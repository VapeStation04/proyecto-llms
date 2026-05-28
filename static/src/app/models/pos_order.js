/** @odoo-module **/
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        this.vs_channel_id = this.vs_channel_id || null;
        this.vs_shipping_type_id = this.vs_shipping_type_id || null;
    },

    get vape_channel() {
        if (!this.vs_channel_id) return null;
        
        const store = this.store || this.pos || this.env?.services?.pos;
        
        if (!store || !store.vape_channels) return null;
        
        return store.vape_channels.find(c => c.id === this.vs_channel_id) || null;
    },

    get vape_shipping_type() {
        if (!this.vs_shipping_type_id) return null;
        
        const store = this.store || this.pos || this.env?.services?.pos;
        
        if (!store || !store.vape_shipping_types) return null;
        
        return store.vape_shipping_types.find(s => s.id === this.vs_shipping_type_id) || null;
    },

    serialize() {
        const json = super.serialize(...arguments);
        
        if (this.vs_channel_id) {
            json.vs_channel_id = this.vs_channel_id;
        }
        if (this.vs_shipping_type_id) {
            json.vs_shipping_type_id = this.vs_shipping_type_id;
        }
        
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if (json.vs_channel_id) {
            this.vs_channel_id = json.vs_channel_id;
        }
        if (json.vs_shipping_type_id) {
            this.vs_shipping_type_id = json.vs_shipping_type_id;
        }
    }
});

patch(PosOrderline.prototype, {
    setup() {
        super.setup(...arguments);
        
        if (this.refunded_orderline_id && this.order_id) {
            const originalOrder = this.refunded_orderline_id.order_id;
            
            if (originalOrder) {
                if (originalOrder.vs_channel_id && !this.order_id.vs_channel_id) {
                    this.order_id.vs_channel_id = originalOrder.vs_channel_id;
                }
                
                if (originalOrder.vs_shipping_type_id && !this.order_id.vs_shipping_type_id) {
                    this.order_id.vs_shipping_type_id = originalOrder.vs_shipping_type_id;
                }
            }
        }
    }
});