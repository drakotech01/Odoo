odoo.define('same_window_module_actions.module_actions', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var ModuleManager = require('base.module_manager');
    var _t = core._t;

    ModuleManager.include({
        _callCustomAction: function(action) {
            var self = this;
            return ajax.jsonRpc('/module/action/override', 'call', {
                action: action,
                module_id: this.handle
            }).then(function(result) {
                if (result.error) {
                    self.do_warn(_t("Error"), result.error);
                    return $.Deferred().reject();
                }
                
                self.do_notify(_t("Success"), _t("Operation completed successfully"));
                self._updateModuleList();
                self.update();
                
                return result;
            });
        },

        button_immediate_install: function() {
            return this._callCustomAction('install');
        },

        button_immediate_upgrade: function() {
            return this._callCustomAction('upgrade');
        },

        button_immediate_uninstall: function() {
            return this._callCustomAction('uninstall');
        }
    });
});