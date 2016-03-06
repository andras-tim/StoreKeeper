'use strict';

var appTableDirectives = angular.module('appDirectives.table', []);


/**
 * @ngdoc directive
 * @name appTablePersist
 * @restrict A
 * @element table
 *
 * @param {string} appTablePersist unique ID of persistent storage
 *
 * @description
 * Persist table state to local storage and search of $location
 *
 * @example
 * <table st-table="displayedItems" ... app-table-persist="items">
 *   ...
 * </table>
 */
appTableDirectives.directive('appTablePersist',
    function appTablePersist () {
        return {
            'require': 'stTable',
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
 *
 * @example
 * <nav>
 *   <ul class="pagination">
 *     ...
 *     <li>
 *       <a><app-page-input></app-page-input> / {{ numPages }}</a>
 *     </li>
 *     ...
 *   </ul>
 * </nav>
 */
appTableDirectives.directive('appPageInput',
    function appPageInput () {
        return {
            'restrict': 'E',
            'template': '<input type="text" class="select-page no-buttons" ng-model="inputPage" ng-change="selectPage(inputPage)" autocomplete="off" />',
            'link': function (scope) {
                scope.$watch('currentPage', function (newValue) {
                    scope.inputPage = newValue;
                });
            }
        };
    });

