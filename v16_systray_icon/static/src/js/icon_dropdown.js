/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, useState } = owl;

class DropDownSystray extends Component {

	setup() {
        this.state = useState({ isOpen: false });
    }

    toggleDropDown() {
        this.state.isOpen = !this.state.isOpen;
    }

    closeDropDown() {
        this.state.isOpen = false;
    }

}

DropDownSystray.template = 'v16_systray_icon.DropDownExample';
registry.category("systray").add("v16_systray_icon.DropDownExample", {
    Component: DropDownSystray,}, { sequence: 111 }
);