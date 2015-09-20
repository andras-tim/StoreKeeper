'use strict';

var appFormDirectives = angular.module('appDirectives.form', []);


/**
 * @ngdoc directive
 * @name appInputValidator
 * @restrict E
 *
 * @param {object} aFormInput
 * @param {string} aRequired
 *
 * @description
 * Wrap input element with error handler
 */
appFormDirectives.directive('appInputValidator',
    function appInputValidator () {
        return {
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aFormInput': '=',
                'aRequired': '@'
            },
            'templateUrl': 'partials/widgets/form/input-validator.html'
        };
    });


/**
 * @ngdoc directive
 * @name appInputForm
 * @restrict E
 *
 * @param {string} aInputId
 * @param {string} aInputName
 * @param {string} aLabel
 * @param {string} aRequired
 * @param {string=} [aLabelClass=col-sm-4]
 * @param {string=} [aInputClass=col-sm-8]
 *
 * @description
 * Nested forms and labels for inputs
 */
appFormDirectives.directive('appInputForm',
    function appInputForm () {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aInputId': '@',
                'aInputName': '@',
                'aLabel': '@',
                'aRequired': '@',
                'aLabelClass': '@',
                'aInputClass': '@'
            },
            'templateUrl': 'partials/widgets/form/input-form.html',
            'compile': function (element, attrs) {
                if (!attrs.aLabelClass) {
                    attrs.aLabelClass = 'col-sm-4';
                }
                if (!attrs.aInputClass) {
                    attrs.aInputClass = 'col-sm-8';
                }
            }
        };
    });


/**
 * @ngdoc directive
 * @name appCheckboxLabel
 * @restrict E
 *
 * @param {string} aLabel
 *
 * @description
 * Label for input[@type="checkbox"] elements
 */
appFormDirectives.directive('appCheckboxLabel',
    function appCheckboxLabel () {
        return {
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aLabel': '@'
            },
            'templateUrl': 'partials/widgets/form/checkbox-label.html'
        };
    });


/**
 * @ngdoc directive
 * @name appTooltip
 * @restrict A
 *
 * @param {string} appTooltip
 *
 * @description
 * Tooltip for form elements
 */
appFormDirectives.directive('appTooltip', ['$tooltip',
    function appTooltip ($tooltip) {
        return {
            'restrict': 'A',
            'scope': false,
            'link': function (scope, element, attrs) {
                var tooltip;
                attrs.$observe('appTooltip', function (newValue) {
                    if (tooltip !== undefined) {
                        tooltip.destroy();
                    }
                    tooltip = $tooltip(element, {
                        'title': newValue
                    });
                });
            }
        };
    }]);


/**
 * @ngdoc directive
 * @name appFormTypeahead
 * @restrict E
 *
 * @param {string} aName
 * @param {object} aModel
 * @param {string} aDataSource
 * @param {string} aLabel
 * @param {string} aPlaceholder
 * @param {string} aRequired
 * @param {function} aCreateCallback
 * @param {object=} [aLoadingSpinner]
 * @param {object=} [aCreatingSpinner]
 * @param {string=} [aLabelClass=col-sm-4]
 * @param {string=} [aInputClass=col-sm-8]
 *
 * @description
 * Typeahead for forms
 */
appFormDirectives.directive('appFormTypeahead',
    function appFormTypeahead () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
                'aName': '@',
                'aModel': '=',
                'aDataSource': '@',
                'aLabel': '@',
                'aPlaceholder': '@',
                'aRequired': '@',
                'aCreateCallback': '&',
                'aLoadingSpinner': '=',
                'aCreatingSpinner': '=',
                'aLabelClass': '@',
                'aInputClass': '@'
            },
            'templateUrl': 'partials/widgets/form-typeahead.html',
            'compile': function (element, attrs) {
                if (!attrs.aLabelClass) {
                    attrs.aLabelClass = 'col-sm-4';
                }
                if (!attrs.aInputClass) {
                    attrs.aInputClass = 'col-sm-8';
                }
            },
            'controller': ['$scope',
                function ($scope) {
                    var isFilled = function isFilled (modelRef) {
                        return typeof modelRef === 'object';
                    };

                    $scope.isFilled = isFilled;
                }]
        };
    });


/**
 * @ngdoc directive
 * @name appIndentedFormGroup
 * @restrict E
 *
 * @param {string=} [aClass=col-sm-offset-4 col-sm-8]
 *
 * @description
 * For easy indent objects without left-side label
 */
appFormDirectives.directive('appIndentedFormGroup',
    function appIndentedFormGroup () {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'scope': {
                'aClass': '@'
            },
            'template': '<div class="form-group"><div class="{{ aClass }}" ng-transclude></div></div>',
            'compile': function (element, attrs) {
                if (!attrs.aClass) {
                    attrs.aClass = 'col-sm-offset-4 col-sm-8';
                }
            }
        };
    });
