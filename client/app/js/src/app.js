'use strict';

var storekeeperApp = angular.module('storekeeperApp', [
    'mgcrea.ngStrap',
    'ngSanitize',
    'ngRoute',
    //'ngAnimate',
    'restangular',
    'gettext',
    'smart-table',
    'appControllers',
    'appDirectives',
    'appFactories',
    'appFilters',
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
        var sessionRequired = {
            'getSession': ['$rootScope', '$q', '$location', 'SessionFactory',
                function ($rootScope, $q, $location, SessionFactory) {
                    var result = $q.defer();

                    SessionFactory.getSession().then(function (session) {
                        result.resolve();
                        $rootScope.session = session;

                    }, function () {
                        result.reject();
                        $location.path('/login');

                    });

                    return result.promise;
                }]
        };

        $routeProvider.
            when('/login', {
                templateUrl: 'partials/views/login.html',
                controller: 'LoginController'
            }).
            when('/items', {
                templateUrl: 'partials/views/items.html',
                controller: 'ItemsController',
                resolve: sessionRequired
            }).
            otherwise({
                redirectTo: '/items'
            });
    }]);


storekeeperApp.config(['RestangularProvider',
    function (RestangularProvider) {
        RestangularProvider.setBaseUrl('api');
    }]);


storekeeperApp.run(['gettextCatalog', 'ConfigFactory', 'CommonFactory',
    function (gettextCatalog, ConfigFactory, CommonFactory) {
        ConfigFactory.getConfig().then(function (config) {
            var language = config.forced_language;
            if (language === null) {
                language = window.navigator.userLanguage || window.navigator.language; // "en" or "en-US"
                language = language.split("-")[0];
            }
            gettextCatalog.baseLanguage = 'en';
            gettextCatalog.debug = config.debug;
            gettextCatalog.setCurrentLanguage(language);
        }, CommonFactory.showResponseError);
    }]);


storekeeperApp.config(['$tooltipProvider',
    function($tooltipProvider) {
        angular.extend($tooltipProvider.defaults, {
            delay: { show: 600, hide: 100 }
        });
    }]);


storekeeperApp.config(['stConfig',
    function(stConfig) {
        stConfig.pagination.template = 'partials/widgets/table_pager.html';
    }]);
