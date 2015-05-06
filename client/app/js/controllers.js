'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', function ($scope, $location, gettextCatalog, ConfigFactory, PageFactory, SessionFactory, HelperFactory) {
    $scope.currentLanguage = gettextCatalog.currentLanguage;

    $scope.languages = [
        {
            "text": "EN",
            "click": "changeLanguage('en')"
        }, {
            "text": "HU",
            "click": "changeLanguage('hu')"
        }
    ];

    $scope.changeLanguage = function (lang) {
        gettextCatalog.setCurrentLanguage(lang);
        $scope.currentLanguage = lang;
    };


    $scope.isAuthenticated = SessionFactory.isAuthenticated;



    ConfigFactory.getConfig().then(function (config) {
        $scope.appTitle = config.app_title;
    }, HelperFactory.showResponseError);
    $scope.getWindowTitle = PageFactory.getWindowTitle;
});


appControllers.controller('UserMenu', function ($scope, $location, SessionFactory, HelperFactory) {
    $scope.logout = function () {
        SessionFactory.logout().then(function () {
            $location.path('/login');
        }, HelperFactory.showResponseError);
    };
});


appControllers.controller('LoginController', function ($scope, $location, SessionFactory, HelperFactory) {
    $scope.login = function () {
        $scope.$broadcast('show-errors-check-validity');
        if (!$scope.userForm.$valid) {
            return;
        }
        SessionFactory.login($scope.user.username, $scope.user.password).then(function () {
            $scope.userForm.$setPristine();
            $location.path('/main');
        }, HelperFactory.showResponseError);
    };

    $scope.user = { username: '', password: '' };
});


appControllers.controller('MainController', function ($scope, ItemService, HelperFactory) {
    ItemService.getList().then(function (items) {
        $scope.items = items;
    }, HelperFactory.showResponseError);
});
