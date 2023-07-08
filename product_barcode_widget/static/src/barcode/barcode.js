/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";

class ProductBarcode extends Component {
    setup() {
        this.state = useState({
            barcodeValue: this.props.value || '',
            barcodeImageUrl: '',
        });
        this.fieldRef = useRef('barcodeField');
        this.onMounted();
        // this.onWillUnmount();
    }

    onMounted() {
        this.generateBarcode();
    }

    // onWillUnmount() {
    //     const barcodeField = this.fieldRef.el;
    //     if (barcodeField) {
    //         barcodeField.removeEventListener('input', this.barcodeOnChange.bind(this));
    //     }
    // }

    async barcodeOnChange(event) {
        const barcodeValue = event.target.value;
        this.state.barcodeValue = barcodeValue;
        await this.generateBarcode();
    }

    async generateBarcode() {
        const barcodeValue = this.state.barcodeValue;
        if (barcodeValue) {
            const barcodeImageUrl = await this.generateBarcodeImage(barcodeValue);
            this.state.barcodeImageUrl = barcodeImageUrl;
        } else {
            this.state.barcodeImageUrl = '';
        }
    }

    async generateBarcodeImage(barcodeValue) {
        const canvas = document.createElement('canvas');
        JsBarcode(canvas, barcodeValue, {
            format: 'CODE128',
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