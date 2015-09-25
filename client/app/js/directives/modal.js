'use strict';

var appModalDirectives = angular.module('appDirectives.modal', []);


/**
 * @ngdoc directive
 * @name appDetailsModal
 * @restrict E
 *
 * @param {expression} aBigModal
 *
 * @description
 * Root object for AngularStrap style modals
 *
 * @example
 * <app-details-modal a-big-modal="true">
 *   <span ng-controller="ItemController">
 *     <div class="modal-body">
 *       <app-details-modal-navbar>
 *         ...
 *       </app-details-modal-navbar>
 *       <div class="details-modal-content">
 *         ...
 *       </div>
 *     </div>
 *     <div class="modal-footer">
 *       ...
 *     </div>
 *   </span>
 * </app-details-modal>
 */
appModalDirectives.directive('appDetailsModal',
    function appDetailsModal () {
        return {
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aBigModal': '='
            },
            'templateUrl': 'partials/widgets/modal/details_modal.html'
        };
    });


/**
 * @ngdoc directive
 * @name appDetailsModalNavbar
 * @restrict E
 *
 * @description
 * Common navbar object for modals
 *
 * @example
 * <div class="modal-body">
 *   <app-details-modal-navbar>
 *     ...
 *   </app-details-modal-navbar>
 * </div>
 */
appModalDirectives.directive('appDetailsModalNavbar',
    function appDetailsModalNavbar () {
        return {
            'require': '^appDetailsModal',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': true,
            'templateUrl': 'partials/widgets/modal/details_modal_navbar.html'
        };
    });


/**
 * @ngdoc directive
 * @name appDetailsModalPanel
 * @restrict E
 *
 * @param {expression} aHalfWidth
 *
 * @description
 * Common navbar object for modals
 *
 * @example
 * <div class="details-modal-content">
 *   <app-details-modal-panel>
 *     <app-input-form>...</app-input-form>
 *     <app-input-form>...</app-input-form>
 *     ...
 *   </app-details-modal-panel>
 * </div>
 */
appModalDirectives.directive('appDetailsModalPanel',
    function appDetailsModalPanel () {
        return {
            'require': '^appDetailsModal',
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': {
                'aHalfWidth': '='
            },
            'templateUrl': 'partials/widgets/modal/details_modal_panel.html'
        };
    });
