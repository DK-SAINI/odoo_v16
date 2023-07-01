/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";

class ProductBarcode extends Component {
    setup() {
        this.state = useState({ barcodeValue: this.props.value || '', barcodeImageUrl: '' });


        onMounted(() => {
            if (this.props.value){
                this.generateBarcode();
            }
            
        });

        // onWillUnmount(() => {
        //     if (this.props.value){
        //         this.generateBarcode();
        //     }
        // });

    }

    async barcodeOnChange(event) {
        const barcodeValue = event.target.value;
        if (barcodeValue){
            this.state.barcodeValue = barcodeValue;
            await this.generateBarcode();
        }
    }

    async generateBarcode() {
        const barcodeValue = this.state.barcodeValue;
        if (barcodeValue){
            const barcodeImageUrl = await this.generateBarcodeImage(barcodeValue);
            this.state.barcodeImageUrl = barcodeImageUrl;
        }
    }

    async generateBarcodeImage(barcodeValue) {
        // Example using JsBarcode
        const canvas = document.createElement('canvas');
        JsBarcode(canvas, barcodeValue, { 
            format: 'CODE128',  
            // displayValue: true 
        });
        return canvas.toDataURL('image/png');
    }
}


ProductBarcode.template = "owl.ProductBarcode";
ProductBarcode.props = {
    ...standardFieldProps,
};

ProductBarcode.supportedTypes = ["char"];

registry.category("fields").add("barcode", ProductBarcode);