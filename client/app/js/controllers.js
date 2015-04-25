'use strict';

/* Controllers */

var appControllers = angular.module('appControllers', []);

appControllers.controller('CommonCtrl', function ($scope, Restangular, $alert, gettextCatalog) {
    Restangular.setErrorInterceptor(function (resp) {
        console.debug(resp);
        $alert({
            title: "Error " + resp.status,
            content: resp.statusText + "<br />" + resp.data,
            container: "body",
            placement: "top-right",
            type: "danger",
            duration: 10,
            show: true
        });
    });


    $scope.changeLanguage = function (lang) {
        gettextCatalog.currentLanguage = lang;
    };
});

appControllers.controller('LoginCtrl', function ($scope, $location, Restangular, Session) {
    //$scope.is_authenticated = false;

    $scope.login = function () {
        $scope.$broadcast('show-errors-check-validity');
        if ($scope.userForm.$valid) {
            Session.post({username: $scope.user.username, password: $scope.user.password}).then(function (resp) {
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

appControllers.controller('MainCtrl', function ($scope, $location, Session) {
    $scope.session = Session.one().get().$object;

    $scope.loginTest = function () {
        Session.one().get().then(function (resp) {
            console.debug(resp);
        });
    };

    $scope.logout = function () {
        Session.one().remove().then(function (resp) {
            console.debug(resp);
            $location.path('/login');
        });
    };
});
