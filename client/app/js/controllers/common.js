'use strict';

var appControllers = angular.module('appControllers.common', []);


appControllers.controller('CommonController', ['$scope', 'ConfigFactory', 'PageFactory', 'SessionFactory', 'CommonFactory',
    function CommonController ($scope, ConfigFactory, PageFactory, SessionFactory, CommonFactory) {
        function initializeShortcutHandler() {
            var shortcuts = {
                '19': function breakPause () {
                    $scope.openSidebar('item');
                }
            };

            function onKeyDown($event) {
                var handler = shortcuts[$event.which];
                if (angular.isUndefined(handler)) {
                    return;
                }
                handler();
            }

            return {
                'onKeyDown': onKeyDown
            };
        }

        var shortcutHandler = initializeShortcutHandler();

        ConfigFactory.getConfig().then(function (config) {
            $scope.appTitle = config.app_title;
        }, CommonFactory.showResponseError);

        $scope.onKeyDown = shortcutHandler.onKeyDown;

        $scope.isAuthenticated = SessionFactory.isAuthenticated;
        $scope.getWindowTitle = PageFactory.getWindowTitle;
    }]);


appControllers.controller('MainMenuController', ['$rootScope', '$scope', '$aside', 'gettextCatalog', 'ConfigFactory', 'CommonFactory',
    function MainMenuController ($rootScope, $scope, $aside, gettextCatalog, ConfigFactory, CommonFactory) {
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
