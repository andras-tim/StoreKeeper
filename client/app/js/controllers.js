'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', function ($scope, $location, gettextCatalog, ConfigFactory, PageFactory, SessionFactory, HelperFactory) {
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
        if (config.forced_language == null) {
            initializeLanguages();
        }
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
        SessionFactory.login($scope.user.username, $scope.user.password, $scope.user.remember).then(function () {
            $scope.userForm.$setPristine();
            $location.path('/main');
        }, HelperFactory.showResponseError);
    };

    $scope.user = { username: '', password: '', remember: false };
});


appControllers.controller('MainController', function ($scope, ItemService, HelperFactory) {
    ItemService.getList().then(function (items) {
        $scope.items = items;
    }, HelperFactory.showResponseError);
});
