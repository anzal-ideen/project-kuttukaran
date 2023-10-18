//odoo.define('custom_dashboard.dashboard_action', function (require){
//"use strict";
//    var AbstractAction = require('web.AbstractAction');
//    var core = require('web.core');
//
//    var PosDashboard = AbstractAction.extend({
//    template :"Dashboard",
//    });
//
////    var QWeb = core.qweb;
////    var rpc = require('web.rpc');
////    var ajax = require('web.ajax');
////    var CustomDashBoard = AbstractAction.extend({
////       template: 'CustomDashBoard',
//
//    })
//    core.action_registry.add('custom_dashboard_tags', CustomDashBoard);
//    return PosDashboard;
//    })

import { registry } from "@web/core/registry"
const { Component } = owl

export class OwlSalesDashboard extend Component {}

OwlSalesDashboard.template = "owl.OwlSalesDashboard"

registry.category("actions").add("owl.sales_dashboard",OwlSalesDashboard)