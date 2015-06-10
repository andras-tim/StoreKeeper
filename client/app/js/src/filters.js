'use strict';

var appFilters = angular.module('appFilters', []);


appFilters.filter('setTitle', ['PageFactory',
    function (PageFactory) {
        return function (title) {
            PageFactory.setPageTitle(title);
            return title;
        };
    }]);


appFilters.filter('nestedIsContained', ['$parse', '$filter',
    function($parse, $filter) {
        function filterInAllFields(items, filters) {
            var f = $filter('filter');
            return f(items, {'$': filters.$});
        }

        return function (items, filters) {
            var itemsLeft;
            if ('$' in filters) {
                itemsLeft = filterInAllFields(items, filters);
            } else {
                itemsLeft = items.slice();
            }

            Object.keys(filters).forEach(function (model) {
                if (model === '$') {
                    return false;
                }
                var expected = filters[model].toLowerCase(),
                    getter = $parse(model);

                itemsLeft = itemsLeft.filter(function (item) {
                    var actual = getter(item);
                    return actual.toLowerCase().indexOf(expected) !== -1;
                });
            });

            return itemsLeft;
        };
    }]);
