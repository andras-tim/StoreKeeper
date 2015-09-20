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
 * @name appLabel
 * @restrict E
 *
 * @param {string} aObjectId
 * @param {string} aLabel
 * @param {string=} [aLabelClass=col-sm-4]
 * @param {string=} [aObjectClass=col-sm-8]
 *
 * @description
 * Make label for anything
 */
appFormDirectives.directive('appLabel',
    function appLabel () {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'scope': {
                'aObjectId': '@',
                'aLabel': '@',
                'aLabelClass': '@',
                'aObjectClass': '@'
            },
            'templateUrl': 'partials/widgets/label.html',
            'compile': function (element, attrs) {
                if (!attrs.aLabelClass) {
                    attrs.aLabelClass = 'col-sm-4';
                }
                if (!attrs.aObjectClass) {
                    attrs.aObjectClass = 'col-sm-8';
                }
            }
        };
    });


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
 * @name appFormCheckbox
 * @restrict E
 *
 * @param {string} aName
 * @param {object} aModel
 * @param {string} aLabel
 * @param {string} aTooltip
 *
 * @description
 * Checkbox with label and tooltip
 */
appFormDirectives.directive('appFormCheckbox',
    function appFormCheckbox () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
                'aName': '@',
                'aModel': '=',
                'aLabel': '@',
                'aTooltip': '@'
            },
            'templateUrl': 'partials/widgets/form-checkbox.html'
        };
    });


/**
 * @ngdoc directive
 * @name appCheckbox
 * @restrict E
 *
 * @param {string} aName
 * @param {object} aModel
 * @param {string} aLabel
 * @param {string} aTooltip
 *
 * @description
 * Checkbox with label and tooltip
 */
appFormDirectives.directive('appCheckbox',
    function appCheckbox () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
                'aName': '@',
                'aModel': '=',
                'aLabel': '@',
                'aTooltip': '@'
            },
            'templateUrl': 'partials/widgets/checkbox.html'
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
