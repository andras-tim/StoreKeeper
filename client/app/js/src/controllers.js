'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', ['$scope', '$location', 'gettextCatalog', 'ConfigFactory', 'PageFactory', 'SessionFactory', 'CommonFactory',
    function ($scope, $location, gettextCatalog, ConfigFactory, PageFactory, SessionFactory, CommonFactory) {
        function initializeLanguages() {
            $scope.languages = [
                {
                    'language': 'en',
                    'title': 'English',
                    'flag': 'us'
                }, {
                    'language': 'hu',
                    'title': 'Magyar'
                }
            ];

            $scope.getCurrentLanguage = function () {
                return gettextCatalog.currentLanguage;
            };

            $scope.changeLanguage = function (lang) {
                gettextCatalog.setCurrentLanguage(lang);
            };
        }


        $scope.isAuthenticated = SessionFactory.isAuthenticated;


        ConfigFactory.getConfig().then(function (config) {
            $scope.appTitle = config.app_title;
            if (config.forced_language === null) {
                initializeLanguages();
            }
        }, CommonFactory.showResponseError);
        $scope.getWindowTitle = PageFactory.getWindowTitle;
    }]);


appControllers.controller('UserMenu', ['$scope', '$location', 'SessionFactory', 'CommonFactory',
    function ($scope, $location, SessionFactory, CommonFactory) {
        $scope.logout = function () {
            CommonFactory.handlePromise(
                SessionFactory.logout(),
                null,
                function () {
                    $location.path('/login');
                });
        };
    }]);


appControllers.controller('LoginController', ['$scope', '$location', 'SessionFactory', 'CommonFactory',
    function ($scope, $location, SessionFactory, CommonFactory) {
        $scope.login = function () {
            $scope.$broadcast('show-errors-check-validity');
            if (!$scope.userForm.$valid) {
                return;
            }

            CommonFactory.handlePromise(
                SessionFactory.login($scope.user.username, $scope.user.password, $scope.user.remember),
                'authenticating',
                function () {
                    $scope.userForm.$setPristine();
                    $location.path('/main');
                });
        };

        $scope.user = { username: '', password: '', remember: false };
    }]);


appControllers.controller('MainController', ['$scope', 'ItemService', 'CommonFactory',
    function ($scope, ItemService, CommonFactory) {
        CommonFactory.handlePromise(
            ItemService.getList(),
            null,
            function (items) {
                $scope.items = items;
            });
    }]);
