'use strict';

var appFormDirectives = angular.module('appDirectives.form', []);


/**
 * @ngdoc directive
 * @name appLabel
 * @restrict E
 *
 * @param {string} aObjectId
 * @param {expression} aLabel
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
                'aLabel': '=',
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
 * @name appFormInput
 * @restrict E
 *
 * @param {string} aName
 * @param {object} aModel
 * @param {string=} [aType=text]
 * @param {expression} aLabel
 * @param {expression} aPlaceholder
 * @param {expression} aRequired
 * @param {string=} [aAutocomplete]
 * @param {string=} [aLabelClass=col-sm-4]
 * @param {string=} [aInputClass=col-sm-8]
 *
 * @description
 * Input text for forms
 */
appFormDirectives.directive('appFormInput',
    function appFormInput () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
                'aName': '@',
                'aModel': '=',
                'aType': '@',
                'aLabel': '=',
                'aPlaceholder': '=',
                'aRequired': '=',
                'aAutocomplete': '@',
                'aLabelClass': '@',
                'aInputClass': '@'
            },
            'templateUrl': 'partials/widgets/form-input.html',
            'compile': function (element, attrs) {
                if (!attrs.aType) {
                    attrs.aType = 'text';
                }
                if (!attrs.aAutocomplete) {
                    attrs.aAutocomplete = attrs.aType === 'password' ? 'off' : 'on';
                }
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
 * @name appFormTypeahead
 * @restrict E
 *
 * @param {string} aName
 * @param {object} aModel
 * @param {string} aDataSource
 * @param {expression} aLabel
 * @param {expression} aPlaceholder
 * @param {expression} aRequired
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
                'aLabel': '=',
                'aPlaceholder': '=',
                'aRequired': '=',
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
 * @param {expression} aLabel
 * @param {expression} aTooltip
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
                'aLabel': '=',
                'aTooltip': '='
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
 * @param {expression} aLabel
 * @param {expression} aTooltip
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
                'aLabel': '=',
                'aTooltip': '='
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
