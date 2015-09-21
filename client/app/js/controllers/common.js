'use strict';

var appControllers = angular.module('appControllers.common', []);


appControllers.controller('CommonController', ['$scope', '$timeout', '$aside', 'ConfigFactory', 'PageFactory', 'SessionFactory', 'CommonFactory',
    function CommonController ($scope, $timeout, $aside, ConfigFactory, PageFactory, SessionFactory, CommonFactory) {
        function initializeModalHandler() {
            var modals = [];

            function registerNewModal(event, $modal) {
                if (modals.indexOf($modal) === -1) {
                    modals.push($modal);
                }
            }

            function closeAllOpenedModals() {
                if (modals.length) {
                    angular.forEach(modals, function ($modal) {
                        $modal.$promise.then($modal.hide);
                    });
                }
            }

            $scope.$on('modal.show', registerNewModal);
            $scope.$on('$routeChangeSuccess', closeAllOpenedModals);
        }

        function initializeSidebarManager() {
            var sidebars = {};

            function openSidebar(type) {
                var sidebar = sidebars[type],
                    options = $scope.sidebars[type];

                if (angular.isUndefined(sidebar)) {
                    if (angular.isUndefined(options)) {
                        CommonFactory.printToConsole('Missing sidebar \'' + type + '\'');
                        return;
                    }
                    sidebar = $aside(options);
                    sidebars[type] = sidebar;
                }

                sidebar.$promise.then(function () {
                    if (!sidebar.$isShown) {
                        sidebar.show();
                    }
                    setFocus(sidebar);
                });
            }

            function setFocus(sidebar) {
                $timeout(function setFocusTimeout () {
                    var defaultElement = sidebar.$element.find('[autofocus]');
                    if (angular.isDefined(defaultElement)) {
                        defaultElement.focus();
                    }
                });
            }

            $scope.openSidebar = openSidebar;
        }

        ConfigFactory.getConfig().then(function (config) {
            $scope.appTitle = config.app_title;
        }, CommonFactory.showResponseError);

        initializeModalHandler();
        initializeSidebarManager();

        $scope.isAuthenticated = SessionFactory.isAuthenticated;
        $scope.getWindowTitle = PageFactory.getWindowTitle;
    }]);


appControllers.controller('MainMenuController', ['$scope', 'gettextCatalog', 'ConfigFactory', 'CommonFactory',
    function MainMenuController ($scope, gettextCatalog, ConfigFactory, CommonFactory) {
        function initializeLanguages() {
            var languages = [
                {
                    'language': 'en',
                    'title': 'English',
                    'flag': 'us'
                }, {
                    'language': 'hu',
                    'title': 'Magyar'
                }
            ];

            function getCurrentLanguage() {
                return gettextCatalog.currentLanguage;
            }

            function changeLanguage(lang) {
                gettextCatalog.setCurrentLanguage(lang);
            }

            $scope.languages = languages;
            $scope.getCurrentLanguage = getCurrentLanguage;
            $scope.changeLanguage = changeLanguage;
        }

        ConfigFactory.getConfig().then(function (config) {
            if (config.forced_language === null) {
                initializeLanguages();
            }
        }, CommonFactory.showResponseError);
    }]);


appControllers.controller('UserMenuController', ['$scope', '$location', 'SessionFactory', 'CommonFactory',
    function UserMenuController ($scope, $location, SessionFactory, CommonFactory) {
        function logout() {
            CommonFactory.handlePromise(
                SessionFactory.logout(),
                null,
                function () {
                    $location.path('/login');
                });
        }

        $scope.logout = logout;
    }]);

