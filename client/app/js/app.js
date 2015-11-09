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
    'appControllers.views',
    'appControllers.sidebars',
    'appDirectives.common',
    'appDirectives.fields',
    'appDirectives.form',
    'appDirectives.icons',
    'appDirectives.modal',
    'appDirectives.table',
    'appFactories.common',
    'appFactories.form',
    'appFactories.resources',
    'appFilters',
    'appServices'
]);


storekeeperApp.constant('appVersion', angular.element('meta[name=version]').attr('content'));


storekeeperApp.config(['$routeProvider',
    function appConfigRouting ($routeProvider) {
        var sessionRequired = {
            'getSession': ['$rootScope', '$q', '$location', 'SessionFactory',
                function getSession ($rootScope, $q, $location, SessionFactory) {
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
                'reloadOnSearch': false,
                'floatingsEnabled': true
            }).
            otherwise({
                'redirectTo': '/items'
            });
    }]);


storekeeperApp.run(['$rootScope',
    function appConfigSidebars ($rootScope) {
        $rootScope.sidebars = {
            'item': {
                'templateUrl': 'partials/sidebars/item.html',
                'placement': 'left'
            }
        };
        $rootScope.modals = {
            'item': {
                'templateUrl': 'partials/views/item.html',
                'dataFactory': 'item'
            },
            'item-selector': {
                'templateUrl': 'partials/views/item-selector.html',
                'saveState': false
            }
        };
    }]);


storekeeperApp.config(['RestangularProvider',
    function appConfigRestangular (RestangularProvider) {
        RestangularProvider.setBaseUrl('api');
    }]);


storekeeperApp.run(['$window', 'gettextCatalog', 'ConfigFactory', 'CommonFactory',
    function appConfigLanguage ($window, gettextCatalog, ConfigFactory, CommonFactory) {
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


storekeeperApp.run(['$rootScope', '$window', 'gettextCatalog', 'SidebarFactory', 'ModalFactory',
    function initDirtyWindowHandler ($rootScope, $window, gettextCatalog, SidebarFactory, ModalFactory) {
        function onWindowBeforeUnload() {
            var event = $rootScope.$broadcast('windowBeforeUnload');

            if (event.defaultPrevented) {
                return gettextCatalog.getString('The form is dirty.');
            }
        }

        $window.onbeforeunload = onWindowBeforeUnload;

        $rootScope.openSidebar = SidebarFactory.open;
        $rootScope.closeSidebar = SidebarFactory.close;
        $rootScope.openModal = ModalFactory.open;
        $rootScope.closeModal = ModalFactory.close;
    }]);


storekeeperApp.config(['$modalProvider', '$tooltipProvider', '$typeaheadProvider', '$asideProvider',
    function appConfigAngularstrap ($modalProvider, $tooltipProvider, $typeaheadProvider, $asideProvider) {
        angular.extend($modalProvider.defaults, {
            'html': true,
            'keyboard': false,
            'show': false
        });
        angular.extend($tooltipProvider.defaults, {
            'trigger': 'hover',
            'delay': {
                'show': 800,
                'hide': 100
            }
        });
        angular.extend($typeaheadProvider.defaults, {
            'minLength': 0,
            'autoSelect': true
        });
        angular.extend($asideProvider.defaults, {
            'show': false
        });
    }]);


storekeeperApp.config(['stConfig',
    function appConfigSmartTable (stConfig) {
        stConfig.pagination.template = 'partials/widgets/table_pager.html';
        stConfig.pagination.itemsByPage = 17;
    }]);


storekeeperApp.config(['$provide',
    function appConfigExceptionHandler ($provide) {
        $provide.decorator('$exceptionHandler', ['$delegate', '$injector',
            function exceptionHandlerWrapper ($delegate, $injector) {
                return function exceptionHandler (exception, cause) {
                    var $rootScope = $injector.get('$rootScope');
                    $rootScope.sendErrorToServer(exception, cause);
                    $delegate(exception, cause);
                };
            }]);

    }]);


storekeeperApp.run(['$rootScope', 'ErrorService',
    function appConfigureErrorForwarder ($rootScope, ErrorService) {
        $rootScope.sendErrorToServer = function sendErrorToServer (exception, cause) {
            ErrorService.post({
                'name': exception.name,
                'message': exception.message,
                'stack': exception.stack,
                'cause': cause
            });
        };
    }]);
