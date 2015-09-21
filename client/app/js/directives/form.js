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
 *
 * @example
 * <ng-form name="inputForm">
 *   <app-input-validator a-form-input="inputForm.foo" a-required="{{ aRequired }}">
 *     <input name="foo" />
 *   </app-input-validator>
 * </ng-form>
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
 * @param {string} aLabel
 * @param {string} aRequired
 * @param {string=} [aLabelClass=col-sm-4]
 * @param {string=} [aInputClass=col-sm-8]
 *
 * @description
 * Nested forms and labels for inputs
 *
 * @example
 * <app-input-form a-label="{{ 'Username' | translate }}" a-required="{{ 'Username is required' | translate }}">
 *   <input name="username" id="usernameInput" ... />
 * </app-input-form>
 */
appFormDirectives.directive('appInputForm', ['$timeout', 'CommonFactory',
    function appInputForm ($timeout, CommonFactory) {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
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

                return {
                    'post': function postLink (scope, iElement, iAttrs, iCtrl, iTransclude) {
                        iTransclude(function (cloneElement) {
                            element.find('ng-transclude').prepend(cloneElement);

                            $timeout(function () {
                                var inputElement = cloneElement.find('input').addBack('input');

                                if (inputElement.length !== 1) {
                                    CommonFactory.printToConsole('Can not clearly identify the input element in <app-input-form>', {
                                        'element': iElement,
                                        'cloneElement': cloneElement,
                                        'inputElement': inputElement
                                    });
                                }

                                scope.aInputId = inputElement.attr('id');
                                scope.aInputName = inputElement.attr('name');
                            });

                        });
                    }
                };
            }
        };
    }]);


/**
 * @ngdoc directive
 * @name appCheckboxLabel
 * @restrict E
 *
 * @param {string} aLabel
 *
 * @description
 * Label for input[@type="checkbox"] elements
 *
 * @example
 * <app-checkbox-label a-label="{{ 'Remember me' | translate }}">
 *   <input type="checkbox" ... />
 * </app-checkbox-label>
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
 * @element ANY
 *
 * @param {string} appTooltip
 *
 * @description
 * Tooltip for form elements
 *
 * @example
 * <ANY app-tooltip="{{ 'Test message' | translate }}">
 *   ...
 * </ANY>
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
 * @name appTypeaheadHelper
 * @restrict E
 *
 * @param {function} aCreateCallback
 * @param {object=} [aLoadingSpinner]
 * @param {object=} [aCreatingSpinner]
 *
 * @description
 * Extend typeahead input[@type="text"] by add new element button and spinners.
 *
 * @example
 * <app-typeahead-helper a-create-callback="createVendor()" a-loading-spinner="loadingVendors" a-creating-spinner="creatingVendor">
 *   <input ng-model="item.vendor" bs-options="vendor as vendor.name for vendor in vendors" type="text" class="form-control" autocomplete="off" placeholder="{{ 'Enter vendor' | translate }}" required bs-typeahead />
 * </app-typeahead-helper>
 */
appFormDirectives.directive('appTypeaheadHelper', ['$timeout',
    function appTypeaheadHelper ($timeout) {
        return {
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aCreateCallback': '&',
                'aLoadingSpinner': '=',
                'aCreatingSpinner': '='
            },
            'templateUrl': 'partials/widgets/form/typeahead-helper.html',
            'link': function (scope, element, attrs, ctrl, transclude) {
                transclude(function (cloneElement) {
                    element.prepend(cloneElement);

                    $timeout(function () {
                        scope.aModelController = angular.element(cloneElement).data('$ngModelController');
                    });

                    element.on('keydown', function (event) {
                        if (event.which === 13 && scope.isReadyToCreate()) {
                            scope.aCreateCallback();
                        }
                    });
                });
            },
            'controller': ['$scope',
                function ($scope) {
                    function getModel() {
                        if ($scope.aModelController) {
                            return $scope.aModelController.$modelValue;
                        }
                        return undefined;
                    }

                    function isFilled() {
                        return typeof getModel() === 'object';
                    }

                    function isReadyToCreate() {
                        return getModel() && !isFilled() && !$scope.aLoadingSpinner && !$scope.aCreatingSpinner;
                    }

                    $scope.isReadyToCreate = isReadyToCreate;
                }]
        };
    }]);


/**
 * @ngdoc directive
 * @name appIndentedFormGroup
 * @restrict E
 *
 * @param {string=} [aClass=col-sm-offset-4 col-sm-8]
 *
 * @description
 * For easy indent objects without left-side label
 *
 * @example
 * <app-indented-form-group>
 *   <button></button>
 * </app-indented-form-group>
 */
appFormDirectives.directive('appIndentedFormGroup',
    function appIndentedFormGroup () {
        return {
            'require': '^form',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aClass': '@'
            },
            'templateUrl': 'partials/widgets/form/indented-form-group.html',
            'compile': function (element, attrs) {
                if (!attrs.aClass) {
                    attrs.aClass = 'col-sm-offset-4 col-sm-8';
                }
            }
        };
    });
