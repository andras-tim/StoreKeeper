'use strict';

var appLoginViewControllers = angular.module('appControllers.views.login', []);


appLoginViewControllers.controller('LoginController', ['$scope', '$location', 'SessionFactory', 'CommonFactory',
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

