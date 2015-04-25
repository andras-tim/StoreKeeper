'use strict';

var appControllers = angular.module('appControllers', []);


appControllers.controller('CommonController', function ($scope, Restangular, $alert, gettextCatalog, ConfigFactory) {
    Restangular.setErrorInterceptor(function (resp) {
        console.debug(resp);
        $alert({
            title: gettextCatalog.getString("Error {{status}}", {status: resp.status}),
            content: resp.statusText + "<br />" + resp.data,
            container: "body",
            placement: "top-right",
            type: "danger",
            duration: 10,
            show: true
        });
    });

    $scope.changeLanguage = function (lang) {
        gettextCatalog.setCurrentLanguage(lang);
    };

    $scope.appTitle = ConfigFactory.getConfig().appTitle;
});


appControllers.controller('LoginController', function ($scope, $location, SessionService) {
    $scope.login = function () {
        $scope.$broadcast('show-errors-check-validity');
        if ($scope.userForm.$valid) {
            SessionService.post({username: $scope.user.username, password: $scope.user.password}).then(function (resp) {
                console.debug("OK");
                console.debug(resp);
                $scope.reset();
                $location.path('/main');
            }, function (resp) {
                console.debug(resp.status + " " + resp.statusText + ": " + JSON.stringify(resp.data));
            });
        }
    };

    $scope.reset = function () {
        $scope.$broadcast('show-errors-reset');
        $scope.user = {username: '', password: ''}
    };

    $scope.reset();
});


appControllers.controller('MainController', function ($scope, $location, Restangular, SessionService) {
    $scope.loginTest = function () {
        SessionService.one().get().then(function (resp) {
            console.debug(resp);
        });
    };

    $scope.logout = function () {
        SessionService.one().remove().then(function (resp) {
            console.debug(resp);
            $location.path('/login');
        });
    };

    $scope.session = '';
    SessionService.one().get().then(function (resp) {
        $scope.session = Restangular.stripRestangular(resp);
    });
});
