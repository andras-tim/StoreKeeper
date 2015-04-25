'use strict';

/* App Module */

var storekeeperApp = angular.module('storekeeperApp', [
    'mgcrea.ngStrap',
    'ngSanitize',
    'ngRoute',
    'ngAnimate',
    'restangular',
    'gettext',
    'appControllers',
    'appServices'
]);

storekeeperApp.config(['$modalProvider',
    function ($modalProvider) {
        angular.extend($modalProvider.defaults, {
            html: true
        });
    }]);


storekeeperApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/login', {
                templateUrl: 'partials/login.html',
                controller: 'LoginCtrl'
            }).
            when('/main', {
                templateUrl: 'partials/main.html',
                controller: 'MainCtrl'
            }).
            otherwise({
                redirectTo: '/login'
            });
    }]);


storekeeperApp.config(['RestangularProvider',
    function (RestangularProvider) {
        RestangularProvider.setBaseUrl('api');
    }]);


storekeeperApp.run(function (gettextCatalog) {
    var language = window.navigator.userLanguage || window.navigator.language; // "en" or "en-US"
    gettextCatalog.currentLanguage = language.split("-")[0];
    gettextCatalog.debug = true;
});
