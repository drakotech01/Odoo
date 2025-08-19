odoo.define('spreadsheet_dashboard.spreadsheet_widget', function (require) {
    "use strict";

    const fieldRegistry = require('web.field_registry');
    const AbstractField = require('web.basic_fields').FieldText;

    const SpreadsheetWidget = AbstractField.extend({
        supportedFieldTypes: ['text'],
        template: 'spreadsheet_dashboard.SpreadsheetWidget',

        start: function () {
            this.$el.css({
                'background-color': '#1e1e2f',
                'color': '#dcdcdc',
                'font-family': 'monospace',
                'height': '300px',
                'padding': '10px'
            });
            return this._super.apply(this, arguments);
        },
    });

    fieldRegistry.add('spreadsheet_widget', SpreadsheetWidget);
});