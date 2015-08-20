'use strict';

var appDirectives = angular.module('appDirectives', []);


appDirectives.directive('appSpinner',
    function appSpinner () {
        return {
            restrict: 'A',
            scope: {
                spinning: '=appSpinner'
            },
            templateUrl: 'partials/widgets/spinner.html'
        };
    });


appDirectives.directive('appPager',
    function appPager () {
        return {
            restrict: 'E',
            template: '<input type="text" class="select-page" ng-model="inputPage" ng-change="selectPage(inputPage)">',
            link: function (scope) {
                scope.$watch('currentPage', function (newValue) {
                    scope.inputPage = newValue;
                });
            }
        };
    });


appDirectives.directive('appDetailsModal',
    function appDetailsModal () {
        return {
            restrict: 'A',
            transclude: true,
            replace: true,
            scope: true,
            templateUrl: 'partials/widgets/details_modal.html'
        };
    });


appDirectives.directive('appDetailsModalNavbar',
    function appDetailsModalNavbar () {
        return {
            require: '^appDetailsModal',
            restrict: 'A',
            transclude: true,
            replace: true,
            scope: true,
            templateUrl: 'partials/widgets/details_modal_navbar.html'
        };
    });
