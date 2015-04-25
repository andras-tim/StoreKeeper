'use strict';

var appFactories = angular.module('appFilters', []);


appFactories.filter('setTitle', function (PageFactory) {
    return function (title) {
        PageFactory.setPageTitle(title);
        return title;
    };
});
