odoo.define('file_upload.amazon_dashboard', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var AmazonDashboard = AbstractAction.extend({
        template: "AmazonDashboard",
        events: {
            // Define any event handlers here
        },

        init: function (parent, context) {
            this._super.apply(this, arguments);
        },

        start: function () {
            // Initialize your dashboard here
            return this._super();
        },
    });

    core.action_registry.add('amazon_dashboard', AmazonDashboard);

    return AmazonDashboard;
});
