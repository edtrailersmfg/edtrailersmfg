odoo.define("pwa_ultimate.backend_pwa", function(require) {
    'use strict';
    var utils = require('web.utils');
    var session = require('web.session');

    $(document).ready(function (require) {

        if ("serviceWorker" in navigator) {
            navigator.serviceWorker.register("/service-worker.js").then(function () {
                console.log("Service Worker Registered");
            });
        }
    });
});
