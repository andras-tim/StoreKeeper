'use strict';

var storekeeperApp = angular.module('storekeeperApp', [
    'mgcrea.ngStrap',
    'ngSanitize',
    'ngRoute',
    'ngAnimate',
    'restangular',
    'gettext',
    'appControllers',
    'appFactories',
    'appFilters',
    'appServices'
]);


storekeeperApp.config(function ($modalProvider) {
    angular.extend($modalProvider.defaults, {
        html: true
    });
});


storekeeperApp.config(function ($routeProvider) {
    $routeProvider.
        when('/login', {
            templateUrl: 'partials/login.html',
            controller: 'LoginController'
        }).
        when('/main', {
            templateUrl: 'partials/main.html',
            controller: 'MainController'
        }).
        otherwise({
            redirectTo: '/login'
        });
});


storekeeperApp.config(function (RestangularProvider) {
    RestangularProvider.setBaseUrl('api');
});


storekeeperApp.run(function (gettextCatalog) {
    var language = window.navigator.userLanguage || window.navigator.language; // "en" or "en-US"
    gettextCatalog.currentLanguage = language.split("-")[0];
    gettextCatalog.debug = true;
});