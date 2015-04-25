'use strict';

var appFactories = angular.module('appFactories', []);


appFactories.factory('ConfigFactory', function (ConfigService) {
    var config = {
        appName: undefined,
        appTitle: 'StoreKeeper'
    };

    ConfigService.one().get().then(function (resp) {
        config.appName = resp.app_name;
        config.appTitle = resp.app_title;
    });

    return {
        getConfig: function () {
            return config;
        }
    }
});
