'use strict';

var appModalDirectives = angular.module('appDirectives.modal', []);


/**
 * @ngdoc directive
 * @name appDetailsModal
 * @restrict E
 *
 * @description
 * Root object for AngularStrap style modals
 */
appModalDirectives.directive('appDetailsModal',
    function appDetailsModal () {
        return {
            'restrict': 'E',
            'transclude': true,
            'replace': true,
            'scope': true,
            'templateUrl': 'partials/widgets/details_modal.html'
        };
    });


/**
 * @ngdoc directive
 * @name appDetailsModalNavbar
 * @restrict E
 *
 * @description
 * Common navbar object for modals
 */
appModalDirectives.directive('appDetailsModalNavbar',
    function appDetailsModalNavbar () {
        return {
            'require': '^appDetailsModal',
            'restrict': 'E',
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
appModalDirectives.directive('appDetailsModalPanel',
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
