/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { HomeMenu } from "@web_enterprise/webclient/home_menu/home_menu";

const { Component, useState, onWillStart } = owl;


export class ConectionPanel extends Component {

	setup() {
		
		this.orm = useService("orm");
		this.state = useState({'msg' : '', 'type': ''})
		
		onWillStart(async () => {
            await this.connectionMessage();
            await this.connectionAlertType();
        });
    }

    async connectionAlertType() {
    	
    	const data = await this.orm.call(
    	    "catalogue.configuration",
    	    'test_connection_search',
    	    [false]
    	)
    	if (data && data[0]){
	    	if (data[0].catalogue_server_status == 'error'){
	    		this.state.type = "block"
	    	}
	    	else{
	    		this.state.type = "none"
	    	}
	    }else{
	    	this.state.type = "none"
	    }
    }


    async connectionMessage(){
    	const data = await this.orm.call(
    	    "catalogue.configuration",
    	    'test_connection_search',
    	    [false]
    	)
    	if (data && data[0]){
	    	if (data[0].catalogue_server_status == 'error'){
	    		const { _t } = this.env;
	    		this.state.msg = _t("The Catalogue Server has an Error, please inform the administrator to look into the error.");
	    	}
	    }

    }

}

ConectionPanel.template = "amt_catalogue_synch.ConnectionPanel";
HomeMenu.template = "amt_catalogue_synch.ConnectionHomeMenu";
HomeMenu.components = { ConectionPanel }