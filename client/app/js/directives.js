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
            'restrict': 'EA',
            'template': ' <i class="fa fa-spinner fa-pulse"></i> '
        };
    });


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
appDirectives.directive('appLabel',
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
appDirectives.directive('appFormInput',
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
appDirectives.directive('appFormTypeahead',
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
appDirectives.directive('appFormCheckbox',
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
appDirectives.directive('appCheckbox',
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
appDirectives.directive('appIndentedFormGroup',
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


/**
 * @ngdoc directive
 * @name appTablePersist
 * @restrict A
 *
 * @param {string} appTablePersist unique ID of persistent storage
 *
 * @description
 * Persist table state to local storage and search of $location
 */
appDirectives.directive('appTablePersist',
    function appTablePersist () {
        return {
            'require': '^stTable',
            'restrict': 'A',
            'scope': {
                'appTablePersist': '@'
            },
            'link': function (scope, element, attr, ctrl) {
                var configId = 'table_' + attr.appTablePersist;

                function backupState(newValue, oldValue) {
                    if (newValue === oldValue) {
                        return;
                    }

                    var state = {
                        'version': 1,
                        'sort': newValue.sort
                    };

                    localStorage.setItem(configId, JSON.stringify(state));
                }

                function restoreState() {
                    var currentState,
                        stateJson,
                        state;

                    stateJson = localStorage.getItem(configId);
                    if (!stateJson) {
                        return;
                    }

                    state = JSON.parse(stateJson);
                    currentState = ctrl.tableState();

                    if (state.version === 1) {
                        currentState.sort = state.sort;
                    }

                    ctrl.pipe();
                }

                scope.$watch(function () {
                    return ctrl.tableState();
                }, backupState, true);

                restoreState();
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
            'restrict': 'E',
            'template': '<input type="text" class="select-page" ng-model="inputPage" ' +
                        'ng-change="selectPage(inputPage)">',
            'link': function (scope) {
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
            'require': 'tr',
            'restrict': 'A',
            'priority': 5000,
            'compile': function (element, attrs) {
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
            'restrict': 'EA',
            'transclude': true,
            'replace': true,
            'scope': true,
            'templateUrl': 'partials/widgets/details_modal.html'
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
            'require': '^appDetailsModal',
            'restrict': 'EA',
            'transclude': true,
            'replace': true,
            'scope': true,
            'templateUrl': 'partials/widgets/details_modal_navbar.html'
        };
    });


/**
 * @ngdoc directive
 * @name appDetailsModalPanel
 * @restrict E
 *
 * @description
 * Common navbar object for modals
 */
appDirectives.directive('appDetailsModalPanel',
    function appDetailsModalPanel () {
        return {
            'require': '^appDetailsModal',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': true,
            'templateUrl': 'partials/widgets/details_modal_panel.html'
        };
    });
