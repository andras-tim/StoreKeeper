'use strict';

var appDirectives = angular.module('appDirectives', []);


appDirectives.directive('spinner', function() {
    return {
        restrict: 'AE',
        scope: {
            spinning: '=spinner'
        },
        templateUrl: 'partials/widgets/spinner.html'
    };
});


appDirectives.directive('pageSelector', function() {
    return {
        restrict: 'E',
        template: '<input type="text" class="select-page" ng-model="inputPage" ng-change="selectPage(inputPage)">',
        link: function (scope, element, attrs) {
            scope.$watch('currentPage', function (c) {
                scope.inputPage = c;
            });
        }
    };
});
