/** @odoo-module **/

import { registry } from "@web/core/registry";

const { Component, useState, OnMounted, OnWillUnmount, useRef} = owl;

class DropDownSystray extends Component {

    setup() {
        this.dropdownRef = useRef('dropdownRef');
        console.log(this.dropdownRef.el)
        this.state = useState({ isOpen: false });
        this.OnMounted();
    }


    OnMounted() {
        document.addEventListener("click", this.onClickOutside);
    }

    OnWillUnmount() {
        document.removeEventListener("click", this.onClickOutside);
    }

    toggleDropDown() {
        this.state.isOpen = !this.state.isOpen;
    }

    onClickOutside(event) {
        console.log("@@@@@@@@@@@@", this.dropdownRef);
        // const dropdownElement = event.target;
        // const dropdown = this.dropdownRef.el;
        // if (dropdown && !dropdown.contains(dropdownElement)) {
        //     this.state.isOpen = false;
        // }
    }



}

DropDownSystray.template = 'v16_systray_icon.DropDownExample';
registry.category("systray").add("v16_systray_icon.DropDownExample", {
    Component: DropDownSystray,}, { sequence: 111 }
);