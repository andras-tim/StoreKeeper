'use strict';

var appFormDirectives = angular.module('appDirectives.form', []);


/**
 * @ngdoc directive
 * @name appLabel
 * @restrict E
 *
 * @param {string} appObjectId
 * @param {expression} appLabel
 * @param {string} [appLabelClass=col-sm-4]
 * @param {string} [appObjectClass=col-sm-8]
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
                'appObjectId': '@',
                'appLabel': '=',
                'appLabelClass': '@',
                'appObjectClass': '@'
            },
            'templateUrl': 'partials/widgets/label.html',
            'compile': function (element, attrs) {
                if (!attrs.appLabelClass) {
                    attrs.appLabelClass = 'col-sm-4';
                }
                if (!attrs.appObjectClass) {
                    attrs.appObjectClass = 'col-sm-8';
                }
            }
        };
    });


/**
 * @ngdoc directive
 * @name appFormInput
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
 * Input text for forms
 */
appFormDirectives.directive('appFormInput',
    function appFormInput () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
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
            'templateUrl': 'partials/widgets/form-input.html',
            'compile': function (element, attrs) {
                if (!attrs.appType) {
                    attrs.appType = 'text';
                }
                if (!attrs.appAutocomplete) {
                    attrs.appAutocomplete = attrs.appType === 'password' ? 'off' : 'on';
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
 * @name appFormTypeahead
 * @restrict E
 *
 * @param {string} appName
 * @param {object} appModel
 * @param {string} appDataSource
 * @param {expression} appLabel
 * @param {expression} appPlaceholder
 * @param {expression} appRequired
 * @param {function} appCreateCallback
 * @param {object} [appLoadingSpinner]
 * @param {object} [appCreatingSpinner]
 * @param {string} [appLabelClass=col-sm-4]
 * @param {string} [appInputClass=col-sm-8]
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
                'appName': '@',
                'appModel': '=',
                'appDataSource': '@',
                'appLabel': '=',
                'appPlaceholder': '=',
                'appRequired': '=',
                'appCreateCallback': '&',
                'appLoadingSpinner': '=',
                'appCreatingSpinner': '=',
                'appLabelClass': '@',
                'appInputClass': '@'
            },
            'templateUrl': 'partials/widgets/form-typeahead.html',
            'compile': function (element, attrs) {
                if (!attrs.appLabelClass) {
                    attrs.appLabelClass = 'col-sm-4';
                }
                if (!attrs.appInputClass) {
                    attrs.appInputClass = 'col-sm-8';
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
 * @param {string} appName
 * @param {object} appModel
 * @param {expression} appLabel
 * @param {expression} appTooltip
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
                'appName': '@',
                'appModel': '=',
                'appLabel': '=',
                'appTooltip': '='
            },
            'templateUrl': 'partials/widgets/form-checkbox.html'
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
appFormDirectives.directive('appCheckbox',
    function appCheckbox () {
        return {
            'require': '^form',
            'restrict': 'E',
            'scope': {
                'appName': '@',
                'appModel': '=',
                'appLabel': '=',
                'appTooltip': '='
            },
            'templateUrl': 'partials/widgets/checkbox.html'
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
appFormDirectives.directive('appIndentedFormGroup',
    function appIndentedFormGroup () {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'scope': {
                'appClass': '@'
            },
            'template': '<div class="form-group"><div class="{{ appClass }}" ng-transclude></div></div>',
            'compile': function (element, attrs) {
                if (!attrs.appClass) {
                    attrs.appClass = 'col-sm-offset-4 col-sm-8';
                }
            }
        };
    });
