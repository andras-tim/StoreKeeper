'use strict';

var appCommonDirectives = angular.module('appDirectives.common', []);


/**
 * @ngdoc directive
 * @name appSpinner
 * @restrict EA
 *
 * @description
 * Append a spinner
 */
appCommonDirectives.directive('appSpinner',
    function appSpinner () {
        return {
            'restrict': 'EA',
            'template': ' <i class="fa fa-spinner fa-pulse"></i> '
        };
    });


/**
 * @ngdoc directive
 * @name appConfirmOnExit
 * @restrict A
 *
 * @param {function} appConfirmOnExit dirty validator
 * @param {expression=} [appModalId] name of parent modal
 *
 * @description
 * Confirm of leaving dirty form
 */
appCommonDirectives.directive('appConfirmOnExit', ['$rootScope', '$window', 'gettextCatalog',
    function appConfirmOnExit ($rootScope, $window, gettextCatalog) {
        return {
            'scope': {
                'appConfirmOnExit': '&',
                'appModalId': '='
            },
            'restrict': 'A',
            'link': function (scope, element, attr) {
                var dirtyOnExitQuestion,
                    windowBeforeUnloadUnbind,
                    modalHideUnbind,
                    locationChangeUnbind;

                function handleWindowUnload(event) {
                    if (scope.appConfirmOnExit()) {
                        event.preventDefault();
                    }
                }

                function handleLocationChange(event) {
                    if (scope.appConfirmOnExit()) {
                        if (!$window.confirm(dirtyOnExitQuestion)) {
                            event.preventDefault();
                        }
                    }
                }

                function handleCloseModal(event, $modal) {
                    if ($modal.$id !== scope.appModalId) {
                        return;
                    }
                    if (scope.appConfirmOnExit()) {
                        if (!$window.confirm(dirtyOnExitQuestion)) {
                            event.preventDefault();
                        }
                    }
                }

                dirtyOnExitQuestion = gettextCatalog.getString('The form is dirty. Do you want to stay on the page?');

                modalHideUnbind = $rootScope.$on('modal.hide.before', handleCloseModal);
                locationChangeUnbind = $rootScope.$on('$locationChangeStart', handleLocationChange);
                if (attr.appModalId !== undefined) {
                    windowBeforeUnloadUnbind = $rootScope.$on('windowBeforeUnload', handleWindowUnload);
                }

                scope.$on('$destroy', function () {
                    modalHideUnbind();
                    locationChangeUnbind();
                    if (windowBeforeUnloadUnbind) {
                        windowBeforeUnloadUnbind();
                    }
                });
            }
        };
    }]);

