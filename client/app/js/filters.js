'use strict';

var appFilters = angular.module('appFilters', []);


appFilters.filter('setTitle', ['PageFactory',
    function (PageFactory) {
        return function (title) {
            PageFactory.setPageTitle(title);
            return title;
        };
    }]);
