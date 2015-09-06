'use strict';

var appDirectives = angular.module('appDirectives', []);


/**
 * @ngdoc directive
 * @name appSpinner
 * @restrict A
 *
 * @param {boolean} appSpinner spinning is on
 *
 * @description
 * Input box for go to page in a pager
 */
appDirectives.directive('appSpinner',
    function appSpinner () {
        return {
            restrict: 'A',
            scope: {
                appSpinner: '='
            },
            template: ' <i ng-if="appSpinner" class="fa fa-spinner fa-pulse"></i>'
        };
    });


/**
 * @ngdoc directive
 * @name appPageInput
 * @restrict E
 *
 * @description
 * Input box for go to page in a pager
 */
appDirectives.directive('appPageInput',
    function appPageInput () {
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


/**
 * @ngdoc directive
 * @name appDetailsModal
 * @restrict EA
 *
 * @description
 * Root object for AngularStrap style modals
 */
appDirectives.directive('appDetailsModal',
    function appDetailsModal () {
        return {
            restrict: 'EA',
            transclude: true,
            replace: true,
            scope: true,
            templateUrl: 'partials/widgets/details_modal.html'
        };
    });


/**
 * @ngdoc directive
 * @name appDetailsModal
 * @restrict EA
 *
 * @description
 * Common navbar object for modals
 */
appDirectives.directive('appDetailsModalNavbar',
    function appDetailsModalNavbar () {
        return {
            require: '^appDetailsModal',
            restrict: 'EA',
            transclude: true,
            replace: true,
            scope: true,
            templateUrl: 'partials/widgets/details_modal_navbar.html'
        };
    });
