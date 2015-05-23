'use strict';

var appDirectives = angular.module('appDirectives', []);


appDirectives.directive('appSpinner', function() {
    return {
        restrict: 'AE',
        scope: {
            spinning: '=appSpinner'
        },
        templateUrl: 'partials/widgets/spinner.html'
    };
});


appDirectives.directive('appPager', function() {
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
