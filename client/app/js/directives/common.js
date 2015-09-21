'use strict';

var appCommonDirectives = angular.module('appDirectives.common', []);


/**
 * @ngdoc directive
 * @name appConfirmOnExit
 * @restrict A
 * @element form
 *
 * @param {function} appConfirmOnExit dirty validator
 * @param {expression=} [aModalId] name of parent modal
 *
 * @description
 * Confirm of leaving dirty form
 *
 * @example
 * <form name="itemForm" app-confirm-on-exit="itemForm.$dirty" a-modal-id="modalId">
 *   ...
 * </form>
 */
appCommonDirectives.directive('appConfirmOnExit', ['$rootScope', '$window', 'gettextCatalog',
    function appConfirmOnExit ($rootScope, $window, gettextCatalog) {
        return {
            'scope': {
                'appConfirmOnExit': '&',
                'aModalId': '='
            },
            'require': 'form',
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
                    if ($modal.$id !== scope.aModalId) {
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
                if (attr.aModalId !== undefined) {
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

