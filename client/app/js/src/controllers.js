'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', ['$scope', 'gettextCatalog', 'ConfigFactory', 'PageFactory',
                                               'SessionFactory', 'CommonFactory',
    function ($scope, gettextCatalog, ConfigFactory, PageFactory, SessionFactory, CommonFactory) {
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
                    $location.path('/');
                });
        };

        $scope.user = { username: '', password: '', remember: false };
    }]);


appControllers.controller('ItemsController', ['$scope', 'ItemService', 'CommonFactory',
    function ($scope, ItemService, CommonFactory) {
        CommonFactory.handlePromise(
            ItemService.getList(),
            null,
            function (items) {
                $scope.items = items;
            });
    }]);


appControllers.controller('ItemController', ['$scope', 'Restangular', 'VendorService', 'UnitService', 'CommonFactory',
    function ($scope, Restangular, VendorService, UnitService, CommonFactory) {
        CommonFactory.handlePromise(
            VendorService.getList(),
            null,
            function (vendors) {
                $scope.vendors = vendors;
            });

        CommonFactory.handlePromise(
            UnitService.getList(),
            null,
            function (units) {
                $scope.units = units;
            });

        $scope.isFilled = function (modelRef) {
            return typeof modelRef === 'object';
        };

        $scope.createVendor = function () {
            var completedNewVendor = {'name': $scope.vendor};
            CommonFactory.handlePromise(
                VendorService.post(Restangular.copy(completedNewVendor)),
                'creatingVendor',
                function (resp) {
                    $scope.vendors.push(resp);
                    $scope.vendor = resp;
                });
        };

        $scope.createUnit = function () {
            var completedNewUnit = { 'unit': $scope.unit };

            CommonFactory.handlePromise(
                UnitService.post(Restangular.copy(completedNewUnit)),
                'creatingUnit',
                function(resp) {
                    $scope.units.push(resp);
                    $scope.unit = resp;
                });
        };

    }]);
