/** @odoo-module **/

import { OptionalProductsModal } from "@sale_product_configurator/js/product_configurator_modal";
import Dialog from 'web.Dialog';


OptionalProductsModal.include({

    events: _.extend({}, OptionalProductsModal.prototype.events, {
        'change .css_attribute_color input': 'onChangeParentColorAttribute',
        'change .o_variant_pills input': 'onChangeParentPillsAttribute',
        'change .js_attribute_value': 'onChangeAttributeVariant'
    }),

    init: function (parent, params) {
        this._super.apply(this, arguments);
    },

    _onChangeAttributeValue: function (ev, selector) {
        const $parent = $(ev.target).closest('.js_product');
        const $inputGroup = $parent.find(selector);
        $inputGroup.removeClass("active").filter(':has(input:checked)').addClass("active");

        const $checkedInput = $parent.find(`${selector} input[type="radio"]:checked`);
        const checkedDataValue = $checkedInput.data('value_name');

        const $optProducts = $parent.parent().find(`.js_product:not(.in_cart)[data-parent-unique-id='${$parent.data('uniqueId')}']`);

        $optProducts.each(function () {
            const $optProduct = $(this);
            const $radioInputs = $optProduct.find(`${selector} input[type="radio"]`);

            $radioInputs.each(function () {
                const $radio = $(this);
                if ($radio.data('value_name') === checkedDataValue) {
                    if (!$radio.prop('checked')) {
                        $radio.prop('checked', true).trigger('change');
                    }
                    $radio.closest(selector).addClass('active');
                } 
            });
        });
    },

    onChangeAttributeVariant: function (ev) {
        this._onChangeAttributeValue(ev, '.js_attribute_value');
    },

    onChangeParentColorAttribute: function (ev) {
        this._onChangeAttributeValue(ev, '.css_attribute_color');
    },

    onChangeParentPillsAttribute: function (ev) {
        this._onChangeAttributeValue(ev, '.o_variant_pills');
    },

});
