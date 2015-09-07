'use strict';

var appDirectives = angular.module('appDirectives', []);


/**
 * @ngdoc directive
 * @name appSpinner
 * @restrict EA
 *
 * @description
 * Append a spinner
 */
appDirectives.directive('appSpinner',
    function appSpinner () {
        return {
            restrict: 'EA',
            template: ' <i class="fa fa-spinner fa-pulse"></i> '
        };
    });


/**
 * @ngdoc directive
 * @name appInput
 * @restrict E
 *
 * @param {string} appName
 * @param {object} appModel
 * @param {string} [appType=text]
 * @param {expression} appLabel
 * @param {expression} appPlaceholder
 * @param {expression} appRequired
 * @param {string} [appAutocomplete]
 * @param {string} [appLabelClass=col-sm-4]
 * @param {string} [appInputClass=col-sm-8]
 *
 * @description
 * Input text with formatting extras + error handling
 */
appDirectives.directive('appInput',
    function appInput () {
        return {
            require: '^form',
            restrict: 'E',
            scope: {
                'appName': '@',
                'appModel': '=',
                'appType': '@',
                'appLabel': '=',
                'appPlaceholder': '=',
                'appRequired': '=',
                'appAutocomplete': '@',
                'appLabelClass': '@',
                'appInputClass': '@'
            },
            templateUrl: 'partials/widgets/input.html',
            compile: function (element, attrs) {
                if (!attrs.appType) {
                    attrs.appType = 'text';
                }
                if (!attrs.appAutocomplete) {
                    attrs.appAutocomplete = attrs.appType === 'text' ? 'on' : 'off';
                }
                if (!attrs.appLabelClass) {
                    attrs.appLabelClass = 'col-sm-4';
                }
                if (!attrs.appInputClass) {
                    attrs.appInputClass = 'col-sm-8';
                }
            }
        };
    });


/**
 * @ngdoc directive
 * @name appCheckbox
 * @restrict E
 *
 * @param {string} appName
 * @param {object} appModel
 * @param {expression} appLabel
 * @param {expression} appTooltip
 *
 * @description
 * Checkbox with label and tooltip
 */
appDirectives.directive('appCheckbox',
    function appCheckbox () {
        return {
            require: '^form',
            restrict: 'E',
            scope: {
                'appName': '@',
                'appModel': '=',
                'appLabel': '=',
                'appTooltip': '='
            },
            templateUrl: 'partials/widgets/checkbox.html'
        };
    });


/**
 * @ngdoc directive
 * @name appIndentedFormGroup
 * @restrict E
 *
 * @param {string} [appClass=col-sm-offset-4 col-sm-8]
 *
 * @description
 * For easy indent objects without left-side label
 */
appDirectives.directive('appIndentedFormGroup',
    function appIndentedFormGroup () {
        return {
            require: '^form',
            restrict: 'E',
            transclude: true,
            scope: {
                'appClass': '@'
            },
            template: '<div class="form-group"><div class="{{ appClass }}" ng-transclude></div></div>',
            compile: function (element, attrs) {
                if (!attrs.appClass) {
                    attrs.appClass = 'col-sm-offset-4 col-sm-8';
                }
            }
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
 * @name appDetailsRow
 * @element tr
 * @restrict A
 * @priority 5000
 *
 * @param {object} appDetailsRow data object for row
 * @param {string} dataTemplateUrl template for modal
 *
 * @description
 * Editable row object
 */
appDirectives.directive('appDetailsRow',
    function appDetailsRow () {
        return {
            require: 'tr',
            restrict: 'A',
            priority: 5000,
            compile: function (element, attrs) {
                if (!attrs.appDetailsRow || !attrs.templateUrl) {
                    return;
                }
                attrs.$set('bsModal', '{\'rowData\': ' + attrs.appDetailsRow + '}');
                attrs.$addClass('clickable');
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
