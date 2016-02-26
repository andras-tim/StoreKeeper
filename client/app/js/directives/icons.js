'use strict';

var appIconsDirectives = angular.module('appDirectives.icons', []);


appIconsDirectives.constant('iconList', {
    'item':         'fa fa-cube',
    'items':        'fa fa-cube',
    'barcode':      'fa fa-barcode',

    'new':          'fa fa-sticky-note-o',
    'user':         'fa fa-user',
    'language':     'fa fa-flag',
    'spinner':      'fa fa-spinner fa-pulse',
    'warn':         'fa fa-exclamation-triangle',

    'close':        'fa fa-times',
    'logout':       'fa fa-sign-out',
    'search':       'fa fa-search',
    'add':          'fa fa-plus',
    'delete':       'fa fa-trash-o',
    'download':     'fa fa-download',
    'print':        'fa fa-print',
    'addToView':    'fa fa-share',
    'assign':       'fa fa-pencil-square-o',

    'jumpFirst':    'fa fa-fast-backward',
    'jumpPrev':     'fa fa-step-backward',
    'jumpNext':     'fa fa-step-forward',
    'jumpLast':     'fa fa-fast-forward',

    'github':       'fa fa-github'
});


/**
 * @ngdoc directive
 * @name appIcon
 * @restrict A
 *
 * @param {string} appIcon
 *
 * @description
 * Substitutes with the selected icon
 *
 * @example
 * <i app-icon="item"></i>
 */
appIconsDirectives.directive('appIcon', ['$compile', 'iconList', 'CommonFactory',
    function appIcon ($compile, iconList, CommonFactory) {
        return {
            'restrict': 'A',
            'replace': true,
            'scope': {
                'appIcon': '@'
            },
            'link': function (scope, element) {
                var iconId = scope.appIcon,
                    iconClass = iconList[iconId];

                if (iconClass === undefined) {
                    CommonFactory.printToConsole('Can not find icon: ' + iconId);
                    return;
                }
                element.append(' <i class="' + iconClass + '"></i> ');
            }
        };
    }]);
