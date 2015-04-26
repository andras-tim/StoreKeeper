'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', function ($scope, gettextCatalog, ConfigFactory, PageFactory) {
    $scope.changeLanguage = function (lang) {
        gettextCatalog.setCurrentLanguage(lang);
    };

    $scope.getWindowTitle = PageFactory.getWindowTitle;
    $scope.appTitle = ConfigFactory.getConfig().appTitle;
});


appControllers.controller('LoginController', function ($scope, $location, SessionFactory) {
    $scope.login = function () {
        $scope.$broadcast('show-errors-check-validity');
        if (!$scope.userForm.$valid) {
            return;
        }
        SessionFactory.login($scope.user.username, $scope.user.password).then(function () {
            $scope.userForm.$setPristine();
            $location.path('/main');
        });
    };

    $scope.user = { username: '', password: '' };
});


appControllers.controller('MainController', function ($scope, $location, SessionFactory) {
    $scope.logout = function () {
        SessionFactory.logout().then(function () {
            $location.path('/login');
        });
    };

    SessionFactory.getSession().then(function (session) {
        $scope.session = session;
    });
});
