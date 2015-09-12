'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', ['$scope', 'ConfigFactory', 'PageFactory', 'SessionFactory', 'CommonFactory',
    function CommonController ($scope, ConfigFactory, PageFactory, SessionFactory, CommonFactory) {
        $scope.isAuthenticated = SessionFactory.isAuthenticated;

        ConfigFactory.getConfig().then(function (config) {
            $scope.appTitle = config.app_title;
        }, CommonFactory.showResponseError);

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


appControllers.controller('LoginController', ['$scope', '$location', 'SessionFactory', 'CommonFactory',
    function LoginController ($scope, $location, SessionFactory, CommonFactory) {
        function login() {
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
        }

        $scope.user = {'username': '', 'password': '', 'remember': false};
        $scope.login = login;
    }]);


appControllers.controller('ItemsController', ['$scope', 'ItemService', 'CommonFactory',
    function ItemsController ($scope, ItemService, CommonFactory) {
        CommonFactory.handlePromise(
            ItemService.getList(),
            'loadingItems',
            function (items) {
                $scope.items = items;
            });
    }]);


appControllers.controller('ItemController', ['$scope', 'Restangular', 'VendorService', 'UnitService', 'CommonFactory',
    function ItemController ($scope, Restangular, VendorService, UnitService, CommonFactory) {
        function createVendor() {
            var completedNewVendor = {'name': $scope.item.vendor};

            CommonFactory.handlePromise(
                VendorService.post(Restangular.copy(completedNewVendor)),
                'creatingVendor',
                function (resp) {
                    $scope.vendors.push(resp);
                    $scope.item.vendor = resp;
                });
        }

        function createUnit() {
            var completedNewUnit = { 'unit': $scope.item.unit };

            CommonFactory.handlePromise(
                UnitService.post(Restangular.copy(completedNewUnit)),
                'creatingUnit',
                function (resp) {
                    $scope.units.push(resp);
                    $scope.item.unit = resp;
                });
        }

        function saveChanges() {
            CommonFactory.handlePromise(
                $scope.item.put(),
                'savingItem',
                function () {
                    angular.merge($scope.rowData, $scope.item);
                    $scope.$hide();
                }
            );
        }

        function downloadLabel(barcodeId) {
            window.location.href = 'api/items/' + $scope.item.id + '/barcodes/' + barcodeId + '/print';
            //console.log($scope.item.one('barcodes', barcodeId));
        }

        $scope.item = Restangular.copy($scope.rowData);

        CommonFactory.handlePromise(
            $scope.item.getList('barcodes'),
            'loadingBarcodes',
            function (barcodes) {
                $scope.barcodes = barcodes;
            });

        CommonFactory.handlePromise(
            VendorService.getList(),
            'loadingVendors',
            function (vendors) {
                $scope.vendors = vendors;
            });

        CommonFactory.handlePromise(
            UnitService.getList(),
            'loadingUnits',
            function (units) {
                $scope.units = units;
            });

        $scope.createVendor = createVendor;
        $scope.createUnit = createUnit;
        $scope.downloadLabel = downloadLabel;
        $scope.saveChanges = saveChanges;
    }]);
