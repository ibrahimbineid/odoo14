odoo.define('hasanin_right_access.hide_delete', function(require) {
    "use strict";


    var KanbanView = require("web.KanbanView");


    var KanbanController = require("web.KanbanController");
    var ListController = require("web.ListController");
    var FormController = require("web.FormController");
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;

    var includeDict = {
        _getActionMenuItems: function (state) {
        	var result = this._super.apply(this, arguments);
        	if(result && result.items && result.items.other && result.items.other.length && !session.is_show_delete_button){
        		result.items.other.splice(_.findIndex(result.items.other, { description: "Delete" }), 1);
        	}
        	return result
		},
    };

//    KanbanController.include(includeDict);
    ListController.include(includeDict);
    
    FormController.include({
    	_getActionMenuItems: function (state) {
        	var result = this._super.apply(this, arguments);
        	if(result && result.items && result.items.other && result.items.other.length && !session.is_show_delete_button){
        		result.items.other.splice(_.findIndex(result.items.other, { description: "Delete" }), 1);
        	}
        	return result
		},
    });

    KanbanView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            var self = this;
            session.user_has_group('hasanin_right_access.group_display_delete_action').then(function(has_group) {
                console.log(has_group);
                self.rendererParams.record_options.deletable = self.rendererParams.record_options.deletable && has_group;
            });
        }
    });

});
