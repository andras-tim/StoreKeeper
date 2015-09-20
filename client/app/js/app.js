'use strict';

var storekeeperApp = angular.module('storekeeperApp', [
    'mgcrea.ngStrap',
    'ngSanitize',
    'ngRoute',
    //'ngAnimate',
    'restangular',
    'gettext',
    'smart-table',
    'appControllers.common',
    'appControllers.views.login',
    'appControllers.views.items',
    'appControllers.sidebar.item',
    'appDirectives.common',
    'appDirectives.fields',
    'appDirectives.form',
    'appDirectives.icons',
    'appDirectives.modal',
    'appDirectives.table',
    'appFactories',
    'appFilters',
    'appServices'
]);


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
                'templateUrl': 'partials/views/login.html',
                'controller': 'LoginController'
            }).
            when('/items', {
                'templateUrl': 'partials/views/items.html',
                'controller': 'ItemsController',
                'resolve': sessionRequired,
                'reloadOnSearch': false
            }).
            otherwise({
                'redirectTo': '/items'
            });
    }]);


storekeeperApp.run(['$rootScope',
    function ($rootScope) {
        $rootScope.sidebars = {
            'item': {
                'templateUrl': 'partials/sidebars/item.html',
                'placement': 'left'
            }
        };
    }]);


storekeeperApp.config(['RestangularProvider',
    function (RestangularProvider) {
        RestangularProvider.setBaseUrl('api');
    }]);


storekeeperApp.run(['$window', 'gettextCatalog', 'ConfigFactory', 'CommonFactory',
    function ($window, gettextCatalog, ConfigFactory, CommonFactory) {
        ConfigFactory.getConfig().then(function (config) {
            var language = config.forced_language;
            if (language === null) {
                language = $window.navigator.userLanguage || $window.navigator.language; // "en" or "en-US"
                language = language.split('-')[0];
            }
            gettextCatalog.baseLanguage = 'en';
            gettextCatalog.debug = config.debug;
            gettextCatalog.setCurrentLanguage(language);
        }, CommonFactory.showResponseError);
    }]);


storekeeperApp.run(['$rootScope', '$window', 'gettextCatalog',
    function ($rootScope, $window, gettextCatalog) {
        function onWindowBeforeUnload() {
            var event = $rootScope.$broadcast('windowBeforeUnload');

            if (event.defaultPrevented) {
                return gettextCatalog.getString('The form is dirty.');
            }
        }

        $window.onbeforeunload = onWindowBeforeUnload;
    }]);


storekeeperApp.config(['$modalProvider', '$tooltipProvider', '$typeaheadProvider',
    function ($modalProvider, $tooltipProvider, $typeaheadProvider) {
        angular.extend($modalProvider.defaults, {
            'html': true,
            'keyboard': false
        });
        angular.extend($tooltipProvider.defaults, {
            'trigger': 'hover',
            'delay': {
                'show': 600,
                'hide': 100
            }
        });
        angular.extend($typeaheadProvider.defaults, {
            'minLength': 0,
            'autoSelect': true
        });
    }]);


storekeeperApp.config(['stConfig',
    function (stConfig) {
        stConfig.pagination.template = 'partials/widgets/table_pager.html';
        stConfig.pagination.itemsByPage = 20;
    }]);


storekeeperApp.config(['$provide',
    function ($provide) {

        $provide.decorator('$exceptionHandler', ['$delegate', '$injector',
            function ($delegate, $injector) {
                return function (exception, cause) {
                    var $rootScope = $injector.get('$rootScope');
                    $rootScope.sendErrorToServer(exception, cause);
                    $delegate(exception, cause);
                };
            }]);

    }]);


storekeeperApp.run(['$rootScope', 'ErrorService',
    function ($rootScope, ErrorService) {
        $rootScope.sendErrorToServer = function sendErrorToServer (exception, cause) {
            ErrorService.post({
                'name': exception.name,
                'message': exception.message,
                'stack': exception.stack,
                'cause': cause
            });
        };
    }]);
