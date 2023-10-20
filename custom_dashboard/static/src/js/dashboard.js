odoo.define('custom_dashboard.Dashboard', function (require){
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');

var CustomDashBoard = AbstractAction.extend({
    template :"Dashboard_custom",

        start: function () {
            var self = this;
            return this._super().then(function () {
                self._loadProductRequestsCount();
            });
        },

        _loadProductRequestsCount: function () {
            var self = this;
            var $countElement = self.$('#product_requests_count');

            // Define a domain to filter product requests
            var domain = [['status', '=', 'requested']];

            // Make an RPC call to fetch the count of product requests
            this._rpc({
                model: 'product.request', // Replace with your actual model name
                method: 'search_count',
                domain: domain,
            }).then(function (count) {
                $countElement.text(count); // Update the HTML element with the count
            });
        },


            start: function () {
            var self = this;
            return this._super().then(function () {
                self._loadPurchaseRequests();
            });
        },

        _loadPurchaseRequests: function () {
            var self = this;
            var $list = self.$('#purchase_requests_list');
            $list.empty();

            // Define a domain to filter purchase requests
            var domain = [['status', '=', 'requested']];

            // Make an RPC call to fetch the purchase requests
            this._rpc({
                model: 'product.request', // Replace with your actual model name
                method: 'search_read',
                fields: ['name', 'status'], // Add fields you want to display
                domain: domain,
            }).then(function (requests) {
                if (requests.length === 0) {
                    $list.append('<li>No requested purchase requests found.</li>');
                } else {
                    requests.forEach(function (request) {
                        $list.append('<li>' + request.name + ' - ' + request.description + '</li>');
                    });
                }
            });
        },
    });





//});



core.action_registry.add('custom_dashboard_tag', CustomDashBoard);

return CustomDashBoard;
});