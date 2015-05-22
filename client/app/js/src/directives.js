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
