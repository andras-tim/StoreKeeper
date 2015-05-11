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
        $routeProvider.
            when('/login', {
                templateUrl: 'partials/login.html',
                controller: 'LoginController'
            }).
            when('/main', {
                templateUrl: 'partials/main.html',
                controller: 'MainController',
                resolve: sessionRequired
            }).
            otherwise({
                redirectTo: '/main'
            });
    }]);


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


storekeeperApp.config(['RestangularProvider',
    function (RestangularProvider) {
        RestangularProvider.setBaseUrl('api');
    }]);


storekeeperApp.run(['gettextCatalog', 'ConfigFactory', 'HelperFactory',
    function (gettextCatalog, ConfigFactory, HelperFactory) {
        ConfigFactory.getConfig().then(function (config) {
            var language = config.forced_language;
            if (language == null) {
                language = window.navigator.userLanguage || window.navigator.language; // "en" or "en-US"
                language = language.split("-")[0];
            }
            gettextCatalog.baseLanguage = 'en';
            gettextCatalog.debug = config.debug;
            gettextCatalog.setCurrentLanguage(language);
        }, HelperFactory.showResponseError);
    }]);


storekeeperApp.config(['$tooltipProvider',
    function($tooltipProvider) {
        angular.extend($tooltipProvider.defaults, {
            delay: { show: 600, hide: 100 }
        });
    }]);
